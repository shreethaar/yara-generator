from flask import Flask, render_template, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

class YaraRuleGenerator:
    def __init__(self):
        self.rule_template = """
rule {rule_name} {{
    meta:
        author = "{author}"
        description = "{description}"
        date = "{date}"
        version = "{version}"
    
    strings:
        {string_definitions}
    
    condition:
        {conditions}
}}"""

    def sanitize_identifier(self, name):
        """Sanitize rule name to be a valid YARA identifier."""
        return re.sub(r'[^a-zA-Z0-9_]', '_', name)
    def generate_string_definition(self, string_type, string_value, identifier):
        """Generate a YARA string definition based on type and value."""
        if string_type == "text":
            return f'$string_{identifier} = "{string_value}"'
        elif string_type == "hex":
            return f'$hex_{identifier} = {{ {string_value} }}'
        elif string_type == "regex":
            return f'$regex_{identifier} = /{string_value}/'
        return ""

    def generate_rule(self, rule_data):
        """Generate a complete YARA rule from the provided data."""
        rule_name = self.sanitize_identifier(rule_data.get('rule_name', 'unnamed_rule'))
        string_definitions = []
        for idx, string in enumerate(rule_data.get('strings', [])):
            string_def = self.generate_string_definition(
                string.get('type'),
                string.get('value'),
                idx
            )
            if string_def:
                string_definitions.append(string_def)

        condition_type = rule_data.get('condition_type', 'any')
        if condition_type == 'all':
            conditions = "all of them"
        elif condition_type == 'any':
            conditions = "any of them"
        else:
            conditions = rule_data.get('custom_condition', 'any of them')

        formatted_rule = self.rule_template.format(
            rule_name=rule_name,
            author=rule_data.get('author', 'YARA Rule Generator'),
            description=rule_data.get('description', 'Auto-generated YARA rule'),
            date=datetime.now().strftime("%Y-%m-%d"),
            version=rule_data.get('version', '1.0'),
            string_definitions='\n        '.join(string_definitions),
            conditions=conditions
        )
        
        return formatted_rule


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        rule_data = request.get_json()
        generator = YaraRuleGenerator()
        yara_rule = generator.generate_rule(rule_data)
        return jsonify({'success': True, 'rule': yara_rule})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)




