#!/usr/bin/ python3

import datetime
import re
import sys
import os 
import argparse
import hashlib

class YaraEngine:
    def __init__(self, rule_name, author, description=""):
        self.rule_name=rule_name
        self.author=author
        self.description=description
        self.date=datetime.datetimenow().strftime("%Y-%m-%d")
        self.strings=[]
        self.conditions=[]

    def add_string_pattern(self,identifier,pattern,pattern_type="text"):
        if pattern_type=="text":
            self.strings.append(f'$${identifier} = "{pattern}"')
        elif pattern_type=="hex":
            self.strings.append(f'${identifier} = {{ {pattern} }}')
        elif pattern_type == "regex":
            self.strings.append(f'${identifier} = /{pattern}/')
        else:
            raise ValueError("Only use 'text', 'hex' or 'regex'.")

    def add_condition(self, condition):
        self.conditions.append(condition)

    def gen_rule(self):
        meta = f'meta:\n        author = "{self.author}"\n        description = "{self.description}"\n        date = "{self.date}"'
        
        strings = "strings:\n" + "\n".join([f"        {s}" for s in self.strings])
        condition = "condition:\n        " + " and ".join(self.conditions)
        
        rule = f"rule {self.rule_name} {{\n    {meta}\n\n    {strings}\n\n    {condition}\n}}"
        return rule
def main():
    rule_input=input("Enter the name of the rule:")
    author_input=input("Enter the author of the rule:")
    description_input=input("Enter a description for the rule:")
    generator=YaraEngine(rule_input,author_input,description_input)

    while True:
        identifier = input("Enter the identifier for the string pattern (or type 'done' to finish): ")
        if identifier.lower() == 'done':
            break
        pattern = input(f"Enter the pattern for '{identifier}': ")
        pattern_type = input("Enter the pattern type ('text', 'hex', or 'regex'): ").lower()
        generator.add_string_pattern(identifier, pattern, pattern_type)

    while True:
        condition = input("Enter a condition (or type 'done' to finish): ")
        if condition.lower() == 'done':
            break
        generator.add_condition(condition)
    
    print("\n" + "=" * 40)
    print("Generated YARA Rule:\n")
    print(generator.generate_rule())
    print("=" * 40 + "\n")

    


if __name__ == "__main__":
    main()


