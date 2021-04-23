from token_types import *
from leftgrowinglist import LeftGrowingList

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

class Macro:
    def __init__(self, pattern, body_tokens):
        self.pattern = pattern
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
        for token in self.pattern:
            ttype, value = token

            if ttype == TOKEN_TYPE_ARG:
                if value in args:
                    # FIXME
                    print(f'error: override a argument: #{value}')
                
                args[value] = get_token_list(tokens)
            else:
                ptoken = tokens.popleft()
                if ptoken is None:
                    # FIXME
                    print(f'error: input ends before pattern is completed')
                    break

                ptype, pvalue = ptoken

                if ttype != ptype or value != pvalue:
                    # FIXME
                    print(f'error: not the same as the pattern: {token} != {(ptoken)}')
        return args
    
