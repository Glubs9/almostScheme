from CircularDependencyFixer import lex_and_parse, readfile
import Run
import sys
sys.setrecursionlimit(10**8) #roughly double the recursion limit

def main(str_in):
    return Run.Run(lex_and_parse(str_in))

def load_stdlib():
    return main(readfile("stdlib.cl")) #should return nothing
