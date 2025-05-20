from src.TimelineParser import TimelineParser
from src.TimelineParserVisitor import TimelineParserVisitor
from src.models import Event, Period, Timeline, Relationship, Date


def apply_comparison(left, right, op):
    ops = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b
    }
    return ops.get(op, lambda a, b: False)(left, right)


class TimelineInterpreter(TimelineParserVisitor):
    def __init__(self):
        self.events = {}
        self.periods = {}
        self.timelines = {}
        self.relationships = {}
        self.already_exported = set()
        self.validation_errors = []

    def format_date(self, date_dict):
        """Convert a date dictionary to a formatted string."""
        if not isinstance(date_dict, dict):
            return date_dict
        
        if 'year' in date_dict:
            year = date_dict['year']
            if 'month' in date_dict and 'day' in date_dict:
                return f"{date_dict['day']}-{date_dict['month']}-{year}"
            elif 'month' in date_dict:
                return f"{date_dict['month']}-{year}"
            return str(year)
        return None

    # def parse_date_string(self, date_str):
    #     """Convert a date string back to a dictionary format."""
    #     if not isinstance(date_str, str):
    #         return date_str
    #
    #     parts = date_str.split('-')
    #     if len(parts) == 3:  # day-month-year
    #         return {"year": int(parts[2]), "month": int(parts[1]), "day": int(parts[0])}
    #     elif len(parts) == 2:  # month-year
    #         return {"year": int(parts[1]), "month": int(parts[0])}
    #     else:  # year only
    #         try:
    #             return {"year": int(date_str)}
    #         except ValueError:
    #             return date_str

    def visitYearLiteral(self, ctx: TimelineParser.YearLiteralContext):
        year = int(ctx.INT().getText())
        if ctx.BCE():
            year = -year
        return year

    def visitMonthYearLiteral(self, ctx: TimelineParser.MonthYearLiteralContext):
        month = int(ctx.INT().getText())
        year = self.visit(ctx.yearLiteral())
        return {"year": year, "month": month}

    def visitFullDateLiteral(self, ctx: TimelineParser.FullDateLiteralContext):
        day = int(ctx.INT().getText())
        month_year = self.visit(ctx.monthYearLiteral())
        return {"year": month_year["year"], "month": month_year["month"], "day": day}

    def visitDateExpr(self, ctx: TimelineParser.DateExprContext):
        if ctx.yearLiteral():
            year = self.visit(ctx.yearLiteral())
            return {"year": year}
            
        if ctx.monthYearLiteral():
            return self.visit(ctx.monthYearLiteral())
            
        if ctx.fullDateLiteral():
            return self.visit(ctx.fullDateLiteral())
            
        if ctx.dateCalculation():
            return self.visit(ctx.dateCalculation())
            
        print("No matching date format found")
        return None

    def visitEventDecl(self, ctx: TimelineParser.EventDeclContext):
        event_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')
        date_dict = self.visit(ctx.dateExpr())
        
        if not date_dict:
            self.validation_errors.append(f"Invalid date format for event {event_id}")
            return None
            
        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()
            
        try:
            event = Event(event_id, title, date_dict, importance)
            self.events[event_id] = event
        except ValueError as e:
            self.validation_errors.append(f"Error in event {event_id}: {str(e)}")
            return None

    def visitPeriodDecl(self, ctx: TimelineParser.PeriodDeclContext):
        period_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')
        start_dict = self.visit(ctx.dateExpr(0))
        end_dict = self.visit(ctx.dateExpr(1))
        
        if not start_dict or not end_dict:
            self.validation_errors.append(f"Invalid date format for period {period_id}")
            return None
            
        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()
            
        try:
            period = Period(period_id, title, start_dict, end_dict, importance)
            self.periods[period_id] = period
        except ValueError as e:
            self.validation_errors.append(f"Error in period {period_id}: {str(e)}")
            return None

    def visitTimelineDecl(self, ctx: TimelineParser.TimelineDeclContext):
        timeline_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')
        
        components = []
        comp_ctx = ctx.componentList()
        if comp_ctx: 
            for comp_id in [id.getText() for id in comp_ctx.ID()]:
                component = self.events.get(comp_id) or self.periods.get(comp_id) or self.relationships.get(comp_id)
                if component:
                    components.append(component)
                else:
                    self.validation_errors.append(f"Timeline component '{comp_id}' does not exist")
                    return None
                    
        try:
            timeline = Timeline(timeline_id, title, components)
            self.timelines[timeline_id] = timeline
        except ValueError as e:
            self.validation_errors.append(f"Error in timeline {timeline_id}: {str(e)}")
            return None

    def visitRelationshipDecl(self, ctx: TimelineParser.RelationshipDeclContext):
        rel_id = ctx.ID()[0].getText()
        from_id = ctx.ID()[1].getText()
        to_id = ctx.ID()[2].getText()
        rel_type = ctx.relationshipType().getText()
        
        from_comp = self.events.get(from_id) or self.periods.get(from_id)
        to_comp = self.events.get(to_id) or self.periods.get(to_id)
        
        if not from_comp:
            self.validation_errors.append(f"Relationship 'from' component '{from_id}' does not exist")
            return None
            
        if not to_comp:
            self.validation_errors.append(f"Relationship 'to' component '{to_id}' does not exist")
            return None
            
        try:
            relationship = Relationship(rel_id, from_comp, to_comp, rel_type)
            self.relationships[rel_id] = relationship
        except ValueError as e:
            self.validation_errors.append(f"Error in relationship {rel_id}: {str(e)}")
            return None

    def visitExportStmt(self, ctx: TimelineParser.ExportStmtContext):
        export_id = ctx.ID().getText()
        
        if self.validation_errors:
            print("Validation errors found:")
            for error in self.validation_errors:
                print(f"  - {error}")
            return None
            
        if export_id in self.already_exported:
            print(f"[Info] Skipping already exported: {export_id}")
            return None
            
        self.already_exported.add(export_id)
        
        # Just mark the component as exported, actual data generation happens in Flask app
        if export_id in self.timelines:
            print(f"[Info] Timeline {export_id} marked for export")
        elif export_id in self.events:
            print(f"[Info] Event {export_id} marked for export")
        elif export_id in self.periods:
            print(f"[Info] Period {export_id} marked for export")
        elif export_id in self.relationships:
            print(f"[Info] Relationship {export_id} marked for export")
        else:
            print(f"[Warning] ID '{export_id}' not found.")
            
        return None

    def visitIfStmt(self, ctx: TimelineParser.IfStmtContext):
        condition_result = self.visitCondition(ctx.condition())
        if condition_result and ctx.ELSE():
            # Execute if block statements
            print("then gets exec")
            then_block = ctx.statement()[:len(ctx.statement()) // 2]
            for stmt in then_block:
                self.visit(stmt)
        elif condition_result:
            for stmt in ctx.statement():
                self.visit(stmt)
        elif ctx.ELSE() and not condition_result:
            # Execute else block statements if they exist
            print("else gets exec")
            else_block = ctx.statement()[len(ctx.statement())//2:]  # Second half of statements are in else block
            for stmt in else_block:
                self.visit(stmt)
        return None

    def visitCondition(self, ctx: TimelineParser.ConditionContext):
        if ctx.comparisonOp():
            left = self.visitExpr(ctx.expr(0))
            right = self.visitExpr(ctx.expr(1))
            op = ctx.comparisonOp().getText()
            return apply_comparison(left, right, op)
        elif ctx.ID():
            comp_id = ctx.ID().getText()
            return comp_id in self.events or comp_id in self.periods or comp_id in self.timelines
        elif ctx.booleanLiteral():
            return ctx.booleanLiteral().getText().lower() == "true"
        return False

    def visitExpr(self, ctx: TimelineParser.ExprContext):
        if ctx.ID() and ctx.property_():
            obj_id = ctx.ID().getText()
            prop = ctx.property_().getText().lower()
            
            component = (self.events.get(obj_id) or 
                       self.periods.get(obj_id) or 
                       self.relationships.get(obj_id) or 
                       self.timelines.get(obj_id))
            
            # Check if the component exists and handle loop variables
            if not component and hasattr(self, '_loop_vars') and obj_id in self._loop_vars:
                component = self._loop_vars[obj_id]
            
            if component:
                if hasattr(component, prop):
                    return getattr(component, prop)
                elif isinstance(component, dict) and prop in component:
                    return component[prop]
            return None
        elif ctx.STRING():
            return ctx.STRING().getText().strip('"')
        elif ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.dateExpr():
            return self.visitDateExpr(ctx.dateExpr())
        elif ctx.importanceValue():
            return ctx.importanceValue().getText().upper()
        elif ctx.ID():
            # First check if it's a loop variable
            if hasattr(self, '_loop_vars') and ctx.ID().getText() in self._loop_vars:
                return self._loop_vars[ctx.ID().getText()]
            return ctx.ID().getText()
        return None

    def visitForStmt(self, ctx: TimelineParser.ForStmtContext):
        # Get the iterator variable and collection
        iter_var = ctx.ID(0).getText()
        collection_id = ctx.ID(1).getText()
        
        # Find the collection to iterate over
        collection = None
        if collection_id in self.timelines:
            timeline = self.timelines[collection_id]
            collection = timeline.components if hasattr(timeline, 'components') else []
        elif collection_id in self.events:
            collection = [self.events[collection_id]]
        elif collection_id in self.periods:
            collection = [self.periods[collection_id]]
        else:
            self.validation_errors.append(f"Cannot iterate over unknown collection '{collection_id}'")
            return None
            
        # Execute the for loop body for each item
        for item in collection:
            # Store the current item in a way accessible to other visitors
            if not hasattr(self, '_loop_vars'):
                self._loop_vars = {}
            self._loop_vars[iter_var] = item
            
            # Execute all statements in the loop body
            for stmt in ctx.statement():
                self.visit(stmt)
                
        # Clean up the loop variable
        if hasattr(self, '_loop_vars') and iter_var in self._loop_vars:
            del self._loop_vars[iter_var]
            
        return None

    def visitModifyStmt(self, ctx: TimelineParser.ModifyStmtContext):
        # Get the component to modify
        component_id = ctx.ID().getText()
        component = (self.events.get(component_id) or 
                   self.periods.get(component_id) or 
                   self.relationships.get(component_id) or 
                   self.timelines.get(component_id))
        
        if not component:
            self.validation_errors.append(f"Cannot modify unknown component '{component_id}'")
            return None
            
        # Process each property assignment
        for assignment in ctx.propertyAssignment():
            prop = assignment.property_().getText().lower()
            value = self.visitExpr(assignment.expr())
            
            try:
                if prop in ['date', 'start', 'end']:
                    # For date properties, we need to handle both dictionary and string formats
                    # if isinstance(value, dict):
                    # If it's already a dictionary (from dateExpr), use it directly
                    date_dict = value
                    # else:
                    #     # If it's a string (from a previous modification), parse it back to a dictionary
                    #     date_dict = self.parse_date_string(value)
                    
                    # Create a new Date object with the dictionary
                    if isinstance(component, Event):
                        if prop == 'date':
                            component.date = Date(date_dict)
                        else:
                            self.validation_errors.append("No such property for component of type Event")
                    if isinstance(component, Period):
                        if prop == 'start':
                            component.start = Date(date_dict)
                        elif prop == 'end':
                            component.end = Date(date_dict)
                        else:
                            self.validation_errors.append("No such property for component of type Period")
                else:
                    # For non-date properties, set them directly
                    if hasattr(component, prop):
                        setattr(component, prop, value)
                    elif isinstance(component, dict):
                        component[prop] = value
            except (AttributeError, ValueError) as e:
                self.validation_errors.append(f"Error modifying {component_id}.{prop}: {str(e)}")
        
        # Validate the component after all modifications
        try:
            if isinstance(component, Period):
                # Validate that start date is before end date
                if component.start >= component.end:
                    self.validation_errors.append(f"Invalid period {component_id}: start date ({component.start}) must be before end date ({component.end})")
            elif isinstance(component, Event):
                # Validate the date is properly set
                if not component.date:
                    self.validation_errors.append(f"Invalid event {component_id}: date is not set")
            elif isinstance(component, Timeline):
                # Validate timeline components
                if hasattr(component, 'validate_components'):
                    component.validate_components()
            elif isinstance(component, Relationship):
                # Validate relationship components exist and are properly linked
                if not component.from_component or not component.to_component:
                    self.validation_errors.append(f"Invalid relationship {component_id}: missing from/to components")
        except Exception as e:
            self.validation_errors.append(f"Validation error in {component_id}: {str(e)}")
                
        return None
