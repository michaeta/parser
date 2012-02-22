# Test Suite for CS480 Milestone 3
# Nicholas Henderson, TJ Michael, Ryan Baker, Justin Durham

import m3parser

pass_test_list = [
            '(())',
            '(atom)',
            '((()))',
            '(()())',
            '(atom ())',
            '((())())',
            '((()))',
            '((atom))',
            '(((())))',
            '((()()))',
            '((atom()))',
            '(((())()))',
            '(()())',
            '(()atom)',
            '(()(()))',
            '(()()())',
            '(()atom())',
            '(()(())())',
            '(atom ())',
            '(atom1 atom2)',
            '(atom (()))',
            '(atom ()())',
            '(atom1 atom2 ())',
            '(atom (())())',
            '((())())',
            '((())atom)',
            '((atom)())',
            '((atom)(()))',
            '(((()))atom)'
            '(((()))()())',
            '(((()()))(()))',
            '(((()()))atom())',
            '((atom ())()())',
            '((atom ())(())())',
            '(((())())atom())',    
            '(((())())(())())'
            ]

fail_test_list = [
                  '(()((()',
                  '((())', #T->(S)->((S))->((()))
                  '((atom ())())())',
                  '(atom',
                  ')atom',
                  'atom)',
                  '((atom)',
                  '((atom)(',
                  'atom)',
                  '(atom',
                  '(()',
                  '())',
                  '()',
                  '((atom)',
                  '(atom))',
                  '(()atom',
                  'atom atom)',
                  '(atom atom',
                  '((atom)atom',
                  '((atom atom'
                  ]

def test_parser():
    
    global pass_test_list
    it = 0
    print 'Testing passing cases:'
    print 'Expected: Pass'
    for test_case in pass_test_list:
        try:
            parsed_list = m3parser.parse(test_case)
            print '%d:\tPass\t%s' % (it, test_case)
        except:
            print '%d:\tFail\t%s' % (it, test_case)
        it += 1
    
    print
    print 'Testing failing cases:'
    print 'Expected: Fail'
    for test_case in fail_test_list:
        try:
            parser_list = m3parser.parse(test_case)
            print '%d:\tPass\t%s' % (it, test_case)
        except:
            print '%d:\tFail\t%s' % (it, test_case)
        it += 1
    
    
if __name__ == '__main__':
    test_parser()
