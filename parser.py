import os, sys
pro_dir = os.path.dirname(os.getcwd())
sys.path[0] = pro_dir

from milestone2 import scanner

def assertS(tokens):
    popped = 0
    
    # S -> ( S ) S
    # match first (
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        # try and match the S next
        try: popped += assertS(tokens[popped:])
        # no match? No sweat, we still got 5 more productions to try!
        except: pass
        # we got a match for S !
        else:
            # check for the ) next
            if isinstance(tokens[popped], scanner.EndExpr):
                popped += 1
                # try and match the final S in the production
                try: popped += assertS(tokens[popped:])
                # the 2nd S failed to match... 
                except: pass
                # holy crap! We matched the whole ( S ) S 
                else: return popped
    
    # well, we failed to match ( S ) S, so its time to see if we can match one of the 
    # other productions. First we have to reset any partial matches though.
    popped = 0
        
    # S -> ( S )
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        try: popped += assertS(tokens[popped:])
        except: pass
        else: 
            if isinstance(tokens[popped], scanner.EndExpr): return popped + 1
    
    popped = 0
        
    # S -> () S
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        if isinstance(tokens[1], scanner.EndExpr):
            popped += 1
            try: popped += assertS(tokens[popped:])
            except: pass
            else: return popped 
        
    popped = 0
    
    # S -> ()
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        if isinstance(tokens[1], scanner.EndExpr): return popped + 1
    
    popped = 0
    
    # S -> atom S
    # an atom is defined as any token except an ( or )
    if not (isinstance(tokens[0], scanner.StartExpr) or isinstance(tokens[0], scanner.EndExpr)):
        popped += 1
        try: popped += assertS(tokens[popped:])
        except: pass
        else: return popped
        
    popped = 0
    
    # S -> atom
    if not (isinstance(tokens[0], scanner.StartExpr) or 
            isinstance(tokens[0], scanner.EndExpr)): return popped + 1
    
    # Well... we checked for every production and nothing matched...
    # Time to raise an Exception
    raise Exception("Syntax Error, Improper nested paren.")
    

def assertT(tokens):
    # counts popped tokens off of the tokens list
    # no tokens are actually being popped, its just used to keep track
    # of how far we have parsed
    popped = 0
    
    # T -> ( S )
    # checks to make sure that beginning and end () are there
    # Yes, S should be checked in the middle, but why parse all of S if the last ) is gone? 
    if (isinstance(tokens[0], scanner.StartExpr) and 
        isinstance(tokens[len(tokens)-1], scanner.EndExpr)): popped += 1
    else: raise Exception("Syntax Error, Improper nested paren.")
    
    # assert that production S -> () | atom | ( S ) | () S | atom S | ( S ) S is enforced
    popped += assertS(tokens[popped:(len(tokens)-1)])
    
    # + 1 is for end ) which was removed at begining
    return popped + 1
    
    
def assertF(tokens):
    popped = 0
    
    # This line is blank?!?!? RETURN!
    if tokens == []: return
    
    # F -> T 
    popped += assertT(tokens)
    
    # F -> T F
    if popped < len(tokens): assertF(tokens[popped:])
    
            
# open that source code and make sure its syntax is correct!
def parse(file_name):
    # 2D list, doesn't have to be, but it makes it easier to print
    total_parsed = []
    
    # open file, each line of source code is a string in list lines
    with open(file_name) as fp:
        lines = fp.readlines()
    
    # for each line, each line is a statement with () around it
    for line in lines:
        #convert line into list of tokens: TOKENIZE!!!!
        tokens = scanner.scan(line)
        # asserts production F -> T | T F is enforced
        assertF(tokens) 
        # append list of tokens to total parsed, this line is assured correct
        total_parsed.append(tokens)
    
    return total_parsed


# main is used for test cases
def main():
    output = parse("test_case.txt")
    
    for statement in output:
        for token in statement:
            print token,
        # uncomment the if statement below to skip printing blank lines from source file.
        #if len(statement) > 0:
        print


if __name__ == "__main__":
    main()

    

        

    
            
                