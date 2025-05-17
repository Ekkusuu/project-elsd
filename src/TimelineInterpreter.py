from src.TimelineParser import TimelineParser
from src.TimelineParserVisitor import TimelineParserVisitor
from src.models import Event, Period, Timeline, Relationship

# def apply_comparison(left, right, op):
#     ops = {
#         "==": lambda a, b: a == b,
#         "!=": lambda a, b: a != b,
#         "<": lambda a, b: a < b,
#         ">": lambda a, b: a > b,
#         "<=": lambda a, b: a <= b,
#         ">=": lambda a, b: a >= b
#     }
#     return ops.get(op, lambda a, b: False)(left, right)


class TimelineInterpreter(TimelineParserVisitor):
    def __init__(self):
        self.events = {}
        self.periods = {}
        self.timelines = {}
        self.relationships = {}
        self.already_exported = set()
        self.validation_errors = []

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
                component = self.events.get(comp_id) or self.periods.get(comp_id)
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
        
        if export_id in self.timelines:
            timeline = self.timelines[export_id]
            filename_json = f"{export_id}.json"
            filename_png = f"{export_id}.png"
            
            timeline.export_json(filename_json)
            timeline.export_png()  # This is empty for now
            print(f"[Exported] Timeline data saved to {filename_json}")
            print(f"[Exported] Timeline image saved to {filename_png}")

        elif export_id in self.events:
            event = self.events[export_id]
            filename = f"{export_id}.json"
            event.export_json(filename)
            print(f"[Exported] Event data saved to {filename}")
            
        elif export_id in self.periods:
            period = self.periods[export_id]
            filename = f"{export_id}.json"
            period.export_json(filename)
            print(f"[Exported] Period data saved to {filename}")
            
        else:
            print(f"[Warning] ID '{export_id}' not found.")
            
        return None


    # def visitIfStmt(self, ctx: TimelineParser.IfStmtContext):
    #     result = self.evaluate_condition(ctx.condition())
    #
    #     if result:
    #         for stmt in ctx.statement():
    #             self.visit(stmt)
    #     elif ctx.ELSE():
    #         else_block = ctx.getChild(6)  # The ELSE block is always the 7th child
    #         for stmt in else_block.statement():
    #             self.visit(stmt)
    #     return None
    #
    # def evaluate_condition(self, ctx):
    #     # Case: expr OP expr
    #     if ctx.comparisonOp():
    #         left = self.evaluate_expr(ctx.expr(0))
    #         right = self.evaluate_expr(ctx.expr(1))
    #         op = ctx.comparisonOp().getText()
    #         return apply_comparison(left, right, op)
    #     elif ctx.ID():
    #         comp_id = ctx.ID().getText()
    #         return comp_id in self.events or comp_id in self.periods
    #     elif ctx.booleanLiteral():
    #         return ctx.booleanLiteral().getText().lower() == "true"
    #     return False
    #
    # def evaluate_expr(self, ctx):
    #     if ctx.ID() and ctx.property_():
    #         obj_id = ctx.ID().getText()
    #         prop = ctx.property_().getText().lower()
    #
    #         component = self.events.get(obj_id) or self.periods.get(obj_id)
    #         if component:
    #             return getattr(component, prop, None)
    #
    #     elif ctx.STRING():
    #         return ctx.STRING().getText().strip('"')
    #     elif ctx.INT():
    #         return int(ctx.INT().getText())
    #     elif ctx.importanceValue():
    #         return ctx.importanceValue().getText().upper()
    #     return None
    #
