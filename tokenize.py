from token_types import *

# text [x]
# digits [x]
# macros [x]
# $ [x]
# spaces [x]
# comments [x]
# arguments [x]
# newlines [x]

PARSING_START = 0
PARSING_TEXT = 1
PARSING_MACRO = 2
PARSING_MATH_SYMBOL = 3
PARSING_COMMENT = 4
PARSING_ARG = 5
PARSING_WHITE_SPACE = 6

END_CHARACTER = '\0'

def tokenize(input_string, need_append_end_character = True):
    state = PARSING_START
    
    if need_append_end_character:
        input_string += END_CHARACTER

    tokens = []

    start = 0
    end = 0
    for i, c in enumerate(input_string):
        while True:
            if state == PARSING_START:
                if c.isalpha():
                    # this solves:
                    # BUG: '\eat hello' where '\def\eat#1{}' assign #1 = hello
                    tokens.append((TOKEN_TYPE_TEXT, c))
                    
                elif c == ' ' or c == '\t':
                    start = i
                    end = i+1
                    state = PARSING_WHITE_SPACE

                elif c == '\\':
                    start = i+1
                    end = i+1
                    state = PARSING_MACRO

                elif c == '{':
                    tokens.append((TOKEN_TYPE_OPEN_GROUP, c))
                elif c == '}':
                    tokens.append((TOKEN_TYPE_CLOSE_GROUP, c))

                elif c == '\n':
                    tokens.append((TOKEN_TYPE_NEWLINE, c))
                
                elif c.isdigit():
                    tokens.append((TOKEN_TYPE_DIGIT, c))
                elif c == '$':
                    state = PARSING_MATH_SYMBOL
                elif c == '%':
                    state = PARSING_COMMENT
                elif c == '#':
                    state = PARSING_ARG
                elif c == END_CHARACTER:
                    break
                else:
                    tokens.append((TOKEN_TYPE_OTHER, c))

            # TODO: this is not in use
            elif state == PARSING_TEXT:
                if c.isalpha():
                    end += 1
                else:
                    tokens.append((TOKEN_TYPE_TEXT, input_string[start:end]))
                    state = PARSING_START
                    continue

            elif state == PARSING_MACRO:
                if c.isalpha():
                    end += 1
                elif end - start == 0 and (c == '\\' or c == ' '):
                    end += 1
                    tokens.append((TOKEN_TYPE_MACRO, input_string[start:end]))
                    state = PARSING_START
                    
                else:   
                    tokens.append((TOKEN_TYPE_MACRO, input_string[start:end]))
                    state = PARSING_START
     
                    if c != ' ' and c != '\t':
                        continue

            elif state == PARSING_MATH_SYMBOL:
                token_type = TOKEN_TYPE_SINGLE_MATH if c != '$' else TOKEN_TYPE_DOUBLE_MATH

                tokens.append((token_type, None))
                state = PARSING_START

                if c != '$':
                    continue
                
            elif state == PARSING_COMMENT:
                if c == '\n' or c == END_CHARACTER:
                    state = PARSING_START
        
            elif state == PARSING_ARG:
                state = PARSING_START

                if c == '#':
                    tokens.append((TOKEN_TYPE_HASH, None))
                elif c.isdigit():
                    tokens.append((TOKEN_TYPE_ARG, c))    
                else:
                    # this might return an error, but is fine because this code is for a translator
                    tokens.append((TOKEN_TYPE_HASH, None))
                    continue

            elif state == PARSING_WHITE_SPACE:
                if c == ' ' or c == '\t':
                    end += 1
                    break
        
                tokens.append((TOKEN_TYPE_SPACE, input_string[start:end]))
                state = PARSING_START
                continue

            break

    return tokens
