#!/usr/bin/python
from token_types import *
from tokenize import tokenize
from macro import Macro
from leftgrowinglist import LeftGrowingList

macro = Macro(tokenize('user: #1'), tokenize('hello #1'))

token_list = tokenize('user: {TeX}')
assert token_list == [(TOKEN_TYPE_TEXT, 'u'),(TOKEN_TYPE_TEXT, 's'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'r'), (TOKEN_TYPE_OTHER, ':'), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_OPEN_GROUP, '{'), (TOKEN_TYPE_TEXT, 'T'), (TOKEN_TYPE_TEXT, 'e'), (TOKEN_TYPE_TEXT, 'X'), (TOKEN_TYPE_CLOSE_GROUP, '}')]

tokens = LeftGrowingList(token_list)

args = macro.parse_args(tokens)

assert args == {'1': [(TOKEN_TYPE_TEXT, 'T'), (TOKEN_TYPE_TEXT, 'e'), (TOKEN_TYPE_TEXT, 'X')]}

macro.exec(args, tokens)

assert tokens.to_list() == [(TOKEN_TYPE_TEXT, 'h'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'o'), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_TEXT, 'T'), (TOKEN_TYPE_TEXT, 'e'), (TOKEN_TYPE_TEXT, 'X')]
