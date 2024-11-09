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
        meta= f'
        meta:\n
        author:"author = "{self.author}"\n        
        description = "{self.description}"\n        
        date = "{self.date}"'
        
        strings = "strings:\n" + "\n".join([f"        {s}" for s in self.strings])
        condition = "condition:\n        " + " and ".join(self.conditions)
        rule = f"rule {self.rule_name} {{\n    {meta}\n\n    {strings}\n\n    {condition}\n}}"
        return rule

if __name__ == "__main__":


