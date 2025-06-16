import traceback
from flask import Flask, render_template, request, jsonify
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from src.TimelineLexer import TimelineLexer
from src.TimelineParser import TimelineParser
from src.TimelineInterpreter import TimelineInterpreter, ValidationError
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)


# Custom error listener to capture parser errors
class TimelineErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error = {
            'line': line,
            'column': column,
            'message': msg,
            'symbol': offendingSymbol.text if offendingSymbol else None
        }
        self.errors.append(error)


@app.route('/')
def index():
    # Read the default timeline content
    default_timeline = ""
    try:
        with open('input_examples/default_input.timeline', 'r') as f:
            default_timeline = f.read()
    except:
        pass
    return render_template('index.html', default_timeline=default_timeline)

@app.route('/visualize', methods=['POST'])
def visualize():
    try:
        # Get the timeline code from the request
        timeline_code = request.json.get('code', '')
        
        # Check if the code has an export statement
        if 'export' not in timeline_code:
            return jsonify({
                'success': False,
                'error': 'No export statement found. Add an export command in the main block to visualize the timeline.',
                'error_type': 'export_missing'
            })

        # Process the timeline code directly from memory
        input_stream = InputStream(timeline_code)
        lexer = TimelineLexer(input_stream)
        lexer_error_listener = TimelineErrorListener()
        lexer.removeErrorListeners()
        lexer.addErrorListener(lexer_error_listener)
        tokens = CommonTokenStream(lexer)
        parser = TimelineParser(tokens)
        parser_error_listener = TimelineErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(parser_error_listener)

        # Check for lexer errors first
        if lexer_error_listener.errors:
            return jsonify({
                'success': False,
                'error': 'Lexical Errors:',
                'parser_errors': lexer_error_listener.errors,
                'error_type': 'lexer_error'
            })

        # Parse the input
        tree = parser.program()

        # Check for parser errors
        if parser_error_listener.errors:
            return jsonify({
                'success': False,
                'error': 'Syntax Errors:',
                'parser_errors': parser_error_listener.errors,
                'error_type': 'parser_error'
            })

        # Run the interpreter
        interpreter = TimelineInterpreter()
        try:
            result = interpreter.visit(tree)
        except ValidationError as e:
            # Return the validation error with line and column information
            print(f"Validation error at line {e.line}, column {e.column}: {str(e)}")
            return jsonify({
                'success': False,
                'error': 'Validation Error:',
                'validation_errors': interpreter.interpretation_errors,
                'error_type': 'validation_error'
            })
        except NameError as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'Name Error:',
                'name_errors': interpreter.interpretation_errors,
                'error_type': 'name_error'
            })
        except LookupError as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'Lookup Error:',
                'lookup_errors': interpreter.interpretation_errors,
                'error_type': 'lookup_error'
            })
        except TypeError as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'Type Error:',
                'type_errors': interpreter.interpretation_errors,
                'error_type': 'type_error'
            })
        except AttributeError as e:
            print(e)
            return jsonify({
                'success': False,
                'error': 'Type Error:',
                'attribute_errors': interpreter.interpretation_errors,
                'error_type': 'attribute_error'
            })


        if not interpreter.exported_components:
            return jsonify({
                'success': False,
                'error': 'No timeline was exported. Add an export command in the main block to visualize the timeline.',
                'error_type': 'export_missing'
            })

        # Return the components that were rendered by the interpreter
        return jsonify({
            'success': True,
            'components': interpreter.exported_components
        })
        
    except Exception as e:
        error_details = {
            'message': str(e),
            'traceback': traceback.format_exc() if app.debug else None
        }
        if app.debug:
            print(error_details)
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred',
            'error_details': error_details,
            'error_type': 'runtime_error'
        })


if __name__ == '__main__':
    # if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    #     webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=True)
