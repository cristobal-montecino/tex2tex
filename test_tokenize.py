from token_types import *
from tokenize import tokenize

assert tokenize('hello world') == [(TOKEN_TYPE_TEXT, 'h'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'o'), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_TEXT, 'w'),(TOKEN_TYPE_TEXT, 'o'),(TOKEN_TYPE_TEXT, 'r'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'd')]
assert tokenize('hello #1 world') == [(TOKEN_TYPE_TEXT, 'h'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'o'), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_ARG, '1'), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_TEXT, 'w'),(TOKEN_TYPE_TEXT, 'o'),(TOKEN_TYPE_TEXT, 'r'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'd')]

assert tokenize('hello $\\alpha$ world') == [(TOKEN_TYPE_TEXT, 'h'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'o'), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_SINGLE_MATH, None), (TOKEN_TYPE_MACRO, 'alpha'), (TOKEN_TYPE_SINGLE_MATH, None), (TOKEN_TYPE_SPACE, ' '), (TOKEN_TYPE_TEXT, 'w'),(TOKEN_TYPE_TEXT, 'o'),(TOKEN_TYPE_TEXT, 'r'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'd')]

assert tokenize('{hello}') == [(TOKEN_TYPE_OPEN_GROUP, '{'), (TOKEN_TYPE_TEXT, 'h'),(TOKEN_TYPE_TEXT, 'e'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'l'),(TOKEN_TYPE_TEXT, 'o'), (TOKEN_TYPE_CLOSE_GROUP, '}')]

assert tokenize('\\\\a') == [(TOKEN_TYPE_MACRO, '\\'), (TOKEN_TYPE_TEXT, 'a')]

assert tokenize('\\ a') == [(TOKEN_TYPE_MACRO, ' '), (TOKEN_TYPE_TEXT, 'a')]

assert tokenize('\\a\\b') == [(TOKEN_TYPE_MACRO, 'a'), (TOKEN_TYPE_MACRO, 'b')]
