import Lex

#parsing algo not a real algo
    #like not push down or bottom up algo
    #but it is influenced by bottom up algo as i think it has a stack kinda
#oh shit algo doesn't consider pairs or ` (idk what it would be (could be like a macro lol)
#tbh this algo is pre clever i'm not gonna lie
    #although I would like to generalise the macro system and allow it to be define-macro'd but what ar you gonna do
def parse(tokens, n=0):
    ret = []
    while n < len(tokens):
        if tokens[n] == "(":
            n,tmp = parse(tokens, n+1)
            ret.append(tmp)
        elif tokens[n] == ")":
            return (n, ret)
        else:
            ret.append(tokens[n])
        n += 1
    return (n,ret)

#specieal macros (don't work and everything else works)
"""elif ret[-2] == "." and len(ret) == 3 and tokens[n+1] == ")": #extra checks unenecerarry but comforting
tmp = ["(", "pair", ret[-1], ret[-3]] #the tokens[n+1] == ")" doesn't work
return (n+1, tmp)"""

"""elif tokens[n] == "`" and tokens[n+1] == "(":
n,tmp = parse(tokens,n+2)
tmp_arr = ["(", "quote", tmp, ")"]"""

def convert(string):
    try:
        return float(string)
    except ValueError:
        if string == "true": return True
        elif string == "false": return False
        else: return string

def convert_list(li):
    return list(map(convert, li))

def Parse(tokens):
    tokens = convert_list(tokens)
    _,ret = parse(tokens)
    return ret
