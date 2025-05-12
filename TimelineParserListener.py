# Generated from TimelineParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TimelineParser import TimelineParser
else:
    from TimelineParser import TimelineParser

# This class defines a complete listener for a parse tree produced by TimelineParser.
class TimelineParserListener(ParseTreeListener):

    # Enter a parse tree produced by TimelineParser#program.
    def enterProgram(self, ctx:TimelineParser.ProgramContext):
        pass

    # Exit a parse tree produced by TimelineParser#program.
    def exitProgram(self, ctx:TimelineParser.ProgramContext):
        pass


    # Enter a parse tree produced by TimelineParser#declaration.
    def enterDeclaration(self, ctx:TimelineParser.DeclarationContext):
        pass

    # Exit a parse tree produced by TimelineParser#declaration.
    def exitDeclaration(self, ctx:TimelineParser.DeclarationContext):
        pass


    # Enter a parse tree produced by TimelineParser#eventDecl.
    def enterEventDecl(self, ctx:TimelineParser.EventDeclContext):
        pass

    # Exit a parse tree produced by TimelineParser#eventDecl.
    def exitEventDecl(self, ctx:TimelineParser.EventDeclContext):
        pass


    # Enter a parse tree produced by TimelineParser#periodDecl.
    def enterPeriodDecl(self, ctx:TimelineParser.PeriodDeclContext):
        pass

    # Exit a parse tree produced by TimelineParser#periodDecl.
    def exitPeriodDecl(self, ctx:TimelineParser.PeriodDeclContext):
        pass


    # Enter a parse tree produced by TimelineParser#timelineDecl.
    def enterTimelineDecl(self, ctx:TimelineParser.TimelineDeclContext):
        pass

    # Exit a parse tree produced by TimelineParser#timelineDecl.
    def exitTimelineDecl(self, ctx:TimelineParser.TimelineDeclContext):
        pass


    # Enter a parse tree produced by TimelineParser#componentList.
    def enterComponentList(self, ctx:TimelineParser.ComponentListContext):
        pass

    # Exit a parse tree produced by TimelineParser#componentList.
    def exitComponentList(self, ctx:TimelineParser.ComponentListContext):
        pass


    # Enter a parse tree produced by TimelineParser#relationshipDecl.
    def enterRelationshipDecl(self, ctx:TimelineParser.RelationshipDeclContext):
        pass

    # Exit a parse tree produced by TimelineParser#relationshipDecl.
    def exitRelationshipDecl(self, ctx:TimelineParser.RelationshipDeclContext):
        pass


    # Enter a parse tree produced by TimelineParser#dateExpr.
    def enterDateExpr(self, ctx:TimelineParser.DateExprContext):
        pass

    # Exit a parse tree produced by TimelineParser#dateExpr.
    def exitDateExpr(self, ctx:TimelineParser.DateExprContext):
        pass


    # Enter a parse tree produced by TimelineParser#dateCalculation.
    def enterDateCalculation(self, ctx:TimelineParser.DateCalculationContext):
        pass

    # Exit a parse tree produced by TimelineParser#dateCalculation.
    def exitDateCalculation(self, ctx:TimelineParser.DateCalculationContext):
        pass


    # Enter a parse tree produced by TimelineParser#yearLiteral.
    def enterYearLiteral(self, ctx:TimelineParser.YearLiteralContext):
        pass

    # Exit a parse tree produced by TimelineParser#yearLiteral.
    def exitYearLiteral(self, ctx:TimelineParser.YearLiteralContext):
        pass


    # Enter a parse tree produced by TimelineParser#monthYearLiteral.
    def enterMonthYearLiteral(self, ctx:TimelineParser.MonthYearLiteralContext):
        pass

    # Exit a parse tree produced by TimelineParser#monthYearLiteral.
    def exitMonthYearLiteral(self, ctx:TimelineParser.MonthYearLiteralContext):
        pass


    # Enter a parse tree produced by TimelineParser#fullDateLiteral.
    def enterFullDateLiteral(self, ctx:TimelineParser.FullDateLiteralContext):
        pass

    # Exit a parse tree produced by TimelineParser#fullDateLiteral.
    def exitFullDateLiteral(self, ctx:TimelineParser.FullDateLiteralContext):
        pass


    # Enter a parse tree produced by TimelineParser#importanceValue.
    def enterImportanceValue(self, ctx:TimelineParser.ImportanceValueContext):
        pass

    # Exit a parse tree produced by TimelineParser#importanceValue.
    def exitImportanceValue(self, ctx:TimelineParser.ImportanceValueContext):
        pass


    # Enter a parse tree produced by TimelineParser#relationshipType.
    def enterRelationshipType(self, ctx:TimelineParser.RelationshipTypeContext):
        pass

    # Exit a parse tree produced by TimelineParser#relationshipType.
    def exitRelationshipType(self, ctx:TimelineParser.RelationshipTypeContext):
        pass


    # Enter a parse tree produced by TimelineParser#mainBlock.
    def enterMainBlock(self, ctx:TimelineParser.MainBlockContext):
        pass

    # Exit a parse tree produced by TimelineParser#mainBlock.
    def exitMainBlock(self, ctx:TimelineParser.MainBlockContext):
        pass


    # Enter a parse tree produced by TimelineParser#statement.
    def enterStatement(self, ctx:TimelineParser.StatementContext):
        pass

    # Exit a parse tree produced by TimelineParser#statement.
    def exitStatement(self, ctx:TimelineParser.StatementContext):
        pass


    # Enter a parse tree produced by TimelineParser#exportStmt.
    def enterExportStmt(self, ctx:TimelineParser.ExportStmtContext):
        pass

    # Exit a parse tree produced by TimelineParser#exportStmt.
    def exitExportStmt(self, ctx:TimelineParser.ExportStmtContext):
        pass


    # Enter a parse tree produced by TimelineParser#ifStmt.
    def enterIfStmt(self, ctx:TimelineParser.IfStmtContext):
        pass

    # Exit a parse tree produced by TimelineParser#ifStmt.
    def exitIfStmt(self, ctx:TimelineParser.IfStmtContext):
        pass


    # Enter a parse tree produced by TimelineParser#condition.
    def enterCondition(self, ctx:TimelineParser.ConditionContext):
        pass

    # Exit a parse tree produced by TimelineParser#condition.
    def exitCondition(self, ctx:TimelineParser.ConditionContext):
        pass


    # Enter a parse tree produced by TimelineParser#comparisonOp.
    def enterComparisonOp(self, ctx:TimelineParser.ComparisonOpContext):
        pass

    # Exit a parse tree produced by TimelineParser#comparisonOp.
    def exitComparisonOp(self, ctx:TimelineParser.ComparisonOpContext):
        pass


    # Enter a parse tree produced by TimelineParser#expr.
    def enterExpr(self, ctx:TimelineParser.ExprContext):
        pass

    # Exit a parse tree produced by TimelineParser#expr.
    def exitExpr(self, ctx:TimelineParser.ExprContext):
        pass


    # Enter a parse tree produced by TimelineParser#property.
    def enterProperty(self, ctx:TimelineParser.PropertyContext):
        pass

    # Exit a parse tree produced by TimelineParser#property.
    def exitProperty(self, ctx:TimelineParser.PropertyContext):
        pass


    # Enter a parse tree produced by TimelineParser#forStmt.
    def enterForStmt(self, ctx:TimelineParser.ForStmtContext):
        pass

    # Exit a parse tree produced by TimelineParser#forStmt.
    def exitForStmt(self, ctx:TimelineParser.ForStmtContext):
        pass


    # Enter a parse tree produced by TimelineParser#modifyStmt.
    def enterModifyStmt(self, ctx:TimelineParser.ModifyStmtContext):
        pass

    # Exit a parse tree produced by TimelineParser#modifyStmt.
    def exitModifyStmt(self, ctx:TimelineParser.ModifyStmtContext):
        pass


    # Enter a parse tree produced by TimelineParser#propertyAssignment.
    def enterPropertyAssignment(self, ctx:TimelineParser.PropertyAssignmentContext):
        pass

    # Exit a parse tree produced by TimelineParser#propertyAssignment.
    def exitPropertyAssignment(self, ctx:TimelineParser.PropertyAssignmentContext):
        pass


    # Enter a parse tree produced by TimelineParser#booleanLiteral.
    def enterBooleanLiteral(self, ctx:TimelineParser.BooleanLiteralContext):
        pass

    # Exit a parse tree produced by TimelineParser#booleanLiteral.
    def exitBooleanLiteral(self, ctx:TimelineParser.BooleanLiteralContext):
        pass



del TimelineParser