import os, sys
pro_dir = os.path.dirname(os.getcwd())
sys.path[0] = pro_dir

from milestone2 import scanner

correctly_parsed = []

def assertS(tokens):
    global correctly_parsed
    assert isinstance(tokens, list)

    popped = 0
    
    # S -> ( S ) S
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        try:
            poppedS1 = assertS(tokens[popped:len(tokens)])
        except:
            pass
        else:
            if isinstance(tokens[popped + poppedS1], scanner.EndExpr):
                popped += 1
                try:
                    poppedS2 = assertS(tokens[(popped + poppedS1):len(tokens)])
                except:
                    pass
                else:
                    correctly_parsed.append(tokens.pop(0))
                    for token in range(poppedS1):
                        tokens.pop(0)
                    correctly_parsed.append(tokens.pop(0))
                    for token in range(poppedS2):
                        tokens.pop(0)
                    return popped + poppedS1 + poppedS2
    
    popped = 0
        
    # S -> ( S )
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        try:
            poppedS1 = assertS(tokens[popped:len(tokens)])
        except:
            pass
        else:
            if isinstance(tokens[popped + poppedS1], scanner.EndExpr):
                popped += 1
                correctly_parsed.append(tokens.pop(0))
                for token in range(poppedS1):
                    tokens.pop(0)
                correctly_parsed.append(tokens.pop(0))
                return popped + poppedS1
    
    popped = 0
        
    # S -> () S
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        if isinstance(tokens[1], scanner.EndExpr):
            popped += 1
            try:
                poppedS1 = assertS(tokens[popped:len(tokens)])
            except:
                pass
            else:
                correctly_parsed.append(tokens.pop(0))
                correctly_parsed.append(tokens.pop(0))
                for token in range(poppedS1):
                    tokens.pop(0)
                return popped + poppedS1
        
    popped = 0
    
    # S -> ()
    if isinstance(tokens[0], scanner.StartExpr):
        popped += 1
        if isinstance(tokens[1], scanner.EndExpr):
            popped += 1
            correctly_parsed.append(tokens.pop(0))
            correctly_parsed.append(tokens.pop(0))
            return popped
    
    popped = 0
    
    # S -> atom S
    if not (isinstance(tokens[0], scanner.StartExpr) or isinstance(tokens[0], scanner.EndExpr)):
        popped += 1
        try:
            poppedS1 = assertS(tokens[popped:len(tokens)])
        except:
            pass
        else:
            correctly_parsed.append(tokens.pop(0))
            for token in range(poppedS1):
                tokens.pop(0)
            return popped + poppedS1   
        
    popped = 0
    
    # S -> atom
    if not (isinstance(tokens[0], scanner.StartExpr) or isinstance(tokens[0], scanner.EndExpr)):
        popped += 1
        correctly_parsed.append(tokens.pop(0))
        return popped
              
    raise Exception("Syntax Error, Improper nested paren.")
    

def assertT(tokens):
    global correctly_parsed
    assert isinstance(tokens, list)
    
    # T -> ( S )
    if isinstance(tokens[0], scanner.StartExpr):
        correctly_parsed.append(tokens.pop(0))
    else:
        raise Exception("Syntax Error, Expected: (")
    assertS(tokens)
    if isinstance(tokens[0], scanner.EndExpr):
        correctly_parsed.append(tokens.pop(0))
    else:
        raise Exception("Syntax Error, Expected: )")    
    

def parse(file_name):
    global correctly_parsed
    total_parsed = []
    with open(file_name) as fp:
        lines = fp.readlines()
    
    for line in lines:
        tokens = scanner.scan(line)
        
        if len(tokens) > 0:
            assertT(tokens) 

        total_parsed.append(correctly_parsed)
        correctly_parsed = []
    
    return total_parsed


def main():
    output = parse("test_case.txt")
    
    for statement in output:
        for token in statement:
            print token,
        #if len(statement) > 0:
        print

if __name__ == "__main__":
    main()

    

        

    
            
                