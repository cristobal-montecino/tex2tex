#!/usr/bin/python
from tokenize import tokenize

print(tokenize(input() + '\0'))
