from token_types import *
from macro import Macro
from leftgrowinglist import LeftGrowingList
from tokenize import tokenize

MACRO_TYPE_NATIVE = 0
MACRO_TYPE_USER = 1

def parse_def(macros, macro_type_of, tokens):
    body_tokens = []
    pattern = []
    
    name_token = tokens.popleft()
    if name_token is None:
        # FIXME
        print('error: def: input ends before def finishes (name)')
        return
       
    ttype, value = name_token
    if ttype != TOKEN_TYPE_MACRO:
        # FIXME
        print('error: def: try to define a non macro')
        return
        
    PARSING_START = 0
    PARSING_HASH = 1
    
    status = PARSING_START
    pattern_loop = True
    while pattern_loop:
        token = tokens.popleft()
        if token is None:
            # FIXME
            print('error: def: input ends before def finishes (pattern)')
            return
        
        ttype, value = token
        
        while True:
            if status == PARSING_START:
                if ttype == TOKEN_TYPE_OPEN_GROUP:
                    pattern_loop = False
                    break
                    
                elif ttype == TOKEN_TYPE_HASH:
                    status = PARSING_HASH
                    
                else:
                    pattern.append(token)
                
            elif status == PARSING_HASH:
                status = PARSING_START
                
                if ttype == TOKEN_TYPE_HASH:
                    pattern.append(token)
                    
                elif ttype ==  TOKEN_TYPE_DIGIT:
                    pattern.append((TOKEN_TYPE_ARG, value))
                    
                else:
                    # FIXME
                    pattern.append(token)
                    print('error: def: # need # or a digit next to it')
                    continue
               
            break

    status = PARSING_START
    group_count = 1
    body_loop = True    
    while body_loop:
        token = tokens.popleft()
        if token is None:
            # FIXME
            print('error: def: input ends before def finishes (body)')
            return
        
        ttype, value = token
        while True:
            if status == PARSING_START:
                if ttype == TOKEN_TYPE_OPEN_GROUP:
                    group_count += 1
                    
                elif ttype == TOKEN_TYPE_CLOSE_GROUP:
                    group_count -= 1
                    
                    if group_count == 0:
                        body_loop = False
                        break
                        
                elif ttype == TOKEN_TYPE_HASH:
                    status = PARSING_HASH
                    break
                
                body_tokens.append(token)
                    
            elif status == PARSING_HASH:
                status = PARSING_START
                
                if ttype == TOKEN_TYPE_HASH:
                    body_tokens.append(token)
                    
                elif ttype == TOKEN_TYPE_DIGIT:
                    body_tokens.append((TOKEN_TYPE_ARG, value))
                    
                else:
                    continue

            break

    _, name = name_token

    macro_type_of[name] = MACRO_TYPE_USER
    macros[name] = Macro(pattern, body_tokens)

def parse_let(macros, macro_type_of, tokens):
    to_token = tokens.popleft()
    if to_token is None:
        # FIXME
        print('error: let: need two macros (missing first)')
        return
     
    ttype, to_name = to_token
    if ttype != TOKEN_TYPE_MACRO:
        # FIXME
        print('error: let: need two macros (first is not a macro token)')
        return
    
    from_token = tokens.popleft()
    if from_token is None:
        # FIXME
        print('error: let: need two macros (missing second)')
        return
        
    ttype, from_name = from_token
    if ttype != TOKEN_TYPE_MACRO:
        # FIXME
        print('error: let: need two macros (second is not a macro token)')
        return
    
    macro_type_of[to_name] = macro_type_of[from_name]
    macros[to_name] = macros[from_name]

def parse_user_macro(macro, tokens):
    args = macro.parse_args(tokens)
    macro.exec(args, tokens)

def parse_expandafter(macros, macro_type_of, tokens):
    holded_token = tokens.popleft()
    if holded_token is None:
        # FIXME
        print('error: expandafter: need two tokens (first is not found)')
        
    token = tokens.popleft()
    if token is None:
        # FIXME
        print('error: expandafter: need two tokens (second is not found)')
    
    while True:    
        ttype, value = token
        if ttype == TOKEN_TYPE_MACRO:
            if value in macro_type_of:
                macro_type = macro_type_of[value]
                if macro_type == MACRO_TYPE_USER:
                    macro = macros[value]
                    parse_user_macro(macro, tokens)
                    break
                    
        tokens.appendleft(token)
        break
        
    tokens.appendleft(holded_token)

def parse_futurelet(macros, macro_type_of, tokens):
    to_token = tokens.popleft()
    if to_token is None:
        # FIXME
        print('error: futurelet: need three tokens (missing first)')
        return
     
    holded_token = tokens.popleft()
    if holded_token is None:
        # FIXME
        print('error: futurelet: need three tokens (missing second)')
        return
        
    tokens.appendleft(to_token)

    parse_let(macros, macro_type_of, tokens)
    
    tokens.appendleft(holded_token)   

def parse(input_string):
    tokens = LeftGrowingList(tokenize(input_string))
    
    output_builder = []
    macro_type_of = {
        'def': MACRO_TYPE_NATIVE,
        'let': MACRO_TYPE_NATIVE,
        'expandafter': MACRO_TYPE_NATIVE,
        'futurelet': MACRO_TYPE_NATIVE,
    }
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
                    parse_user_macro(macro, tokens)
                    
                elif macro_type == MACRO_TYPE_NATIVE:
                    if value == 'def':
                        parse_def(macros, macro_type_of, tokens)
                        
                    elif value == 'let':
                        parse_let(macros, macro_type_of, tokens)

                    elif value == 'expandafter':
                        parse_expandafter(macros, macro_type_of, tokens)
                        
                    elif value == 'futurelet':
                        parse_futurelet(macros, macro_type_of, tokens)

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
