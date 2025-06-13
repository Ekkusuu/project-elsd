from src.TimelineParser import TimelineParser
from src.TimelineParserVisitor import TimelineParserVisitor
from src.models import Event, Period, Timeline, Relationship, Date


def apply_comparison(left, right, op):
    if left is None or right is None:
        return False

    if isinstance(left, dict) and 'year' in left:
        left = Date(left)
    if isinstance(right, dict) and 'year' in right:
        right = Date(right)

    if isinstance(left, int) and isinstance(right, Date):
        left = Date({"year": left})
    if isinstance(right, int) and isinstance(left, Date):
        right = Date({"year": right})

    ops = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "<": lambda a, b: a < b,
        ">": lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b
    }
    try:
        return ops.get(op, lambda a, b: False)(left, right)
    except TypeError as e:
        print(f"Comparison error: Cannot compare {type(left)} with {type(right)}")
        raise TypeError(e)
        return False


class ValidationError(Exception):
    """Custom exception for validation errors"""
    def __init__(self, message, line=None, column=None):
        super().__init__(message)
        self.line = line
        self.column = column


class TimelineInterpreter(TimelineParserVisitor):
    def __init__(self):
        self.events = {}
        self.periods = {}
        self.timelines = {}
        self.relationships = {}
        self.already_exported = set()
        self.interpretation_errors = []

    def add_error(self, error_msg, ctx=None, ExceptionType=Exception):
        line = None
        column = None
        if ctx and hasattr(ctx, 'start') and ctx.start:
            line = ctx.start.line
            column = ctx.start.column

        error = {
            'message': error_msg,
            'line': line,
            'column': column
        }
        self.interpretation_errors.append(error)
        raise ExceptionType(error_msg)

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

        self.add_error("No matching date format found", ctx, ExceptionType=ValidationError)
        return None

    def visitEventDecl(self, ctx: TimelineParser.EventDeclContext):
        event_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')
        date_dict = self.visit(ctx.dateExpr())

        if event_id in self.periods.keys() or event_id in self.relationships.keys() or event_id in self.timelines.keys():
            self.add_error(f"Identifier '{event_id}' is already used", ctx, ExceptionType=NameError)

        if not date_dict:
            self.add_error(f"Invalid date format for event {event_id}", ctx, ExceptionType=ValidationError)
            return None
            
        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()
            
        try:
            event = Event(event_id, title, date_dict, importance)
            self.events[event_id] = event
        except ValueError as e:
            self.add_error(f"Error in event {event_id}: {str(e)}", ctx, ExceptionType=ValidationError)
            return None

    def visitPeriodDecl(self, ctx: TimelineParser.PeriodDeclContext):
        period_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')
        start_dict = self.visit(ctx.dateExpr(0))
        end_dict = self.visit(ctx.dateExpr(1))

        if period_id in self.events.keys() or period_id in self.relationships.keys() or period_id in self.timelines.keys():
            self.add_error(f"Identifier '{period_id}' is already used", ctx, ExceptionType=NameError)

        if not start_dict or not end_dict:
            self.add_error(f"Invalid date format for period {period_id}", ctx, ExceptionType=ValidationError)
            return None
            
        importance = "MEDIUM"
        if ctx.IMPORTANCE():
            importance = ctx.importanceValue().getText().upper()
            
        try:
            period = Period(period_id, title, start_dict, end_dict, importance)
            self.periods[period_id] = period
        except ValueError as e:
            self.add_error(f"Error in period {period_id}: {str(e)}", ctx, ExceptionType=ValidationError)
            return None

    def visitTimelineDecl(self, ctx: TimelineParser.TimelineDeclContext):
        timeline_id = ctx.ID().getText()
        title = ctx.STRING().getText().strip('"')

        if timeline_id in self.events.keys() or timeline_id in self.relationships.keys() or timeline_id in self.periods.keys():
            self.add_error(f"Identifier '{timeline_id}' is already used", ctx, ExceptionType=NameError)

        components = []
        comp_ctx = ctx.componentList()
        if comp_ctx: 
            for comp_id in [id.getText() for id in comp_ctx.ID()]:
                component = self.events.get(comp_id) or self.periods.get(comp_id) or self.relationships.get(comp_id)
                if component:
                    components.append(component)
                else:
                    self.add_error(f"Timeline component '{comp_id}' does not exist", comp_ctx, ExceptionType=ValidationError)
                    return None
                    
        try:
            timeline = Timeline(timeline_id, title, components)
            self.timelines[timeline_id] = timeline
        except ValueError as e:
            self.add_error(f"Error in timeline {timeline_id}: {str(e)}", ctx, ExceptionType=ValidationError)
            return None

    def visitRelationshipDecl(self, ctx: TimelineParser.RelationshipDeclContext):
        rel_id = ctx.ID()[0].getText()
        from_id = ctx.ID()[1].getText()
        to_id = ctx.ID()[2].getText()
        rel_type = ctx.relationshipType().getText()

        if rel_id in self.events.keys() or rel_id in self.timelines.keys() or rel_id in self.periods.keys():
            self.add_error(f"Identifier '{rel_id}' is already used", ctx, ExceptionType=NameError)

        from_comp = self.events.get(from_id) or self.periods.get(from_id)
        to_comp = self.events.get(to_id) or self.periods.get(to_id)
        
        if not from_comp:
            self.add_error(f"Relationship 'from' component '{from_id}' does not exist", ctx, ExceptionType=ValidationError)
            return None
            
        if not to_comp:
            self.add_error(f"Relationship 'to' component '{to_id}' does not exist", ctx, ExceptionType=ValidationError)
            return None
            
        try:
            relationship = Relationship(rel_id, from_comp, to_comp, rel_type)
            self.relationships[rel_id] = relationship
        except ValueError as e:
            self.add_error(f"Error in relationship {rel_id}: {str(e)}", ctx, ExceptionType=ValidationError)
            return None

    def visitExportStmt(self, ctx: TimelineParser.ExportStmtContext):
        export_id = ctx.ID().getText()
        
        if self.interpretation_errors:
            return None
            
        if export_id in self.already_exported:
            print(f"[Info] Skipping already exported: {export_id}")
            return None
            
        self.already_exported.add(export_id)

        if export_id in self.timelines:
            print(f"[Info] Timeline {export_id} marked for export")
        elif export_id in self.events:
            print(f"[Info] Event {export_id} marked for export")
        elif export_id in self.periods:
            print(f"[Info] Period {export_id} marked for export")
        elif export_id in self.relationships:
            print(f"[Info] Relationship {export_id} marked for export")
        # elif export_id in self._loop_vars.keys():
        #
        else:
            self.add_error(f"ID '{export_id}' not found.", ctx, ExceptionType=LookupError)
            
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

            # Handle date comparisons
            if isinstance(left, dict) and 'year' in left:
                left = Date(left)
            if isinstance(right, dict) and 'year' in right:
                right = Date(right)
            try:
                return apply_comparison(left, right, op)
            except TypeError as e:
                self.add_error(str(e), ctx, TypeError)

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
            elif not component:
                self.add_error(f"Component '{obj_id}' not found", ctx, ExceptionType=LookupError)
            
            if component:
                if hasattr(component, prop):
                    value = getattr(component, prop)
                    # If it's a Date object, convert to dict for consistency
                    if isinstance(value, Date):
                        return {"year": value.year, "month": value.month, "day": value.day}
                    return value
                elif isinstance(component, dict) and prop in component:
                    return component[prop]
                else:
                    self.add_error(f"No {prop} property for {obj_id}", ctx, ExceptionType=ValidationError)
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
            self.add_error(f"Cannot iterate over unknown collection '{collection_id}'", ctx, ExceptionType=LookupError)
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
        
        # First check if it's a loop variable
        component = None
        if hasattr(self, '_loop_vars') and component_id in self._loop_vars:
            component = self._loop_vars[component_id]
        else:
            # If not a loop variable, check regular components
            component = (self.events.get(component_id) or 
                       self.periods.get(component_id) or 
                       self.relationships.get(component_id) or 
                       self.timelines.get(component_id))
        
        if not component:
            self.add_error(f"Cannot modify unknown component '{component_id}'", ctx, ExceptionType=LookupError)
            return None
            
        # Process each property assignment
        for assignment in ctx.propertyAssignment():
            prop = assignment.property_().getText().lower()
            value = self.visitExpr(assignment.expr())
            
            try:
                if prop in ['date', 'start', 'end']:
                    # For date properties, we need to handle both dictionary and string formats
                    date_dict = value
                    
                    # Create a new Date object with the dictionary
                    if isinstance(component, Event):
                        if prop == 'date':
                            component.date = Date(date_dict)
                        else:
                            self.add_error("No such property for component of type Event", ctx, ExceptionType=AttributeError)
                    if isinstance(component, Period):
                        if prop == 'start':
                            component.start = Date(date_dict)
                        elif prop == 'end':
                            component.end = Date(date_dict)
                        else:
                            self.add_error("No such property for component of type Period", ctx, ExceptionType=AttributeError)
                else:
                    # For non-date properties, set them directly
                    if hasattr(component, prop):
                        setattr(component, prop, value)
                    elif isinstance(component, dict):
                        component[prop] = value
            except (AttributeError, ValueError) as e:
                self.add_error(f"Error modifying {component_id}.{prop}: {str(e)}", ctx, ExceptionType=AttributeError)
        
        # Validate the component after all modifications
        try:
            if isinstance(component, Period):
                # Validate that start date is before end date
                if component.start >= component.end:
                    self.add_error(
                        f"Invalid period {component_id}: start date ({component.start}) must be before end date ({component.end})",
                        ctx, ExceptionType=ValidationError)
            elif isinstance(component, Event):
                # Validate the date is properly set
                if not component.date:
                    self.add_error(f"Invalid event {component_id}: date is not set", ctx, ExceptionType=ValidationError)
            elif isinstance(component, Timeline):
                # Validate timeline components
                if hasattr(component, 'validate_components'):
                    component.validate_components()
            elif isinstance(component, Relationship):
                # Validate relationship components exist and are properly linked
                if not component.from_component or not component.to_component:
                    self.add_error(f"Invalid relationship {component_id}: missing from/to components", ctx, ExceptionType=ValidationError)
        except Exception as e:
            self.add_error(f"Validation error in {component_id}: {str(e)}", ctx, ExceptionType=ValidationError)
                
        return None
