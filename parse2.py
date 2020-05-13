'''
This program implements a recursive descent parser for the CFG below:

Syntax Rule  Lookahead Set          Strings generated
------------------------------------------------------------
1 <exp> → <term>{+<term> | -<term>}
2 <term> → <factor>{*<factor> | /<factor>}
3 <factor> → (<exp>) | <number>
'''
import math
class ParseError(Exception): pass

#---------------------------------------
# Parse an Expression   <exp> → <term>{+<term> | -<term>}
#
def exp():
    global i, err

    value = term()
    while True:
        if w[i] == '+':
            i += 1
            value = binary_op('+', value, term())
        elif w[i] == '-':
            i += 1
            value = binary_op('-', value, term())
        else:
            break

    return value
#---------------------------------------
# Parse a Term   <term> → <factor>{+<factor> | -<factor>}
#
def term():
    global i, err

    value = factor()
    while True:
        if w[i] == '*':
            i += 1
            value = binary_op('*', value, factor())
        elif w[i] == '/':
            i += 1
            value = binary_op('/', value, factor())
        else:
            break

    return value
#---------------------------------------
# Parse a Factor   <factor> → (<exp>) | <number> 
#       
array = ""
def factor():
    global i, err, array
    value = None
    if w[i] == '(':
        i += 1          # read the next character
        value = exp()
        if w[i] == ')':
            i += 1
            value = func(array, value)
        else:
            print('missing )')
            raise ParseError

    elif w[i] == 'pi':
        i += 1
        return math.pi

    elif w[i] in ['sin', 'cos', 'tan', 'sqrt']:
        array = w[i]
        i+=1
        value = exp()

    else:
        try:
            value = atomic(w[i])
            i += 1          # read the next character
        except ValueError:
            try:
                value = atomicStr(w[i])
            except ValueError:
                print('number expected')
                value = None
    
    #print('factor returning', value)
    
    return value


#==============================================================
# BACK END PARSER (ACTION RULES)
#==============================================================

def binary_op(op, lhs, rhs):
    if op == '+': return lhs + rhs
    elif op == '-': return lhs - rhs
    elif op == '*': return lhs * rhs
    elif op == '/': return lhs / rhs
    else: return None

def atomic(x):
    return float(x)

def atomicStr(x):
    return str(x)

def func(op, lhs):
    if op == 'sin': return math.sin(lhs)
    elif op == 'cos': return math.cos(lhs)
    elif op == 'tan': return math.tan(lhs)
    elif op == 'sqrt': return math.sqrt(lhs)
    else: return None

dict = {}
while True:
    i = 0 # keeps track of what character we are currently reading.
    err = None
    w = None
    w = input('\nEnter input string: ')
    temp = w
    
    if w == 'table':
        for x, y in dict.items():
            print(str(x) + ' | ' + str(y))
    else:
        for c in '()+-*/':
            w = w.replace(c, ' '+c+' ')
        w = w.split()
        w.append('$') # EOF marker

        print('\nToken Stream:\n')
        for t in w: print(t, end = '  ')
        print('\n\nEnd Token Stream\n')

        finalVal = exp()
        try:
            print('Result:\n\n', finalVal) # call the parser
        except:
            print('parse error')
        print()


        if w[i] != '$': print('Syntax error: all input not parsed')

        for c in w[:i]:print(c, end = '')
        print(' | ', end = '')
        for c in w[i:]: print(c, end = '')
        dict[str(temp)] = finalVal




