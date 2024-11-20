"""

TO FIX:
1. Multiple rule (Current: Single rule)
2. Output file .yar is not right
3. Print out short guide on input

"""


#!/usr/bin/python3
import datetime
import re
import sys
import os
import argparse
import hashlib
from typing import List, Dict, Optional

class YaraEngine:
    def __init__(self, rule_name: str, author: str, description: str = ""):
        self.rule_name = self._sanitize_name(rule_name)
        self.author = author
        self.description = description
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.strings: List[Dict] = []
        self.conditions: List[str] = []
        self.metadata: Dict[str, str] = {}

    def _sanitize_name(self, name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9_]', '_', name)

    def add_metadata(self, key: str, value: str) -> None:
        self.metadata[key] = value

    def add_string_pattern(self, identifier: str, pattern: str, pattern_type: str = "text") -> None:
        if pattern_type not in ["text", "hex", "regex"]:
            raise ValueError("Pattern type must be 'text', 'hex', or 'regex'")
        if pattern_type == "hex":
            if not re.match(r'^[0-9A-Fa-f\s]+$', pattern):
                raise ValueError("Invalid hex pattern. Use hexadecimal characters (0-9, A-F)")
        if pattern_type == "text":
            string_def = f'${identifier} = "{pattern}"'
        elif pattern_type == "hex":
            string_def = f'${identifier} = {{ {pattern} }}'
        elif pattern_type == "regex":
            string_def = f'${identifier} = /{pattern}/'
        self.strings.append(string_def)

    def add_condition(self, condition: str) -> None:
        self.conditions.append(condition)

    def generate_rule(self) -> str:
        metadata_items = {
            "author": self.author,
            "description": self.description,
            "date": self.date,
            **self.metadata
        }
        
        meta = "\n        ".join(f'{key} = "{value}"' for key, value in metadata_items.items())
        meta = f"meta:\n        {meta}"
        strings = "strings:\n" + "\n".join([f"        {s}" for s in self.strings])
        condition = "condition:\n        " + " and ".join(self.conditions)
        rule = f"""rule {self.rule_name} {{
    {meta}

    {strings}

    {condition}
}}"""
        return rule

    def save_rule(self, filename: str = None) -> None:
        if filename is None:
            filename = f"{self.rule_name}.yar"
        
        with open(filename, 'w') as f:
            f.write(self.generate_rule())
        print(f"Rule saved to: {filename}.yar")

def get_user_input(prompt: str, required: bool = True) -> str:
    while True:
        value = input(prompt).strip()
        if value or not required:
            return value
        print("This field is required. Please try again.")

def main():
    try:
        print("\n=== YARA Rule Generator ===\n")
        rule_name = get_user_input("[1] Enter the name of the rule: ")
        author = get_user_input("[2] Enter the author of the rule: ")
        description = get_user_input("[3] Enter a description for the rule: ", required=False)
        generator = YaraEngine(rule_name, author, description)
        while True:
            add_metadata = input("\nWould you like to add additional metadata? (y/n): ").lower()
            if add_metadata != 'y':
                break
            key = get_user_input("Enter metadata key: ")
            value = get_user_input("Enter metadata value: ")
            generator.add_metadata(key, value)
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
                generator.add_string_pattern(identifier, pattern, pattern_type)
                print(f"Added {pattern_type} pattern: ${identifier}")
            except ValueError as e:
                print(f"Error: {e}")
                continue
        print("\n=== Adding Conditions ===")
        while True:
            condition = get_user_input("\nEnter a condition (or 'done' to finish): ")
            if condition.lower() == 'done':
                break
            generator.add_condition(condition)
        print("\n" + "=" * 50)
        print("Generated YARA Rule:")
        print("=" * 50)
        print(generator.generate_rule())
        print("=" * 50 + "\n")
        save = input("Would you like to save this rule to a file? (y/n): ").lower()
        if save == 'y':
            filename = input("Enter filename (press Enter for default name): ").strip()
            generator.save_rule(filename if filename else None)
    except KeyboardInterrupt:
        print("\n\nRule generation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()



