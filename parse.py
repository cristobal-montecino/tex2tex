from token_types import *
from macro import Macro
from leftgrowinglist import LeftGrowingList
from tokenize import tokenize

MACRO_NATIVE = 0
MACRO_USER = 1

def parse(input_string):
    tokens = LeftGrowingList(tokenize(input_string))
    
    output_builder = []
    macro_types = {'def': MACRO_NATIVE}
    macros = {}
    
    prev_macro = -1
    
    i = 0
    while True:
        i += 1
        
        token = tokens.popleft()
        if token is None:
            break

        ttype, value = token

        if ttype == TOKEN_TYPE_MACRO:
            if value in macro_types:
                macro_type = macro_types[value]
                if macro_type == MACRO_USER:
                    macro = macros[value]
                    args = macro.parse_args(tokens)
                    macro.exec(args, tokens)

                elif macro_type == MACRO_NATIVE:
                    if value == 'def':
                        body_tokens = []
                        pattern = []
                        
                        name_token = tokens.popleft()
                        if name_token is None:
                            # FIXME
                            print('error: input ends before def finishes (name)')
                            return
                        
                        ttype, value = name_token
                        if ttype != TOKEN_TYPE_MACRO:
                            # FIXME
                            print('error: try to define a non macro')
                            return

                        while True:
                            token = tokens.popleft()
                            if token is None:
                                # FIXME
                                print('error: input ends before def finishes (pattern)')
                                return
                            
                            ttype, value = token
                            if ttype == TOKEN_TYPE_OPEN_GROUP:
                                break

                            pattern.append(token)

                        group_count = 1
                        while True:
                            token = tokens.popleft()
                            if token is None:
                                # FIXME
                                print('error: input ends before def finishes (body)')
                                return
                            
                            ttype, value = token
                            if ttype == TOKEN_TYPE_OPEN_GROUP:
                                group_count += 1
                                
                            elif ttype == TOKEN_TYPE_CLOSE_GROUP:
                                group_count -= 1
                                
                                if group_count == 0:
                                    break

                            body_tokens.append(token)
                    
                        _, name = name_token

                        macro_types[name] = MACRO_USER
                        macros[name] = Macro(pattern, body_tokens)

            else:
                output_builder.append(f'\\{value}')
                prev_macro = i

        elif ttype == TOKEN_TYPE_TEXT:
            if prev_macro == i - 1:
                output_builder.append(' ')
          
            output_builder.append(value)
            
        elif ttype == TOKEN_TYPE_DIGIT:
            if prev_macro == i - 1:
                output_builder.append(' ')
                
            output_builder.append(value)
        elif ttype == TOKEN_TYPE_SINGLE_MATH:
            output_builder.append('$')
        elif ttype == TOKEN_TYPE_DOUBLE_MATH:
            output_builder.append('$$')
        elif ttype == TOKEN_TYPE_SPACE:
            output_builder.append(value)
        elif ttype == TOKEN_TYPE_HASH:
            output_builder.append('#')
        elif ttype == TOKEN_TYPE_NEWLINE:
            output_builder.append('\n')
        elif ttype == TOKEN_TYPE_OPEN_GROUP:
            output_builder.append('{')
        elif ttype == TOKEN_TYPE_CLOSE_GROUP:
            output_builder.append('}')
        elif ttype == TOKEN_TYPE_OTHER:
            if prev_macro == i - 1:
                output_builder.append(' ')
                
            output_builder.append(value)
        else:
            if prev_macro == i - 1:
                output_builder.append(' ')
                
            output_builder.append(value)
           
    return ''.join(output_builder)
