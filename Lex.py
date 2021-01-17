#if i was really lazy i could just replace all ( by [ and then eval and then w would be good for
#general algorithms

break_chars = {"(", ")"} #characters that end a symbol
ignore_chars = {" ", "\n", "\t"}
def lex(str_in):
    ret = []
    tmp_str = ""
    for c in str_in:
        if c in break_chars or c in ignore_chars:
            ret.append(tmp_str)
            (c in break_chars) and ret.append(c)
            tmp_str = ""
        else:
            tmp_str += c
    return ret

#lexing algo leaves lots of empty space
def clean(tokens):
    return list(filter(lambda n: n != "" and n != " ", tokens)) 

def Lex(str_in):
    return clean(lex(str_in))
