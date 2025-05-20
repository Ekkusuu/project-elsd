# Generated from TimelineParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,55,275,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,1,0,5,0,54,
        8,0,10,0,12,0,57,9,0,1,0,3,0,60,8,0,1,0,1,0,1,1,1,1,1,1,1,1,3,1,
        68,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,3,2,86,8,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,
        1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,1,3,3,3,110,8,3,1,3,1,3,1,4,
        1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,5,5,127,8,5,10,5,
        12,5,130,9,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,1,6,
        1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,7,3,7,155,8,7,1,8,1,8,1,8,
        1,8,1,8,1,8,1,9,1,9,3,9,165,8,9,1,10,1,10,1,10,1,10,1,11,1,11,1,
        11,1,11,1,12,1,12,1,13,1,13,1,14,1,14,1,14,5,14,182,8,14,10,14,12,
        14,185,9,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,3,15,194,8,15,1,16,
        1,16,1,16,1,16,1,17,1,17,1,17,1,17,1,17,1,17,5,17,206,8,17,10,17,
        12,17,209,9,17,1,17,1,17,1,17,1,17,5,17,215,8,17,10,17,12,17,218,
        9,17,1,17,3,17,221,8,17,1,18,1,18,1,18,1,18,1,18,1,18,3,18,229,8,
        18,1,19,1,19,1,20,1,20,1,20,1,20,1,20,1,20,1,20,1,20,3,20,241,8,
        20,1,21,1,21,1,22,1,22,1,22,1,22,1,22,1,22,5,22,251,8,22,10,22,12,
        22,254,9,22,1,22,1,22,1,23,1,23,1,23,1,23,4,23,262,8,23,11,23,12,
        23,263,1,23,1,23,1,24,1,24,1,24,1,24,1,24,1,25,1,25,1,25,0,0,26,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        46,48,50,0,7,1,0,33,35,1,0,21,22,1,0,12,14,2,0,15,20,53,53,1,0,46,
        51,2,0,25,29,32,35,1,0,23,24,277,0,55,1,0,0,0,2,67,1,0,0,0,4,69,
        1,0,0,0,6,89,1,0,0,0,8,113,1,0,0,0,10,123,1,0,0,0,12,133,1,0,0,0,
        14,154,1,0,0,0,16,156,1,0,0,0,18,162,1,0,0,0,20,166,1,0,0,0,22,170,
        1,0,0,0,24,174,1,0,0,0,26,176,1,0,0,0,28,178,1,0,0,0,30,193,1,0,
        0,0,32,195,1,0,0,0,34,199,1,0,0,0,36,228,1,0,0,0,38,230,1,0,0,0,
        40,240,1,0,0,0,42,242,1,0,0,0,44,244,1,0,0,0,46,257,1,0,0,0,48,267,
        1,0,0,0,50,272,1,0,0,0,52,54,3,2,1,0,53,52,1,0,0,0,54,57,1,0,0,0,
        55,53,1,0,0,0,55,56,1,0,0,0,56,59,1,0,0,0,57,55,1,0,0,0,58,60,3,
        28,14,0,59,58,1,0,0,0,59,60,1,0,0,0,60,61,1,0,0,0,61,62,5,0,0,1,
        62,1,1,0,0,0,63,68,3,4,2,0,64,68,3,6,3,0,65,68,3,8,4,0,66,68,3,12,
        6,0,67,63,1,0,0,0,67,64,1,0,0,0,67,65,1,0,0,0,67,66,1,0,0,0,68,3,
        1,0,0,0,69,70,5,1,0,0,70,71,5,54,0,0,71,72,5,42,0,0,72,73,5,25,0,
        0,73,74,5,36,0,0,74,75,5,53,0,0,75,76,5,38,0,0,76,77,5,26,0,0,77,
        78,5,36,0,0,78,79,3,14,7,0,79,85,5,38,0,0,80,81,5,29,0,0,81,82,5,
        36,0,0,82,83,3,24,12,0,83,84,5,38,0,0,84,86,1,0,0,0,85,80,1,0,0,
        0,85,86,1,0,0,0,86,87,1,0,0,0,87,88,5,43,0,0,88,5,1,0,0,0,89,90,
        5,2,0,0,90,91,5,54,0,0,91,92,5,42,0,0,92,93,5,25,0,0,93,94,5,36,
        0,0,94,95,5,53,0,0,95,96,5,38,0,0,96,97,5,27,0,0,97,98,5,36,0,0,
        98,99,3,14,7,0,99,100,5,38,0,0,100,101,5,28,0,0,101,102,5,36,0,0,
        102,103,3,14,7,0,103,109,5,38,0,0,104,105,5,29,0,0,105,106,5,36,
        0,0,106,107,3,24,12,0,107,108,5,38,0,0,108,110,1,0,0,0,109,104,1,
        0,0,0,109,110,1,0,0,0,110,111,1,0,0,0,111,112,5,43,0,0,112,7,1,0,
        0,0,113,114,5,3,0,0,114,115,5,54,0,0,115,116,5,42,0,0,116,117,5,
        25,0,0,117,118,5,36,0,0,118,119,5,53,0,0,119,120,5,38,0,0,120,121,
        3,10,5,0,121,122,5,43,0,0,122,9,1,0,0,0,123,128,5,54,0,0,124,125,
        5,37,0,0,125,127,5,54,0,0,126,124,1,0,0,0,127,130,1,0,0,0,128,126,
        1,0,0,0,128,129,1,0,0,0,129,131,1,0,0,0,130,128,1,0,0,0,131,132,
        5,38,0,0,132,11,1,0,0,0,133,134,5,4,0,0,134,135,5,54,0,0,135,136,
        5,42,0,0,136,137,5,30,0,0,137,138,5,36,0,0,138,139,5,54,0,0,139,
        140,5,38,0,0,140,141,5,31,0,0,141,142,5,36,0,0,142,143,5,54,0,0,
        143,144,5,38,0,0,144,145,5,32,0,0,145,146,5,36,0,0,146,147,3,26,
        13,0,147,148,5,38,0,0,148,149,5,43,0,0,149,13,1,0,0,0,150,155,3,
        22,11,0,151,155,3,20,10,0,152,155,3,18,9,0,153,155,3,16,8,0,154,
        150,1,0,0,0,154,151,1,0,0,0,154,152,1,0,0,0,154,153,1,0,0,0,155,
        15,1,0,0,0,156,157,5,54,0,0,157,158,5,39,0,0,158,159,7,0,0,0,159,
        160,5,45,0,0,160,161,5,52,0,0,161,17,1,0,0,0,162,164,5,52,0,0,163,
        165,7,1,0,0,164,163,1,0,0,0,164,165,1,0,0,0,165,19,1,0,0,0,166,167,
        5,52,0,0,167,168,5,44,0,0,168,169,3,18,9,0,169,21,1,0,0,0,170,171,
        5,52,0,0,171,172,5,44,0,0,172,173,3,20,10,0,173,23,1,0,0,0,174,175,
        7,2,0,0,175,25,1,0,0,0,176,177,7,3,0,0,177,27,1,0,0,0,178,179,5,
        5,0,0,179,183,5,42,0,0,180,182,3,30,15,0,181,180,1,0,0,0,182,185,
        1,0,0,0,183,181,1,0,0,0,183,184,1,0,0,0,184,186,1,0,0,0,185,183,
        1,0,0,0,186,187,5,43,0,0,187,29,1,0,0,0,188,194,3,32,16,0,189,194,
        3,34,17,0,190,194,3,44,22,0,191,194,3,46,23,0,192,194,5,38,0,0,193,
        188,1,0,0,0,193,189,1,0,0,0,193,190,1,0,0,0,193,191,1,0,0,0,193,
        192,1,0,0,0,194,31,1,0,0,0,195,196,5,6,0,0,196,197,5,54,0,0,197,
        198,5,38,0,0,198,33,1,0,0,0,199,200,5,7,0,0,200,201,5,40,0,0,201,
        202,3,36,18,0,202,203,5,41,0,0,203,207,5,42,0,0,204,206,3,30,15,
        0,205,204,1,0,0,0,206,209,1,0,0,0,207,205,1,0,0,0,207,208,1,0,0,
        0,208,210,1,0,0,0,209,207,1,0,0,0,210,220,5,43,0,0,211,212,5,8,0,
        0,212,216,5,42,0,0,213,215,3,30,15,0,214,213,1,0,0,0,215,218,1,0,
        0,0,216,214,1,0,0,0,216,217,1,0,0,0,217,219,1,0,0,0,218,216,1,0,
        0,0,219,221,5,43,0,0,220,211,1,0,0,0,220,221,1,0,0,0,221,35,1,0,
        0,0,222,223,3,40,20,0,223,224,3,38,19,0,224,225,3,40,20,0,225,229,
        1,0,0,0,226,229,5,54,0,0,227,229,3,50,25,0,228,222,1,0,0,0,228,226,
        1,0,0,0,228,227,1,0,0,0,229,37,1,0,0,0,230,231,7,4,0,0,231,39,1,
        0,0,0,232,241,5,54,0,0,233,241,5,53,0,0,234,241,3,14,7,0,235,241,
        5,52,0,0,236,237,5,54,0,0,237,238,5,39,0,0,238,241,3,42,21,0,239,
        241,3,24,12,0,240,232,1,0,0,0,240,233,1,0,0,0,240,234,1,0,0,0,240,
        235,1,0,0,0,240,236,1,0,0,0,240,239,1,0,0,0,241,41,1,0,0,0,242,243,
        7,5,0,0,243,43,1,0,0,0,244,245,5,9,0,0,245,246,5,54,0,0,246,247,
        5,10,0,0,247,248,5,54,0,0,248,252,5,42,0,0,249,251,3,30,15,0,250,
        249,1,0,0,0,251,254,1,0,0,0,252,250,1,0,0,0,252,253,1,0,0,0,253,
        255,1,0,0,0,254,252,1,0,0,0,255,256,5,43,0,0,256,45,1,0,0,0,257,
        258,5,11,0,0,258,259,5,54,0,0,259,261,5,42,0,0,260,262,3,48,24,0,
        261,260,1,0,0,0,262,263,1,0,0,0,263,261,1,0,0,0,263,264,1,0,0,0,
        264,265,1,0,0,0,265,266,5,43,0,0,266,47,1,0,0,0,267,268,3,42,21,
        0,268,269,5,36,0,0,269,270,3,40,20,0,270,271,5,38,0,0,271,49,1,0,
        0,0,272,273,7,6,0,0,273,51,1,0,0,0,17,55,59,67,85,109,128,154,164,
        183,193,207,216,220,228,240,252,263
    ]

class TimelineParser ( Parser ):

    grammarFileName = "TimelineParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'event'", "'period'", "'timeline'", "'relationship'", 
                     "'main'", "'export'", "'if'", "'else'", "'for'", "'in'", 
                     "'modify'", "'high'", "'medium'", "'low'", "'cause-effect'", 
                     "'contemporaneous'", "'precedes'", "'follows'", "'includes'", 
                     "'excludes'", "'BCE'", "'CE'", "'true'", "'false'", 
                     "'title'", "'date'", "'start'", "'end'", "'importance'", 
                     "'from'", "'to'", "'type'", "'year'", "'month'", "'day'", 
                     "'='", "','", "';'", "'.'", "'('", "')'", "'{'", "'}'", 
                     "'-'", "<INVALID>", "'<'", "'>'", "'<='", "'>='", "'=='", 
                     "'!='" ]

    symbolicNames = [ "<INVALID>", "EVENT", "PERIOD", "TIMELINE", "RELATIONSHIP", 
                      "MAIN", "EXPORT", "IF", "ELSE", "FOR", "IN", "MODIFY", 
                      "HIGH", "MEDIUM", "LOW", "CAUSE_EFFECT", "CONTEMPORANEOUS", 
                      "PRECEDES", "FOLLOWS", "INCLUDES", "EXCLUDES", "BCE", 
                      "CE", "TRUE", "FALSE", "TITLE", "DATE", "START", "END", 
                      "IMPORTANCE", "FROM", "TO", "TYPE", "YEAR", "MONTH", 
                      "DAY", "EQ", "COMMA", "SEMI", "DOT", "LPAREN", "RPAREN", 
                      "LCURLY", "RCURLY", "DASH", "ADD_OP", "LT", "GT", 
                      "LE", "GE", "EQ_EQ", "NEQ", "INT", "STRING", "ID", 
                      "WS" ]

    RULE_program = 0
    RULE_declaration = 1
    RULE_eventDecl = 2
    RULE_periodDecl = 3
    RULE_timelineDecl = 4
    RULE_componentList = 5
    RULE_relationshipDecl = 6
    RULE_dateExpr = 7
    RULE_dateCalculation = 8
    RULE_yearLiteral = 9
    RULE_monthYearLiteral = 10
    RULE_fullDateLiteral = 11
    RULE_importanceValue = 12
    RULE_relationshipType = 13
    RULE_mainBlock = 14
    RULE_statement = 15
    RULE_exportStmt = 16
    RULE_ifStmt = 17
    RULE_condition = 18
    RULE_comparisonOp = 19
    RULE_expr = 20
    RULE_property = 21
    RULE_forStmt = 22
    RULE_modifyStmt = 23
    RULE_propertyAssignment = 24
    RULE_booleanLiteral = 25

    ruleNames =  [ "program", "declaration", "eventDecl", "periodDecl", 
                   "timelineDecl", "componentList", "relationshipDecl", 
                   "dateExpr", "dateCalculation", "yearLiteral", "monthYearLiteral", 
                   "fullDateLiteral", "importanceValue", "relationshipType", 
                   "mainBlock", "statement", "exportStmt", "ifStmt", "condition", 
                   "comparisonOp", "expr", "property", "forStmt", "modifyStmt", 
                   "propertyAssignment", "booleanLiteral" ]

    EOF = Token.EOF
    EVENT=1
    PERIOD=2
    TIMELINE=3
    RELATIONSHIP=4
    MAIN=5
    EXPORT=6
    IF=7
    ELSE=8
    FOR=9
    IN=10
    MODIFY=11
    HIGH=12
    MEDIUM=13
    LOW=14
    CAUSE_EFFECT=15
    CONTEMPORANEOUS=16
    PRECEDES=17
    FOLLOWS=18
    INCLUDES=19
    EXCLUDES=20
    BCE=21
    CE=22
    TRUE=23
    FALSE=24
    TITLE=25
    DATE=26
    START=27
    END=28
    IMPORTANCE=29
    FROM=30
    TO=31
    TYPE=32
    YEAR=33
    MONTH=34
    DAY=35
    EQ=36
    COMMA=37
    SEMI=38
    DOT=39
    LPAREN=40
    RPAREN=41
    LCURLY=42
    RCURLY=43
    DASH=44
    ADD_OP=45
    LT=46
    GT=47
    LE=48
    GE=49
    EQ_EQ=50
    NEQ=51
    INT=52
    STRING=53
    ID=54
    WS=55

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(TimelineParser.EOF, 0)

        def declaration(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.DeclarationContext)
            else:
                return self.getTypedRuleContext(TimelineParser.DeclarationContext,i)


        def mainBlock(self):
            return self.getTypedRuleContext(TimelineParser.MainBlockContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_program

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProgram" ):
                listener.enterProgram(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProgram" ):
                listener.exitProgram(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProgram" ):
                return visitor.visitProgram(self)
            else:
                return visitor.visitChildren(self)




    def program(self):

        localctx = TimelineParser.ProgramContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_program)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 55
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 30) != 0):
                self.state = 52
                self.declaration()
                self.state = 57
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 59
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==5:
                self.state = 58
                self.mainBlock()


            self.state = 61
            self.match(TimelineParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclarationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def eventDecl(self):
            return self.getTypedRuleContext(TimelineParser.EventDeclContext,0)


        def periodDecl(self):
            return self.getTypedRuleContext(TimelineParser.PeriodDeclContext,0)


        def timelineDecl(self):
            return self.getTypedRuleContext(TimelineParser.TimelineDeclContext,0)


        def relationshipDecl(self):
            return self.getTypedRuleContext(TimelineParser.RelationshipDeclContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_declaration

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaration" ):
                listener.enterDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaration" ):
                listener.exitDeclaration(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDeclaration" ):
                return visitor.visitDeclaration(self)
            else:
                return visitor.visitChildren(self)




    def declaration(self):

        localctx = TimelineParser.DeclarationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_declaration)
        try:
            self.state = 67
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 63
                self.eventDecl()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 64
                self.periodDecl()
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 3)
                self.state = 65
                self.timelineDecl()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 4)
                self.state = 66
                self.relationshipDecl()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class EventDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EVENT(self):
            return self.getToken(TimelineParser.EVENT, 0)

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def TITLE(self):
            return self.getToken(TimelineParser.TITLE, 0)

        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.EQ)
            else:
                return self.getToken(TimelineParser.EQ, i)

        def STRING(self):
            return self.getToken(TimelineParser.STRING, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.SEMI)
            else:
                return self.getToken(TimelineParser.SEMI, i)

        def DATE(self):
            return self.getToken(TimelineParser.DATE, 0)

        def dateExpr(self):
            return self.getTypedRuleContext(TimelineParser.DateExprContext,0)


        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def IMPORTANCE(self):
            return self.getToken(TimelineParser.IMPORTANCE, 0)

        def importanceValue(self):
            return self.getTypedRuleContext(TimelineParser.ImportanceValueContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_eventDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEventDecl" ):
                listener.enterEventDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEventDecl" ):
                listener.exitEventDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEventDecl" ):
                return visitor.visitEventDecl(self)
            else:
                return visitor.visitChildren(self)




    def eventDecl(self):

        localctx = TimelineParser.EventDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_eventDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(TimelineParser.EVENT)
            self.state = 70
            self.match(TimelineParser.ID)
            self.state = 71
            self.match(TimelineParser.LCURLY)
            self.state = 72
            self.match(TimelineParser.TITLE)
            self.state = 73
            self.match(TimelineParser.EQ)
            self.state = 74
            self.match(TimelineParser.STRING)
            self.state = 75
            self.match(TimelineParser.SEMI)
            self.state = 76
            self.match(TimelineParser.DATE)
            self.state = 77
            self.match(TimelineParser.EQ)
            self.state = 78
            self.dateExpr()
            self.state = 79
            self.match(TimelineParser.SEMI)
            self.state = 85
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==29:
                self.state = 80
                self.match(TimelineParser.IMPORTANCE)
                self.state = 81
                self.match(TimelineParser.EQ)
                self.state = 82
                self.importanceValue()
                self.state = 83
                self.match(TimelineParser.SEMI)


            self.state = 87
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PeriodDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PERIOD(self):
            return self.getToken(TimelineParser.PERIOD, 0)

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def TITLE(self):
            return self.getToken(TimelineParser.TITLE, 0)

        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.EQ)
            else:
                return self.getToken(TimelineParser.EQ, i)

        def STRING(self):
            return self.getToken(TimelineParser.STRING, 0)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.SEMI)
            else:
                return self.getToken(TimelineParser.SEMI, i)

        def START(self):
            return self.getToken(TimelineParser.START, 0)

        def dateExpr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.DateExprContext)
            else:
                return self.getTypedRuleContext(TimelineParser.DateExprContext,i)


        def END(self):
            return self.getToken(TimelineParser.END, 0)

        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def IMPORTANCE(self):
            return self.getToken(TimelineParser.IMPORTANCE, 0)

        def importanceValue(self):
            return self.getTypedRuleContext(TimelineParser.ImportanceValueContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_periodDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPeriodDecl" ):
                listener.enterPeriodDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPeriodDecl" ):
                listener.exitPeriodDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPeriodDecl" ):
                return visitor.visitPeriodDecl(self)
            else:
                return visitor.visitChildren(self)




    def periodDecl(self):

        localctx = TimelineParser.PeriodDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_periodDecl)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 89
            self.match(TimelineParser.PERIOD)
            self.state = 90
            self.match(TimelineParser.ID)
            self.state = 91
            self.match(TimelineParser.LCURLY)
            self.state = 92
            self.match(TimelineParser.TITLE)
            self.state = 93
            self.match(TimelineParser.EQ)
            self.state = 94
            self.match(TimelineParser.STRING)
            self.state = 95
            self.match(TimelineParser.SEMI)
            self.state = 96
            self.match(TimelineParser.START)
            self.state = 97
            self.match(TimelineParser.EQ)
            self.state = 98
            self.dateExpr()
            self.state = 99
            self.match(TimelineParser.SEMI)
            self.state = 100
            self.match(TimelineParser.END)
            self.state = 101
            self.match(TimelineParser.EQ)
            self.state = 102
            self.dateExpr()
            self.state = 103
            self.match(TimelineParser.SEMI)
            self.state = 109
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==29:
                self.state = 104
                self.match(TimelineParser.IMPORTANCE)
                self.state = 105
                self.match(TimelineParser.EQ)
                self.state = 106
                self.importanceValue()
                self.state = 107
                self.match(TimelineParser.SEMI)


            self.state = 111
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TimelineDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TIMELINE(self):
            return self.getToken(TimelineParser.TIMELINE, 0)

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def TITLE(self):
            return self.getToken(TimelineParser.TITLE, 0)

        def EQ(self):
            return self.getToken(TimelineParser.EQ, 0)

        def STRING(self):
            return self.getToken(TimelineParser.STRING, 0)

        def SEMI(self):
            return self.getToken(TimelineParser.SEMI, 0)

        def componentList(self):
            return self.getTypedRuleContext(TimelineParser.ComponentListContext,0)


        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_timelineDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTimelineDecl" ):
                listener.enterTimelineDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTimelineDecl" ):
                listener.exitTimelineDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTimelineDecl" ):
                return visitor.visitTimelineDecl(self)
            else:
                return visitor.visitChildren(self)




    def timelineDecl(self):

        localctx = TimelineParser.TimelineDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_timelineDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(TimelineParser.TIMELINE)
            self.state = 114
            self.match(TimelineParser.ID)
            self.state = 115
            self.match(TimelineParser.LCURLY)
            self.state = 116
            self.match(TimelineParser.TITLE)
            self.state = 117
            self.match(TimelineParser.EQ)
            self.state = 118
            self.match(TimelineParser.STRING)
            self.state = 119
            self.match(TimelineParser.SEMI)
            self.state = 120
            self.componentList()
            self.state = 121
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComponentListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.ID)
            else:
                return self.getToken(TimelineParser.ID, i)

        def SEMI(self):
            return self.getToken(TimelineParser.SEMI, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.COMMA)
            else:
                return self.getToken(TimelineParser.COMMA, i)

        def getRuleIndex(self):
            return TimelineParser.RULE_componentList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComponentList" ):
                listener.enterComponentList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComponentList" ):
                listener.exitComponentList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComponentList" ):
                return visitor.visitComponentList(self)
            else:
                return visitor.visitChildren(self)




    def componentList(self):

        localctx = TimelineParser.ComponentListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_componentList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(TimelineParser.ID)
            self.state = 128
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==37:
                self.state = 124
                self.match(TimelineParser.COMMA)
                self.state = 125
                self.match(TimelineParser.ID)
                self.state = 130
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 131
            self.match(TimelineParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationshipDeclContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RELATIONSHIP(self):
            return self.getToken(TimelineParser.RELATIONSHIP, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.ID)
            else:
                return self.getToken(TimelineParser.ID, i)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def FROM(self):
            return self.getToken(TimelineParser.FROM, 0)

        def EQ(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.EQ)
            else:
                return self.getToken(TimelineParser.EQ, i)

        def SEMI(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.SEMI)
            else:
                return self.getToken(TimelineParser.SEMI, i)

        def TO(self):
            return self.getToken(TimelineParser.TO, 0)

        def TYPE(self):
            return self.getToken(TimelineParser.TYPE, 0)

        def relationshipType(self):
            return self.getTypedRuleContext(TimelineParser.RelationshipTypeContext,0)


        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_relationshipDecl

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationshipDecl" ):
                listener.enterRelationshipDecl(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationshipDecl" ):
                listener.exitRelationshipDecl(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationshipDecl" ):
                return visitor.visitRelationshipDecl(self)
            else:
                return visitor.visitChildren(self)




    def relationshipDecl(self):

        localctx = TimelineParser.RelationshipDeclContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_relationshipDecl)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 133
            self.match(TimelineParser.RELATIONSHIP)
            self.state = 134
            self.match(TimelineParser.ID)
            self.state = 135
            self.match(TimelineParser.LCURLY)
            self.state = 136
            self.match(TimelineParser.FROM)
            self.state = 137
            self.match(TimelineParser.EQ)
            self.state = 138
            self.match(TimelineParser.ID)
            self.state = 139
            self.match(TimelineParser.SEMI)
            self.state = 140
            self.match(TimelineParser.TO)
            self.state = 141
            self.match(TimelineParser.EQ)
            self.state = 142
            self.match(TimelineParser.ID)
            self.state = 143
            self.match(TimelineParser.SEMI)
            self.state = 144
            self.match(TimelineParser.TYPE)
            self.state = 145
            self.match(TimelineParser.EQ)
            self.state = 146
            self.relationshipType()
            self.state = 147
            self.match(TimelineParser.SEMI)
            self.state = 148
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def fullDateLiteral(self):
            return self.getTypedRuleContext(TimelineParser.FullDateLiteralContext,0)


        def monthYearLiteral(self):
            return self.getTypedRuleContext(TimelineParser.MonthYearLiteralContext,0)


        def yearLiteral(self):
            return self.getTypedRuleContext(TimelineParser.YearLiteralContext,0)


        def dateCalculation(self):
            return self.getTypedRuleContext(TimelineParser.DateCalculationContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_dateExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateExpr" ):
                listener.enterDateExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateExpr" ):
                listener.exitDateExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDateExpr" ):
                return visitor.visitDateExpr(self)
            else:
                return visitor.visitChildren(self)




    def dateExpr(self):

        localctx = TimelineParser.DateExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_dateExpr)
        try:
            self.state = 154
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 150
                self.fullDateLiteral()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 151
                self.monthYearLiteral()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 152
                self.yearLiteral()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 153
                self.dateCalculation()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DateCalculationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def DOT(self):
            return self.getToken(TimelineParser.DOT, 0)

        def ADD_OP(self):
            return self.getToken(TimelineParser.ADD_OP, 0)

        def INT(self):
            return self.getToken(TimelineParser.INT, 0)

        def YEAR(self):
            return self.getToken(TimelineParser.YEAR, 0)

        def MONTH(self):
            return self.getToken(TimelineParser.MONTH, 0)

        def DAY(self):
            return self.getToken(TimelineParser.DAY, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_dateCalculation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDateCalculation" ):
                listener.enterDateCalculation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDateCalculation" ):
                listener.exitDateCalculation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitDateCalculation" ):
                return visitor.visitDateCalculation(self)
            else:
                return visitor.visitChildren(self)




    def dateCalculation(self):

        localctx = TimelineParser.DateCalculationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_dateCalculation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 156
            self.match(TimelineParser.ID)
            self.state = 157
            self.match(TimelineParser.DOT)
            self.state = 158
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 60129542144) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 159
            self.match(TimelineParser.ADD_OP)
            self.state = 160
            self.match(TimelineParser.INT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class YearLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(TimelineParser.INT, 0)

        def BCE(self):
            return self.getToken(TimelineParser.BCE, 0)

        def CE(self):
            return self.getToken(TimelineParser.CE, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_yearLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterYearLiteral" ):
                listener.enterYearLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitYearLiteral" ):
                listener.exitYearLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitYearLiteral" ):
                return visitor.visitYearLiteral(self)
            else:
                return visitor.visitChildren(self)




    def yearLiteral(self):

        localctx = TimelineParser.YearLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_yearLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 162
            self.match(TimelineParser.INT)
            self.state = 164
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==21 or _la==22:
                self.state = 163
                _la = self._input.LA(1)
                if not(_la==21 or _la==22):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MonthYearLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(TimelineParser.INT, 0)

        def DASH(self):
            return self.getToken(TimelineParser.DASH, 0)

        def yearLiteral(self):
            return self.getTypedRuleContext(TimelineParser.YearLiteralContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_monthYearLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMonthYearLiteral" ):
                listener.enterMonthYearLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMonthYearLiteral" ):
                listener.exitMonthYearLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMonthYearLiteral" ):
                return visitor.visitMonthYearLiteral(self)
            else:
                return visitor.visitChildren(self)




    def monthYearLiteral(self):

        localctx = TimelineParser.MonthYearLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_monthYearLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 166
            self.match(TimelineParser.INT)
            self.state = 167
            self.match(TimelineParser.DASH)
            self.state = 168
            self.yearLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FullDateLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(TimelineParser.INT, 0)

        def DASH(self):
            return self.getToken(TimelineParser.DASH, 0)

        def monthYearLiteral(self):
            return self.getTypedRuleContext(TimelineParser.MonthYearLiteralContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_fullDateLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFullDateLiteral" ):
                listener.enterFullDateLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFullDateLiteral" ):
                listener.exitFullDateLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFullDateLiteral" ):
                return visitor.visitFullDateLiteral(self)
            else:
                return visitor.visitChildren(self)




    def fullDateLiteral(self):

        localctx = TimelineParser.FullDateLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_fullDateLiteral)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self.match(TimelineParser.INT)
            self.state = 171
            self.match(TimelineParser.DASH)
            self.state = 172
            self.monthYearLiteral()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ImportanceValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def HIGH(self):
            return self.getToken(TimelineParser.HIGH, 0)

        def MEDIUM(self):
            return self.getToken(TimelineParser.MEDIUM, 0)

        def LOW(self):
            return self.getToken(TimelineParser.LOW, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_importanceValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterImportanceValue" ):
                listener.enterImportanceValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitImportanceValue" ):
                listener.exitImportanceValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImportanceValue" ):
                return visitor.visitImportanceValue(self)
            else:
                return visitor.visitChildren(self)




    def importanceValue(self):

        localctx = TimelineParser.ImportanceValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_importanceValue)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 174
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 28672) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationshipTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def CAUSE_EFFECT(self):
            return self.getToken(TimelineParser.CAUSE_EFFECT, 0)

        def CONTEMPORANEOUS(self):
            return self.getToken(TimelineParser.CONTEMPORANEOUS, 0)

        def PRECEDES(self):
            return self.getToken(TimelineParser.PRECEDES, 0)

        def FOLLOWS(self):
            return self.getToken(TimelineParser.FOLLOWS, 0)

        def INCLUDES(self):
            return self.getToken(TimelineParser.INCLUDES, 0)

        def EXCLUDES(self):
            return self.getToken(TimelineParser.EXCLUDES, 0)

        def STRING(self):
            return self.getToken(TimelineParser.STRING, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_relationshipType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationshipType" ):
                listener.enterRelationshipType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationshipType" ):
                listener.exitRelationshipType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRelationshipType" ):
                return visitor.visitRelationshipType(self)
            else:
                return visitor.visitChildren(self)




    def relationshipType(self):

        localctx = TimelineParser.RelationshipTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_relationshipType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 176
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 9007199256805376) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MainBlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MAIN(self):
            return self.getToken(TimelineParser.MAIN, 0)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.StatementContext)
            else:
                return self.getTypedRuleContext(TimelineParser.StatementContext,i)


        def getRuleIndex(self):
            return TimelineParser.RULE_mainBlock

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMainBlock" ):
                listener.enterMainBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMainBlock" ):
                listener.exitMainBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitMainBlock" ):
                return visitor.visitMainBlock(self)
            else:
                return visitor.visitChildren(self)




    def mainBlock(self):

        localctx = TimelineParser.MainBlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_mainBlock)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 178
            self.match(TimelineParser.MAIN)
            self.state = 179
            self.match(TimelineParser.LCURLY)
            self.state = 183
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 274877909696) != 0):
                self.state = 180
                self.statement()
                self.state = 185
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 186
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StatementContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def exportStmt(self):
            return self.getTypedRuleContext(TimelineParser.ExportStmtContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(TimelineParser.IfStmtContext,0)


        def forStmt(self):
            return self.getTypedRuleContext(TimelineParser.ForStmtContext,0)


        def modifyStmt(self):
            return self.getTypedRuleContext(TimelineParser.ModifyStmtContext,0)


        def SEMI(self):
            return self.getToken(TimelineParser.SEMI, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_statement

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStatement" ):
                listener.enterStatement(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStatement" ):
                listener.exitStatement(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStatement" ):
                return visitor.visitStatement(self)
            else:
                return visitor.visitChildren(self)




    def statement(self):

        localctx = TimelineParser.StatementContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_statement)
        try:
            self.state = 193
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 188
                self.exportStmt()
                pass
            elif token in [7]:
                self.enterOuterAlt(localctx, 2)
                self.state = 189
                self.ifStmt()
                pass
            elif token in [9]:
                self.enterOuterAlt(localctx, 3)
                self.state = 190
                self.forStmt()
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 4)
                self.state = 191
                self.modifyStmt()
                pass
            elif token in [38]:
                self.enterOuterAlt(localctx, 5)
                self.state = 192
                self.match(TimelineParser.SEMI)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExportStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EXPORT(self):
            return self.getToken(TimelineParser.EXPORT, 0)

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def SEMI(self):
            return self.getToken(TimelineParser.SEMI, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_exportStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExportStmt" ):
                listener.enterExportStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExportStmt" ):
                listener.exitExportStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExportStmt" ):
                return visitor.visitExportStmt(self)
            else:
                return visitor.visitChildren(self)




    def exportStmt(self):

        localctx = TimelineParser.ExportStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_exportStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 195
            self.match(TimelineParser.EXPORT)
            self.state = 196
            self.match(TimelineParser.ID)
            self.state = 197
            self.match(TimelineParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(TimelineParser.IF, 0)

        def LPAREN(self):
            return self.getToken(TimelineParser.LPAREN, 0)

        def condition(self):
            return self.getTypedRuleContext(TimelineParser.ConditionContext,0)


        def RPAREN(self):
            return self.getToken(TimelineParser.RPAREN, 0)

        def LCURLY(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.LCURLY)
            else:
                return self.getToken(TimelineParser.LCURLY, i)

        def RCURLY(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.RCURLY)
            else:
                return self.getToken(TimelineParser.RCURLY, i)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.StatementContext)
            else:
                return self.getTypedRuleContext(TimelineParser.StatementContext,i)


        def ELSE(self):
            return self.getToken(TimelineParser.ELSE, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIfStmt" ):
                return visitor.visitIfStmt(self)
            else:
                return visitor.visitChildren(self)




    def ifStmt(self):

        localctx = TimelineParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_ifStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 199
            self.match(TimelineParser.IF)
            self.state = 200
            self.match(TimelineParser.LPAREN)
            self.state = 201
            self.condition()
            self.state = 202
            self.match(TimelineParser.RPAREN)
            self.state = 203
            self.match(TimelineParser.LCURLY)
            self.state = 207
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 274877909696) != 0):
                self.state = 204
                self.statement()
                self.state = 209
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 210
            self.match(TimelineParser.RCURLY)
            self.state = 220
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==8:
                self.state = 211
                self.match(TimelineParser.ELSE)
                self.state = 212
                self.match(TimelineParser.LCURLY)
                self.state = 216
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 274877909696) != 0):
                    self.state = 213
                    self.statement()
                    self.state = 218
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 219
                self.match(TimelineParser.RCURLY)


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ConditionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.ExprContext)
            else:
                return self.getTypedRuleContext(TimelineParser.ExprContext,i)


        def comparisonOp(self):
            return self.getTypedRuleContext(TimelineParser.ComparisonOpContext,0)


        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def booleanLiteral(self):
            return self.getTypedRuleContext(TimelineParser.BooleanLiteralContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_condition

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCondition" ):
                listener.enterCondition(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCondition" ):
                listener.exitCondition(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCondition" ):
                return visitor.visitCondition(self)
            else:
                return visitor.visitChildren(self)




    def condition(self):

        localctx = TimelineParser.ConditionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_condition)
        try:
            self.state = 228
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,13,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 222
                self.expr()
                self.state = 223
                self.comparisonOp()
                self.state = 224
                self.expr()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 226
                self.match(TimelineParser.ID)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 227
                self.booleanLiteral()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ_EQ(self):
            return self.getToken(TimelineParser.EQ_EQ, 0)

        def NEQ(self):
            return self.getToken(TimelineParser.NEQ, 0)

        def LT(self):
            return self.getToken(TimelineParser.LT, 0)

        def GT(self):
            return self.getToken(TimelineParser.GT, 0)

        def LE(self):
            return self.getToken(TimelineParser.LE, 0)

        def GE(self):
            return self.getToken(TimelineParser.GE, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_comparisonOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparisonOp" ):
                listener.enterComparisonOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparisonOp" ):
                listener.exitComparisonOp(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparisonOp" ):
                return visitor.visitComparisonOp(self)
            else:
                return visitor.visitChildren(self)




    def comparisonOp(self):

        localctx = TimelineParser.ComparisonOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_comparisonOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 230
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4433230883192832) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def STRING(self):
            return self.getToken(TimelineParser.STRING, 0)

        def dateExpr(self):
            return self.getTypedRuleContext(TimelineParser.DateExprContext,0)


        def INT(self):
            return self.getToken(TimelineParser.INT, 0)

        def DOT(self):
            return self.getToken(TimelineParser.DOT, 0)

        def property_(self):
            return self.getTypedRuleContext(TimelineParser.PropertyContext,0)


        def importanceValue(self):
            return self.getTypedRuleContext(TimelineParser.ImportanceValueContext,0)


        def getRuleIndex(self):
            return TimelineParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = TimelineParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_expr)
        try:
            self.state = 240
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 232
                self.match(TimelineParser.ID)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 233
                self.match(TimelineParser.STRING)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 234
                self.dateExpr()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 235
                self.match(TimelineParser.INT)
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 236
                self.match(TimelineParser.ID)
                self.state = 237
                self.match(TimelineParser.DOT)
                self.state = 238
                self.property_()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 239
                self.importanceValue()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TITLE(self):
            return self.getToken(TimelineParser.TITLE, 0)

        def DATE(self):
            return self.getToken(TimelineParser.DATE, 0)

        def START(self):
            return self.getToken(TimelineParser.START, 0)

        def END(self):
            return self.getToken(TimelineParser.END, 0)

        def IMPORTANCE(self):
            return self.getToken(TimelineParser.IMPORTANCE, 0)

        def TYPE(self):
            return self.getToken(TimelineParser.TYPE, 0)

        def YEAR(self):
            return self.getToken(TimelineParser.YEAR, 0)

        def MONTH(self):
            return self.getToken(TimelineParser.MONTH, 0)

        def DAY(self):
            return self.getToken(TimelineParser.DAY, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_property

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProperty" ):
                listener.enterProperty(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProperty" ):
                listener.exitProperty(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProperty" ):
                return visitor.visitProperty(self)
            else:
                return visitor.visitChildren(self)




    def property_(self):

        localctx = TimelineParser.PropertyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_property)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 242
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 65464696832) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FOR(self):
            return self.getToken(TimelineParser.FOR, 0)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(TimelineParser.ID)
            else:
                return self.getToken(TimelineParser.ID, i)

        def IN(self):
            return self.getToken(TimelineParser.IN, 0)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def statement(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.StatementContext)
            else:
                return self.getTypedRuleContext(TimelineParser.StatementContext,i)


        def getRuleIndex(self):
            return TimelineParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitForStmt" ):
                return visitor.visitForStmt(self)
            else:
                return visitor.visitChildren(self)




    def forStmt(self):

        localctx = TimelineParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_forStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 244
            self.match(TimelineParser.FOR)
            self.state = 245
            self.match(TimelineParser.ID)
            self.state = 246
            self.match(TimelineParser.IN)
            self.state = 247
            self.match(TimelineParser.ID)
            self.state = 248
            self.match(TimelineParser.LCURLY)
            self.state = 252
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 274877909696) != 0):
                self.state = 249
                self.statement()
                self.state = 254
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 255
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ModifyStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def MODIFY(self):
            return self.getToken(TimelineParser.MODIFY, 0)

        def ID(self):
            return self.getToken(TimelineParser.ID, 0)

        def LCURLY(self):
            return self.getToken(TimelineParser.LCURLY, 0)

        def RCURLY(self):
            return self.getToken(TimelineParser.RCURLY, 0)

        def propertyAssignment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TimelineParser.PropertyAssignmentContext)
            else:
                return self.getTypedRuleContext(TimelineParser.PropertyAssignmentContext,i)


        def getRuleIndex(self):
            return TimelineParser.RULE_modifyStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterModifyStmt" ):
                listener.enterModifyStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitModifyStmt" ):
                listener.exitModifyStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitModifyStmt" ):
                return visitor.visitModifyStmt(self)
            else:
                return visitor.visitChildren(self)




    def modifyStmt(self):

        localctx = TimelineParser.ModifyStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_modifyStmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 257
            self.match(TimelineParser.MODIFY)
            self.state = 258
            self.match(TimelineParser.ID)
            self.state = 259
            self.match(TimelineParser.LCURLY)
            self.state = 261 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 260
                self.propertyAssignment()
                self.state = 263 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 65464696832) != 0)):
                    break

            self.state = 265
            self.match(TimelineParser.RCURLY)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PropertyAssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def property_(self):
            return self.getTypedRuleContext(TimelineParser.PropertyContext,0)


        def EQ(self):
            return self.getToken(TimelineParser.EQ, 0)

        def expr(self):
            return self.getTypedRuleContext(TimelineParser.ExprContext,0)


        def SEMI(self):
            return self.getToken(TimelineParser.SEMI, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_propertyAssignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPropertyAssignment" ):
                listener.enterPropertyAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPropertyAssignment" ):
                listener.exitPropertyAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPropertyAssignment" ):
                return visitor.visitPropertyAssignment(self)
            else:
                return visitor.visitChildren(self)




    def propertyAssignment(self):

        localctx = TimelineParser.PropertyAssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_propertyAssignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 267
            self.property_()
            self.state = 268
            self.match(TimelineParser.EQ)
            self.state = 269
            self.expr()
            self.state = 270
            self.match(TimelineParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BooleanLiteralContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(TimelineParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(TimelineParser.FALSE, 0)

        def getRuleIndex(self):
            return TimelineParser.RULE_booleanLiteral

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBooleanLiteral" ):
                listener.enterBooleanLiteral(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBooleanLiteral" ):
                listener.exitBooleanLiteral(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBooleanLiteral" ):
                return visitor.visitBooleanLiteral(self)
            else:
                return visitor.visitChildren(self)




    def booleanLiteral(self):

        localctx = TimelineParser.BooleanLiteralContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_booleanLiteral)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 272
            _la = self._input.LA(1)
            if not(_la==23 or _la==24):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





