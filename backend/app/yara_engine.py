import datetime
import re
import sys
from typing import List, Dict, Optional

class YaraEngine:
    def __init__(self):
        self.rules: List[Dict] = []

    def _sanitize_name(self, name: str) -> str:
        """Sanitize rule name to be a valid YARA identifier."""
        return re.sub(r'[^a-zA-Z0-9_]', '_', name)

    def create_rule(self, rule_name: str, author: str, description: str = "") -> Dict:
        """Create a new YARA rule."""
        rule = {
            "rule_name": self._sanitize_name(rule_name),
            "author": author,
            "description": description,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "metadata": {},
            "strings": [],
            "conditions": []
        }
        self.rules.append(rule)
        return rule

    def add_metadata(self, rule: Dict, key: str, value: str) -> None:
        """Add metadata to a rule."""
        rule["metadata"][key] = value

    def add_string_pattern(self, rule: Dict, identifier: str, pattern: str, pattern_type: str = "text") -> None:
        """Add a string pattern to a rule."""
        if pattern_type not in ["text", "hex", "regex"]:
            raise ValueError("Pattern type must be 'text', 'hex', or 'regex'")
        if pattern_type == "hex" and not re.match(r'^[0-9A-Fa-f\s]+$', pattern):
            raise ValueError("Invalid hex pattern. Use hexadecimal characters (0-9, A-F)")
        
        if pattern_type == "text":
            string_def = f'${identifier} = "{pattern}"'
        elif pattern_type == "hex":
            string_def = f'${identifier} = {{ {pattern} }}'
        elif pattern_type == "regex":
            string_def = f'${identifier} = /{pattern}/'
        
        rule["strings"].append(string_def)

    def add_condition(self, rule: Dict, condition: str) -> None:
        """Add a condition to a rule."""
        rule["conditions"].append(condition)

    def generate_rule(self, rule: Dict) -> str:
        """Generate a YARA rule string from a rule dictionary."""
        meta = "\n        ".join(f'{key} = "{value}"' for key, value in {
            "author": rule["author"],
            "description": rule["description"],
            "date": rule["date"],
            **rule["metadata"]
        }.items())
        
        strings = "\n        ".join(rule["strings"])
        conditions = " and ".join(rule["conditions"])
        
        return f"""rule {rule["rule_name"]} {{
    meta:
        {meta}

    strings:
        {strings}

    condition:
        {conditions}
}}"""

    def generate_all_rules(self) -> str:
        """Generate all YARA rules as a single string."""
        return "\n\n".join(self.generate_rule(rule) for rule in self.rules)

    def save_rules(self, filename: str = "rules.yar") -> None:
        """Save all rules to a .yar file."""
        with open(filename, 'w') as f:
            f.write(self.generate_all_rules())
        print(f"Rules saved to: {filename}")

def get_user_input(prompt: str, required: bool = True) -> str:
    """Helper function to get user input."""
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please try again.")

def print_guide():
    """Print a short guide for users."""
    print("\n=== YARA Rule Generator Guide ===")
    print("1. Rule Name: A unique name for the rule (alphanumeric and underscores only).")
    print("2. Author: Your name or identifier.")
    print("3. Description: A brief description of the rule.")
    print("4. Metadata: Optional key-value pairs for additional information.")
    print("5. String Patterns: Add text, hex, or regex patterns.")
    print("6. Conditions: Define conditions for the rule (e.g., 'any of them').")
    print("7. Save: Save the rule(s) to a .yar file.\n")

def main():
    try:
        print_guide()
        engine = YaraEngine()
        
        while True:
            print("\n=== Create a New Rule ===")
            rule_name = get_user_input("[1] Enter the name of the rule: ")
            author = get_user_input("[2] Enter the author of the rule: ")
            description = get_user_input("[3] Enter a description for the rule: ", required=False)
            rule = engine.create_rule(rule_name, author, description)
            
            while True:
                add_metadata = input("\nWould you like to add additional metadata? (y/n): ").lower()
                if add_metadata != 'y':
                    break
                key = get_user_input("Enter metadata key: ")
                value = get_user_input("Enter metadata value: ")
                engine.add_metadata(rule, key, value)
            
            print("\n=== Adding String Patterns ===")
            while True:
                identifier = get_user_input("\n[4] Enter the identifier for the string pattern (or 'done' to finish): ")
                if identifier.lower() == 'done':
                    break
                pattern = get_user_input(f"[5] Enter the pattern for '{identifier}': ")
                while True:
                    pattern_type = get_user_input(
                        "[6] Enter the pattern type ('text', 'hex', or 'regex'): "
                    ).lower()
                    if pattern_type in ['text', 'hex', 'regex']:
                        break
                    print("Invalid pattern type. Please use 'text', 'hex', or 'regex'.")
                try:
                    engine.add_string_pattern(rule, identifier, pattern, pattern_type)
                    print(f"Added {pattern_type} pattern: ${identifier}")
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            
            print("\n=== Adding Conditions ===")
            while True:
                condition = get_user_input("\nEnter a condition (or 'done' to finish): ")
                if condition.lower() == 'done':
                    break
                engine.add_condition(rule, condition)
            
            another_rule = input("\nWould you like to create another rule? (y/n): ").lower()
            if another_rule != 'y':
                break
        
        print("\n" + "=" * 50)
        print("Generated YARA Rules:")
        print("=" * 50)
        print(engine.generate_all_rules())
        print("=" * 50 + "\n")
        
        save = input("Would you like to save these rules to a file? (y/n): ").lower()
        if save == 'y':
            filename = input("Enter filename (press Enter for default 'rules.yar'): ").strip()
            engine.save_rules(filename if filename else None)
    
    except KeyboardInterrupt:
        print("\n\nRule generation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
