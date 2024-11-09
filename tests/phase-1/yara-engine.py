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

