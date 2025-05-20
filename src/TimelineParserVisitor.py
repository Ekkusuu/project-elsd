# Generated from TimelineParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .TimelineParser import TimelineParser
else:
    from TimelineParser import TimelineParser

# This class defines a complete generic visitor for a parse tree produced by TimelineParser.

class TimelineParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TimelineParser#program.
    def visitProgram(self, ctx:TimelineParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#declaration.
    def visitDeclaration(self, ctx:TimelineParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#eventDecl.
    def visitEventDecl(self, ctx:TimelineParser.EventDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#periodDecl.
    def visitPeriodDecl(self, ctx:TimelineParser.PeriodDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#timelineDecl.
    def visitTimelineDecl(self, ctx:TimelineParser.TimelineDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#componentList.
    def visitComponentList(self, ctx:TimelineParser.ComponentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#relationshipDecl.
    def visitRelationshipDecl(self, ctx:TimelineParser.RelationshipDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#dateExpr.
    def visitDateExpr(self, ctx:TimelineParser.DateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#dateCalculation.
    def visitDateCalculation(self, ctx:TimelineParser.DateCalculationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#yearLiteral.
    def visitYearLiteral(self, ctx:TimelineParser.YearLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#monthYearLiteral.
    def visitMonthYearLiteral(self, ctx:TimelineParser.MonthYearLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#fullDateLiteral.
    def visitFullDateLiteral(self, ctx:TimelineParser.FullDateLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#importanceValue.
    def visitImportanceValue(self, ctx:TimelineParser.ImportanceValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#relationshipType.
    def visitRelationshipType(self, ctx:TimelineParser.RelationshipTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#mainBlock.
    def visitMainBlock(self, ctx:TimelineParser.MainBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#statement.
    def visitStatement(self, ctx:TimelineParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#exportStmt.
    def visitExportStmt(self, ctx:TimelineParser.ExportStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#ifStmt.
    def visitIfStmt(self, ctx:TimelineParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#condition.
    def visitCondition(self, ctx:TimelineParser.ConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#comparisonOp.
    def visitComparisonOp(self, ctx:TimelineParser.ComparisonOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#expr.
    def visitExpr(self, ctx:TimelineParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#property.
    def visitProperty(self, ctx:TimelineParser.PropertyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#forStmt.
    def visitForStmt(self, ctx:TimelineParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#modifyStmt.
    def visitModifyStmt(self, ctx:TimelineParser.ModifyStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#propertyAssignment.
    def visitPropertyAssignment(self, ctx:TimelineParser.PropertyAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TimelineParser#booleanLiteral.
    def visitBooleanLiteral(self, ctx:TimelineParser.BooleanLiteralContext):
        return self.visitChildren(ctx)



del TimelineParser