from token_types import *
from macro import Macro
from leftgrowinglist import LeftGrowingList
from tokenize import tokenize

MACRO_TYPE_NATIVE = 0
MACRO_TYPE_USER = 1

def parse(input_string):
    tokens = LeftGrowingList(tokenize(input_string))
    
    output_builder = []
    macro_type_of = {'def': MACRO_TYPE_NATIVE}
    macros = {}
    
    next_to_a_macro_index = 0
    
    i = 0
    while True:
        i += 1
        
        token = tokens.popleft()
        if token is None:
            break

        ttype, value = token

        if ttype == TOKEN_TYPE_MACRO:
            if value in macro_type_of:
                macro_type = macro_type_of[value]
                if macro_type == MACRO_TYPE_USER:
                    macro = macros[value]
                    args = macro.parse_args(tokens)
                    macro.exec(args, tokens)

                elif macro_type == MACRO_TYPE_NATIVE:
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

                        macro_type_of[name] = MACRO_TYPE_USER
                        macros[name] = Macro(pattern, body_tokens)

            else:
                output_builder.append(f'\\{value}')
                next_to_a_macro_index = i + 1

        elif ttype == TOKEN_TYPE_TEXT:
            if next_to_a_macro_index == i:
                output_builder.append(' ')
          
            output_builder.append(value)
            
        elif ttype == TOKEN_TYPE_DIGIT:
            if next_to_a_macro_index == i:
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
            if next_to_a_macro_index == i:
                output_builder.append(' ')
                
            output_builder.append(value)
        else:
            if next_to_a_macro_index == i:
                output_builder.append(' ')
                
            output_builder.append(value)
           
    return ''.join(output_builder)
