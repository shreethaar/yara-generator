from flask import request, jsonify
from .yara_engine import YaraEngine
from . import app

@app.route('/generate', methods=['POST'])
def generate_rule():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400

        engine = YaraEngine()
        rule = engine.create_rule(
            rule_name=data.get('rule_name'),
            author=data.get('author'),
            description=data.get('description', '')
        )
        
        for key, value in data.get('metadata', {}).items():
            engine.add_metadata(rule, key, value)
        for string in data.get('strings', []):
            engine.add_string_pattern(
                rule,
                identifier=string.get('identifier'),
                pattern=string.get('pattern'),
                pattern_type=string.get('type', 'text')
            )
        for condition in data.get('conditions', []):
            engine.add_condition(rule, condition)
        
        yara_rule = engine.generate_rule(rule)
        if data.get('save', False):
            filename = data.get('filename', 'rules.yar')
            engine.save_rules(filename)
            return jsonify({'success': True, 'rule': yara_rule, 'saved_to': filename})
        return jsonify({'success': True, 'rule': yara_rule})
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return jsonify({'success': False, 'error': 'An unexpected error occurred'}), 500
