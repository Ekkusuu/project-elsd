from flask import Flask, render_template, request, jsonify
from antlr4 import *
from src.TimelineLexer import TimelineLexer
from src.TimelineParser import TimelineParser
from src.TimelineInterpreter import TimelineInterpreter
import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)

@app.route('/')
def index():
    # Read the default timeline content
    default_timeline = ""
    try:
        with open('input.timeline', 'r') as f:
            default_timeline = f.read()
    except:
        pass
    return render_template('index.html', default_timeline=default_timeline)

@app.route('/visualize', methods=['POST'])
def visualize():
    try:
        # Get the timeline code from the request
        timeline_code = request.json.get('code', '')
        
        # Ensure output directory exists
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the code to a temporary file
        with open('temp_input.timeline', 'w') as f:
            f.write(timeline_code)
        
        # Process the timeline
        input_stream = FileStream('temp_input.timeline', encoding='utf-8')
        lexer = TimelineLexer(input_stream)
        tokens = CommonTokenStream(lexer)
        parser = TimelineParser(tokens)
        tree = parser.program()

        interpreter = TimelineInterpreter()
        interpreter.visit(tree)

        # Check for validation errors
        if interpreter.validation_errors:
            return jsonify({
                'success': False,
                'error': 'Validation Errors:',
                'validation_errors': interpreter.validation_errors
            })

        # Check if any exports were made
        if not interpreter.already_exported:
            return jsonify({
                'success': False,
                'error': 'No timeline was exported. Add an export command in the main block to visualize the timeline.',
                'error_type': 'export_missing'
            })

        # Get the first exported timeline
        export_id = next(iter(interpreter.already_exported))
        output_dir = os.path.join(os.getcwd(), "output")
        json_path = os.path.join(output_dir, f"{export_id}.json")

        # Read the JSON file
        try:
            with open(json_path, 'r') as f:
                json_data = f.read()
        except FileNotFoundError:
            return jsonify({
                'success': False,
                'error': f'Failed to read JSON file: {json_path} not found'
            })

        # If it's a timeline, try to read the PNG
        img_data = None
        if export_id in interpreter.timelines:
            png_path = os.path.join(output_dir, f"{export_id}.png")
            try:
                with open(png_path, 'rb') as f:
                    img_data = base64.b64encode(f.read()).decode('utf-8')
            except FileNotFoundError:
                print(f"Warning: PNG file not found at {png_path}")
            except Exception as e:
                print(f"Warning: Failed to read PNG file: {str(e)}")

        # Clean up temporary files
        try:
            os.remove('temp_input.timeline')
        except:
            pass
        
        return jsonify({
            'success': True,
            'image': img_data,
            'json': json_data,
            'type': 'timeline' if export_id in interpreter.timelines else 'component'
        })
        
    except Exception as e:
        print(f"Error in visualization: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
