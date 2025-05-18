from TimelineInterpreter import TimelineInterpreter
from antlr4 import *
from TimelineLexer import TimelineLexer
from TimelineParser import TimelineParser

input_stream = FileStream("input.timeline", encoding='utf-8')
lexer = TimelineLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = TimelineParser(token_stream)
tree = parser.program()

# Walk the tree using the custom interpreter
walker = ParseTreeWalker()
interpreter = TimelineInterpreter()
walker.walk(interpreter, tree)



