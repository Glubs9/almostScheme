#both run and main both need to import these functions but since run is imported in
#main we can't put it in any of those three files so i separated them out into this file so i
#can import everything

import Lex
import Parse

#comments are handled here cause i'm lazy
def readfile(file_name):
    return  ''.join([
        l[:l.index(";")] if ";" in l else l
        for l in open(file_name, "r").readlines() 
        if l[0] != ";"
    ])

def lex_and_parse(str_in):
    tmp = Lex.Lex(str_in)
    tmp = Parse.Parse(tmp)
    return tmp
