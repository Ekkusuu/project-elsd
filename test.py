from antlr4 import *
from src import TimelineLexer, TimelineParser, TimelineInterpreter


def main():
    input_stream = FileStream("input_examples/default_input.timeline", encoding='utf-8')
    lexer = TimelineLexer(input_stream)
    tokens = CommonTokenStream(lexer)
    parser = TimelineParser(tokens)
    tree = parser.program()

    visitor = TimelineInterpreter()
    visitor.visit(tree)


if __name__ == "__main__":
    main()
