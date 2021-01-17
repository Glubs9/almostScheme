from CircularDependencyFixer import readfile, lex_and_parse

#global scope is dictionary defined later in file containing the defined global scope
def search_global_scope(name):
    if name in global_scope: return global_scope[name]
    return False

def is_in_global_scope(name):
    return name in global_scope

def find_in_scope(scope, var_name):
    #maybe if we want to have static scope we might be able to make this remove the scope here?
    if is_in_global_scope(var_name): return search_global_scope(var_name) #double call doesn't matter as is_in_global_scope is O(1) (!= false to handle truthy values)
    for name, res in reversed(scope):
        if name == var_name: return res
    return False

#might not be called
def is_in_scope(scope, var_name):
    return not not_in_scope(scope, var_name)

def not_in_scope(scope, var_name):
    if is_in_global_scope(var_name): return False
    for name, res in reversed(scope):
        if name == var_name: return False
    return True

#too complicated for a lambda
def handle_cond(arr, scope):
    #arr[0] == "cond"
    for n in arr[1:]: 
        if eval_s(n[0], scope) == True: return eval_s(n[1], scope)
    raise Exception("no true result found in cond " + str(arr))

def handle_func(arr, scope):
    return eval_s(
            [find_in_scope(scope, arr[0])] + arr[1:], #i put eval thing here
            scope
    )

#very slow but makes the scope small
    #might be some way to higher order it
def unique_key(arr):
    ret = set()
    ret_arr = []
    for n in reversed(arr):
        if n[0] not in ret: 
            ret.add(n[0])
            ret_arr.append(n)
    return list(reversed(ret_arr))

#this has fucked the entire thing up
def make_add_scope(parameters, args, scope):
    return list(zip(parameters, map(lambda n: eval_s(n, scope), args)))

#done in multiple parts for clarity
def handle_lambda(arr, scope):
    rec_eval_s = arr[0][2]
    #have to zip arr[0][1] and arr[1:]
    assert len(arr[0][1]) == len(arr[1:]), ("argument arity mismatch with args " + str(arr[0][1]))
    add_scope = make_add_scope(arr[0][1], arr[1:], scope) #add_scope is fucking it up
    return eval_s(rec_eval_s, unique_key(scope + add_scope))

#don't eval_s arguments before zipping
def handle_macro(arr, scope):
    rec_eval_s = arr[0][2]
    #have to zip arr[0][1] and arr[1:]
    assert len(arr[0][1]) == len(arr[1:]), ("argument arity mismatch with args " + str(arr[0][1]))
    add_scope = list(zip(arr[0][1], arr[1:]))
    return eval_s(rec_eval_s, scope + add_scope)

#only a separate function because it is side effects
def handle_define(arr, scope):
    global_scope[arr[1]] = arr[2]
    return #idk what to return, probs nothing

#maybe change to adding arr[1] to scope without modifying anything?
    #if i do that make sure to check for correct syntax
#might be able to shift to lambda then re eval_s
def handle_let(arr, scope):
    ret = list(map(lambda n: (n[0], eval_s(n[1], scope)), arr[1]))
    return eval_s(arr[2], scope + ret)

def handle_letlaz(arr, scope):
    return eval_s(arr[2], scope + arr[1]) #this is pretty nifty but do syntax check

def handle_begin(arr, scope):
    for n in arr[1:-1]:
        eval_s(n, scope)
    return eval_s(arr[-1], scope)

#might not be necersarry to have as a separte function
def handle_const(arr, scope):
    val = global_scope[arr[0]]
    rec_arr = [val] + arr[1:] #might not need the extra array
    return eval_s(rec_arr, scope)

#i think i wsas supposed to put these scope dictionaries in the scope call with eval
    #wait no i am using the dictionaries to generalize the eval function a lil bit
    #and scope is used for lambda
global_scope = {"e": []} #e is defined so you don't have to write (quote ())

def print_and_return(arr, msg=""):
    print(msg + str(arr))
    return arr

#how to handle argument arity for predefined_functions
predefined_functions = {
        "quote": lambda n, scope: n[1],
        "list": lambda n, scope: list(map(lambda i: eval_s(i, scope), n[1:])),
        "car": lambda n, scope: eval_s(n[1], scope)[0],
        "cdr": lambda n, scope: eval_s(n[1], scope)[1:],
        "cons": lambda n, scope: [eval_s(n[1], scope)] + eval_s(n[2], scope),
        "eq": lambda n, scope: eval_s(n[1], scope) == eval_s(n[2], scope), #for everything
        "=": lambda n, scope: eval_s(n[1], scope) == eval_s(n[2], scope), #for numbers
        "atom": lambda n, scope: type(eval_s(n[1], scope)) is not list,
        "cond": handle_cond,
        #"f": handle_func,
        "define": handle_define,
        "eval": lambda n, scope: eval_s(eval_s(n[1], scope), scope), #might not be necersarry
        "let": handle_let,
        "letlaz": handle_letlaz, #let lazy which doesn't evaluate the value of each definition
        #add letrec
        "disp": lambda n, scope: print(eval_s(n[1], scope)),
        "dispnnl": lambda n, scope: print(eval_s(n[1], scope), end=''), #display no new line
        "dispchar": lambda n, scope: print(chr(int(eval_s(n[1], scope))), end=''),
        "trace": lambda n, scope: print_and_return(eval_s(n[1], scope)),
        "begin": handle_begin, 
        "+": lambda n, scope: eval_s(n[1], scope) + eval_s(n[2], scope), #lots of repetition in math functions
        "-": lambda n, scope: eval_s(n[1], scope) - eval_s(n[2], scope), #lots of repetition in math functions
        "*": lambda n, scope: eval_s(n[1], scope) * eval_s(n[2], scope), #lots of repetition in math functions
        "/": lambda n, scope: eval_s(n[1], scope) / eval_s(n[2], scope), # #lots of repetition in math functions
        "and": lambda n, scope: eval_s(n[1], scope) and eval_s(n[2], scope),
        "or": lambda n, scope: eval_s(n[1], scope) or eval_s(n[2], scope),
        "not": lambda n, scope: not eval_s(n[1], scope),
        "lambda": lambda n, scope: n, #for when lambda is passed to a function
        "empty": lambda n, scope: len(eval_s(n[1], scope)) == 0,
        "print-scope": lambda n, scope: print(scope), #for debugging the interp
        "<": lambda n, scope: eval_s(n[1], scope) < eval_s(n[2], scope),
        "<=": lambda n, scope: eval_s(n[1], scope) <= eval_s(n[2], scope),
        ">": lambda n, scope: eval_s(n[1], scope) > eval_s(n[2], scope),
        ">=": lambda n, scope: eval_s(n[1], scope) >= eval_s(n[2], scope),
        "load": lambda n, scope: Run(lex_and_parse(readfile(n[1]))),
        "mod": lambda n, scope: eval_s(n[1], scope) % eval_s(n[2], scope),
        "input": lambda n, scope: input(""),
        "input-msg": lambda n, scope: input(n[1]), #inputs with atom given
        "last": lambda n, scope: eval_s(n[1], scope)[-1], #could be defined in stdlib but it would be really slow
        "init": lambda n, scope: eval_s(n[1], scope)[:-1] #^
}

#add load command

#i don't like that there are two calls for list_in[0] is str
def eval_s(list_in, scope):
    #print("list_in = " + str(list_in))
    #print("scope ^ is " + str(scope))
    #pre much just a list of if statements and corresponding functions
    if type(list_in) is float or type(list_in) is bool: return list_in 
    elif type(list_in) is str:
        if not_in_scope(scope, list_in): 
            return list_in #for when you evaluate higher order arguments (tmp == False to avoid falsey values)
        tmp = find_in_scope(scope, list_in) 
        return tmp
    elif type(list_in[0]) is str and is_in_scope(scope, list_in[0]): return handle_func(list_in, scope)
    elif type(list_in[0]) is str and list_in[0] in predefined_functions: return predefined_functions[list_in[0]](list_in, scope)
    elif list_in[0][0] == "lambda": return handle_lambda(list_in, scope)
    elif list_in[0][0] == "lambda-macro": return handle_macro(list_in, scope)
    #print("list_in = " + str(list_in))
    #if no case found then just eval till it works lmao
    if type(list_in[0]) is list: return eval_s([eval_s(list_in[0], scope)] + list_in[1:], scope)
    raise Exception(str(list_in[0]) + " called with " + str(list_in[1:]) + " but function not found") #might not be true all the time

def Run(ast):
    for n in ast[:-1]:
        eval_s(n, [])
    return eval_s(ast[-1], [])
