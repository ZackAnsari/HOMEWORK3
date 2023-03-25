import re

class Token:
    def __init__(self, token_type, value, line, position):
        self.type = token_type
        self.value = value
        self.line = line
        self.position = position

class Lexer:
    def __init__(self, filename):
        self.file = open(filename, 'r')
        self.tokens = []
        self.line_number = 0

    def tokenize(self, string):
        regex_patterns = {
            'add_op': r'\+',
            'sub_op': r'-',
            'mul_op': r'\*',
            'div_op': r'/',
            'mod_op': r'%',
            'lparen': r'\(',
            'rparen': r'\)',
            'assign_op': r'=',
            'eq_op': r'==',
            'lt_op': r'<',
            'lte_op': r'<=',
            'gt_op': r'>',
            'gte_op': r'>=',
            'and_op': r'&&',
            'or_op': r'\|\|',
            'identifier': r'[a-zA-Z][a-zA-Z0-9]*',
            'int_literal': r'\d+',
            'float_literal': r'\d*\.\d+'
        }

        token_regex = '|'.join('(?P<%s>%s)' % pair for pair in regex_patterns.items())
        line = string.strip()
        position = 0

        while line:
            match = re.match(token_regex, line)

            if not match:
                raise ValueError('Invalid token: %s' % line)

            token_type = match.lastgroup
            value = match.group(token_type)

            if token_type == 'identifier':
                token = Token(token_type, value, self.line_number, position)
            elif token_type == 'int_literal' or token_type == 'float_literal':
                token = Token('literal', value, self.line_number, position)
            else:
                token = Token(token_type, None, self.line_number, position)

            self.tokens.append(token)

            position = match.end()
            line = line[position:].lstrip()

    def tokenize_file(self):
        for line in self.file:
            self.line_number += 1
            self.tokenize(line)

        return self.tokens
