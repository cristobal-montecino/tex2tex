from token_types import *
from leftgrowinglist import LeftGrowingList


PATTERN_TOKENS = 0
PATTERN_ARG = 1

def build_macro_pattern(pattern_tokens):
    start = 0
    end = 0
    
    PARSING_START = 0
    PARSING_TOKENS = 1

    state = PARSING_START

    pattern = []

    for i, token in enumerate(pattern_tokens):
        ttype, value = token
        
        while True:
            if state == PARSING_START:
                if ttype == TOKEN_TYPE_ARG:
                    pattern.append((PATTERN_ARG, value))
                else:
                    start = i
                    end = i + 1
                    state = PARSING_TOKENS

            elif state == PARSING_TOKENS:
                if ttype != TOKEN_TYPE_ARG:
                    end += 1
                    break
                
                pattern.append((PATTERN_TOKENS, pattern_tokens[start:end]))
                state = PARSING_START
                continue

            break

    if state == PARSING_TOKENS:
        pattern.append((PATTERN_TOKENS, pattern_tokens[start:end]))
    
    return pattern


def build_macro_body(body_tokens):
    start = 0
    end = 0
    
    PARSING_START = 0
    PARSING_TOKENS = 1

    state = PARSING_START

    body = []
    replace_index = []

    for i, token in enumerate(body_tokens):
        ttype, value = token
        
        while True:
            if state == PARSING_START:
                if ttype == TOKEN_TYPE_ARG:
                    where = len(body)
                    by = value
                    replace_index.append((where, by))
                    body.append(None)
                else:
                    start = i
                    end = i + 1
                    state = PARSING_TOKENS

            elif state == PARSING_TOKENS:
                if ttype != TOKEN_TYPE_ARG:
                    end += 1
                    break
                
                body.append(body_tokens[start:end])
                state = PARSING_START
                continue

            break

    if state == PARSING_TOKENS:
        body.append(body_tokens[start:end]) 

    body.reverse()

    last = len(body) - 1
    for i, (where, by) in enumerate(replace_index):
        replace_index[i] = (last - where, by)

    return (body, replace_index)
 
# If you modify get_token_list,
# modify get_token_list_with_boundaries
def get_token_list(tokens):
    token = tokens.popleft()
    if token is None:
        # FIXME
        print('error: no more tokens')
        return [token]

    ttype, value = token
    if ttype == TOKEN_TYPE_OPEN_GROUP:
        token_list = []

        group_count = 1
        while True:
            token = tokens.popleft()
            if token is None:
                # FIXME
                print('error: missing }')
                break

            ttype, value = token
            
            if ttype == TOKEN_TYPE_OPEN_GROUP:
                group_count += 1
            
            elif ttype == TOKEN_TYPE_CLOSE_GROUP:
                group_count -= 1
                
                if group_count == 0:
                    break
            
            token_list.append(token)
        
        return token_list

    else:
        return [token]
        
# Warning: This is a modification of get_token_list
# If you modify get_token_list, modify this
def get_token_list_with_boundaries(tokens):
    token = tokens.popleft()
    if token is None:
        # FIXME
        print('error: no more tokens')
        return [token]

    ttype, value = token
    if ttype == TOKEN_TYPE_OPEN_GROUP:
        token_list = [token]

        group_count = 1
        while True:
            token = tokens.popleft()
            if token is None:
                # FIXME
                print('error: missing }')
                break

            ttype, value = token
            token_list.append(token)
            
            if ttype == TOKEN_TYPE_OPEN_GROUP:
                group_count += 1
            
            elif ttype == TOKEN_TYPE_CLOSE_GROUP:
                group_count -= 1
                
                if group_count == 0:
                    break
        
        return token_list

    else:
        return [token]

def check_pattern(pattern_tokens, tokens, arg_value):
    tmp = []
    is_first = True
    first_token_list = None
    for token in pattern_tokens:
        ttype, value = token
        
        current_token_list = get_token_list_with_boundaries(tokens)
        
        if is_first:
            first_token_list = current_token_list
            is_first = False
        else:
            tmp.extend(current_token_list)
        
        ctype, cvalue = current_token_list[0]

        if ttype != ctype or value != cvalue or len(current_token_list) > 1:
            tokens.extendleft(tmp)
            arg_value.extend(first_token_list)
            return False
            
    return True

class Macro:
    def __init__(self, pattern_tokens, body_tokens):
        self.pattern = build_macro_pattern(pattern_tokens)
        body, replace_index = build_macro_body(body_tokens)
        self.body = body
        self.replace_index = replace_index
    
    def exec(self, args, tokens):
        for where, by in self.replace_index:
            if by in args:
                self.body[where] = args[by]
            else:
                # FIXME
                print(f'Argument #{by} not defined')
                self.body[where] = []

        for token_list in self.body:
            tokens.extendleft(token_list)

    def parse_args(self, tokens):
        args = {}
        
        PARSING_START = 0
        PARSING_ARG = 1
        
        arg_name = ''
        state = PARSING_START
        for pattern_type, pattern_value in self.pattern:
            while True:
                if state == PARSING_START:
                    if pattern_type == PATTERN_ARG:
                        arg_name = pattern_value
                        state = PARSING_ARG
                        
                    elif pattern_type == PATTERN_TOKENS:
                        for token in pattern_value:
                            ttype, value = token
                            
                            current_token = tokens.popleft()
                            if current_token is None:
                                # FIXME
                                print('error: input ends before pattern is completed')
                                break

                            ctype, cvalue = current_token

                            if ttype != ctype or value != cvalue:
                                # FIXME
                                print(f'error: not the same as the pattern: {token} != {(current_token)}')
                                
                elif state == PARSING_ARG:
                    if pattern_type == PATTERN_ARG:                        
                        args[arg_name] = get_token_list(tokens)
                        arg_name = pattern_value
                        
                    elif pattern_type == PATTERN_TOKENS: 
                        first_token = tokens.popleft()
                        if first_token is None:
                            # FIXME
                            print('error: input ends before pattern is completed')
                            break

                        tokens.appendleft(first_token)
                        
                        ttype, value = first_token
                        if ttype == TOKEN_TYPE_OPEN_GROUP:
                            args[arg_name] = get_token_list(tokens)
                            state = PARSING_START
                            continue
                        else:   
                            arg_value = []
                            while not check_pattern(pattern_value, tokens, arg_value):
                                pass
                            
                            args[arg_name] = arg_value
                            state = PARSING_START
                break

        if state == PARSING_ARG:
            args[arg_name] = get_token_list(tokens)
            
        return args
    
