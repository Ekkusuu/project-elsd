# this is just a program for testing the lexer/parser

from antlr4 import *
from TimelineLexer import TimelineLexer 
from TimelineParser import TimelineParser  

def parse_file(file_path):
    # Open the input file and read its contents
    with open(file_path, 'r') as file:
        input_text = file.read()

    # Convert input text into an input stream
    input_stream = InputStream(input_text)
    
    # Create a lexer instance using the input stream
    lexer = TimelineLexer(input_stream)
    
    # Create a token stream from the lexer
    token_stream = CommonTokenStream(lexer)
    
    # Create a parser instance using the token stream
    parser = TimelineParser(token_stream)
    
    try:
        # Parse the input starting from the 'program' rule (change based on your grammar)
        tree = parser.program()
        
        # Check if the parse tree is generated
        if tree:
            print("Parse Tree:")
            print(tree.toStringTree(recog=parser))
        else:
            print("No parse tree generated.")

    except Exception as e:
        print(f"Error during parsing: {e}")

file_path = 'input.timeline'  # Path to your input file
parse_file(file_path)
