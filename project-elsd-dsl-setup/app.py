from flask import Flask, render_template, request, jsonify
from TimelineInterpreter import TimelineInterpreter
from antlr4 import *
from TimelineLexer import TimelineLexer
from TimelineParser import TimelineParser
import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

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
        
        # Save the code to a temporary file
        with open('temp_input.timeline', 'w') as f:
            f.write(timeline_code)
        
        # Process the timeline
        input_stream = FileStream('temp_input.timeline', encoding='utf-8')
        lexer = TimelineLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = TimelineParser(token_stream)
        tree = parser.program()
        
        # Create and run the interpreter
        interpreter = TimelineInterpreter()
        walker = ParseTreeWalker()
        walker.walk(interpreter, tree)
        
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

        # Generate the visualization in memory
        plt.clf()  # Clear any existing plots
        for timeline_id in interpreter.already_exported:  # Only process exported timelines
            # Generate visualization for the first timeline found
            img_buf = BytesIO()
            interpreter.generate_visualization(timeline_id, save_path=None)
            plt.savefig(img_buf, format='png', bbox_inches='tight')
            plt.close()
            img_buf.seek(0)
            img_data = base64.b64encode(img_buf.read()).decode('utf-8')

            # Prepare JSON data
            timeline = interpreter.timelines[timeline_id]
            json_data = {
                "timeline_id": timeline_id,
                "title": timeline["title"],
                "events": [],
                "periods": [],
                "relationships": []
            }

            # Add events
            for comp_id in timeline["components"]:
                if comp_id in interpreter.events:
                    json_data["events"].append({
                        "id": comp_id,
                        **interpreter.events[comp_id]
                    })
                elif comp_id in interpreter.periods:
                    json_data["periods"].append({
                        "id": comp_id,
                        **interpreter.periods[comp_id]
                    })

            # Add relationships
            for rel_id, rel in interpreter.relationships.items():
                if rel["from"] in timeline["components"] and rel["to"] in timeline["components"]:
                    json_data["relationships"].append({
                        "id": rel_id,
                        **rel
                    })

            return jsonify({
                'success': True,
                'image': img_data,
                'json': json_data
            })
        
        return jsonify({
            'success': False,
            'error': 'No timeline found in the code'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 