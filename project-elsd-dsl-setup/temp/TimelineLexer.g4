lexer grammar TimelineLexer;

EVENT: 'event';
PERIOD: 'period';
TIMELINE: 'timeline';
RELATIONSHIP: 'relationship';
MAIN: 'main';
EXPORT: 'export';
IF: 'if';
ELSE: 'else';
FOR: 'for';
IN: 'in';
MODIFY: 'modify';

HIGH: 'high';
MEDIUM: 'medium';
LOW: 'low';

CAUSE_EFFECT: 'cause-effect';
CONTEMPORANEOUS: 'contemporaneous';
PRECEDES: 'precedes';
FOLLOWS: 'follows';
INCLUDES: 'includes';
EXCLUDES: 'excludes';

BCE: 'BCE';
CE: 'CE';

TRUE: 'true';
FALSE: 'false';

TITLE: 'title';
DATE: 'date';
START: 'start';
END: 'end';
IMPORTANCE: 'importance';
FROM: 'from';
TO: 'to';
TYPE: 'type';
YEAR: 'year';
MONTH: 'month';
DAY: 'day';

EQ: '=';
COMMA: ',';
SEMI: ';';
DOT: '.';
LPAREN: '(';
RPAREN: ')';
LCURLY: '{';
RCURLY: '}';
DASH: '-';
ADD_OP: '+';

LT: '<';
GT: '>';
LE: '<=';
GE: '>=';
EQ_EQ: '==';
NEQ: '!=';

DATE_LITERAL: INT '-BCE' | INT '-CE';
INT: [0-9]+;
STRING: '"' (~["\\])* '"';
ID: [a-zA-Z_][a-zA-Z_0-9]*;

// Skip whitespace and comments
WS: [ \t\r\n]+ -> skip;
COMMENT: '//' ~[\r\n]* -> skip;
BLOCK_COMMENT: '/*' .*? '*/' -> skip;