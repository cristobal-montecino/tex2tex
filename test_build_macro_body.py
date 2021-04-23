#!/usr/bin/python
from token_types import *
from tokenize import tokenize
from macro import build_macro_body

#assert build_macro_body(tokenize('hello #1 world #2')) == ([None, [(TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_TEXT, 'w'),(TOKEN_TYPE_TEXT, 'o'),(TOKEN_TYPE_TEXT, 'r'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'd'), (TOKEN_TYPE_SPACE, ' ')], None, [(TOKEN_TYPE_TEXT, 'h'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'o'), (TOKEN_TYPE_SPACE, ' ')]], [(2, '1'), (0, '2')])

