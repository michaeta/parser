import os, sys
import m3scanner
import fileinput

class TreeNode(object):
    
    # Usage: root = TreeNode(None, data)
    def __init__(self, parent, data):
        self.data = data
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

def assertS(tokens):
    popped = 0
    
    # S -> ( S ) S
    # match first (
    if isinstance(tokens[0], m3scanner.StartExpr):
        popped += 1
        # try and match the S next
        try: popped += assertS(tokens[popped:])
        # no match? No sweat, we still got 5 more productions to try!
        except: pass
        # we got a match for S !
        else:
            # check for the ) next
            if isinstance(tokens[popped], m3scanner.EndExpr):
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
    if isinstance(tokens[0], m3scanner.StartExpr):
        popped += 1
        try: popped += assertS(tokens[popped:])
        except: pass
        else:
            if isinstance(tokens[popped], m3scanner.EndExpr): return popped + 1
    
    popped = 0
        
    # S -> () S
    if isinstance(tokens[0], m3scanner.StartExpr):
        popped += 1
        if isinstance(tokens[1], m3scanner.EndExpr):
            popped += 1
            try: popped += assertS(tokens[popped:])
            except: pass
            else: return popped
        
    popped = 0
    
    # S -> ()
    if isinstance(tokens[0], m3scanner.StartExpr):
        popped += 1
        if isinstance(tokens[1], m3scanner.EndExpr): return popped + 1
    
    popped = 0
    
    # S -> atom S
    # an atom is defined as any token except an ( or )
    if not (isinstance(tokens[0], m3scanner.StartExpr) or isinstance(tokens[0], m3scanner.EndExpr)):
        popped += 1
        try: popped += assertS(tokens[popped:])
        except: pass
        else: return popped
        
    popped = 0
    
    # S -> atom
    if not (isinstance(tokens[0], m3scanner.StartExpr) or
            isinstance(tokens[0], m3scanner.EndExpr)): return popped + 1
    
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
    if (isinstance(tokens[0], m3scanner.StartExpr) and
        isinstance(tokens[len(tokens)-1], m3scanner.EndExpr)): popped += 1
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
def parse(line):
    tokens = m3scanner.scan(line)
    # asserts production F -> T | T F is enforced
    assertF(tokens)
    return tokens

def parser_wrapper():
    total_parsed = []
    
    for line in fileinput.input():
        tokens = parse(line)
        total_parsed.append(tokens)
    
    return total_parsed

def main():
    output = parser_wrapper()
    
    for statement in output:
        for token in statement:
            print token,
            # uncomment the if statement below to skip printing blank lines from source file.
            #if len(statement) > 0:
        print
    
    print "Successfully parsed with no errors."

if __name__ == '__main__':
    main()
