parser grammar TimelineParser;
options { tokenVocab=TimelineLexer; }

program: declaration* mainBlock? EOF;

declaration: eventDecl | periodDecl | timelineDecl | relationshipDecl;

eventDecl: EVENT ID LCURLY TITLE EQ STRING SEMI DATE EQ dateExpr SEMI (IMPORTANCE EQ importanceValue SEMI)? RCURLY SEMI;

periodDecl: PERIOD ID LCURLY TITLE EQ STRING SEMI START EQ dateExpr SEMI END EQ dateExpr SEMI (IMPORTANCE EQ importanceValue SEMI)? RCURLY SEMI;

timelineDecl: TIMELINE ID LCURLY TITLE EQ STRING SEMI componentList SEMI RCURLY SEMI;

componentList: ID (COMMA ID)* SEMI;

relationshipDecl: RELATIONSHIP ID LCURLY FROM EQ ID SEMI TO EQ ID SEMI TYPE EQ relationshipType SEMI RCURLY SEMI;

dateExpr: fullDateLiteral | monthYearLiteral | yearLiteral | dateCalculation;

dateCalculation: ID DOT (YEAR | MONTH | DAY) ADD_OP INT;

yearLiteral: INT (BCE | CE)?;

monthYearLiteral: INT DASH yearLiteral;

fullDateLiteral: INT DASH monthYearLiteral;

importanceValue: HIGH | MEDIUM | LOW;

relationshipType: CAUSE_EFFECT | CONTEMPORANEOUS | PRECEDES | FOLLOWS | INCLUDES | EXCLUDES | STRING;

mainBlock: MAIN LCURLY statement* RCURLY SEMI;

statement: exportStmt | ifStmt | forStmt | modifyStmt | SEMI;

exportStmt: EXPORT ID SEMI;

ifStmt: IF LPAREN condition RPAREN LCURLY statement* RCURLY (ELSE LCURLY statement* RCURLY)?;

condition: expr comparisonOp expr | ID | booleanLiteral;

comparisonOp: EQ_EQ | NEQ | LT | GT | LE | GE;

expr: ID | STRING | dateExpr | INT | ID DOT property | importanceValue;

property: TITLE | DATE | START | END | IMPORTANCE | TYPE | YEAR | MONTH | DAY;

forStmt: FOR ID IN ID LCURLY statement* RCURLY SEMI;

modifyStmt: MODIFY ID LCURLY propertyAssignment+ RCURLY SEMI;

propertyAssignment: property EQ expr SEMI;

booleanLiteral: TRUE | FALSE;
