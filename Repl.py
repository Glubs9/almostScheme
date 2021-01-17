import Main

#output information later (like classic lisp version 0.1)

def unmatched_brackets(string):
    return sum([1 if c == "(" else -1 for c in string if c in {"(", ")"}]) > 0 #might reconstruct set ever iteration but idk

def line():
    inp = input(">>> ")
    while unmatched_brackets(inp): inp += input("... ")
    if inp == "quit": return False
    print(Main.main(inp))
    return True

def Repl():
    Main.load_stdlib()
    #should be some way to have done this better
    while line(): pass

Repl()
