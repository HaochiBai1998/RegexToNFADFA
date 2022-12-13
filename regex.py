from nfa import *
from state import *

class Regex:
    def __repr__(self):
        ans=str(type(self))+"("
        sep=""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep=", "
            pass
        ans=ans+")"
        return ans
    def transformToNFA(self):
        pass
    pass

class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "{}{}".format(self.children[0],self.children[1])
    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()
        size = len(nfa1.states)
        id = 0
        for i in range(len(nfa1.is_accepting)):
            if nfa1.is_accepting[i] is True:
                id = i
                nfa1.is_accepting[i] = False
                break
        nfa1.addStatesFrom(nfa2)
        s1 = nfa1.findStateById(id)
        s2 = nfa1.states[size]
        nfa1.addTransition(s1,s2,'&')
        return nfa1
    pass

class StarRegex(Regex):
    def __init__(self, r1):
        self.children=[r1]
        pass
    def __str__(self):
        return "({})*".format(self.children[0])
    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        nfa = NFA()
        nfa.states.append(state(0))
        nfa.is_accepting[0] = False
        nfa.addStatesFrom(nfa1)
        size = len(nfa.states)
        nfa.is_accepting[size-1] = False
        nfa.states.append(state(size))
        nfa.is_accepting[size] = True
        nfa.addTransition(nfa.states[0],nfa.states[1],'&')
        nfa.addTransition(nfa.states[0],nfa.states[size],'&')
        nfa.addTransition(nfa.states[size-1],nfa.states[size],'&')
        nfa.addTransition(nfa.states[size-1],nfa.states[1],'&')
        return nfa
    pass

class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children=[r1,r2]
        pass
    def __str__(self):
        return "(({})|({}))".format(self.children[0],self.children[1])
    def transformToNFA(self):
        nfa1 = self.children[0].transformToNFA()
        nfa2 = self.children[1].transformToNFA()
        nfa = NFA()
        nfa.states.append(state(0))
        nfa.is_accepting[0] = False

        nfa.addStatesFrom(nfa1)
        nfa1_end_state = nfa.states[len(nfa.states)-1]
        nfa.is_accepting[nfa1_end_state.id] = False
        nfa.addTransition(nfa.states[0],nfa.states[1],'&')

        size = len(nfa.states)
        nfa.addStatesFrom(nfa2)
        nfa2_end_state = nfa.states[len(nfa.states)-1]
        nfa.is_accepting[nfa2_end_state.id] = False
        nfa.addTransition(nfa.states[0],nfa.states[size],'&')

        accepting_state = state(len(nfa.states))
        nfa.is_accepting[accepting_state.id] = True
        nfa.states.append(accepting_state)
        nfa.addTransition(nfa1_end_state,accepting_state,'&')
        nfa.addTransition(nfa2_end_state,accepting_state,'&')

        return nfa
    pass

class SymRegex(Regex):
    def __init__(self, sym):
        self.sym=sym
        pass
    def __str__(self):
        return self.sym
    def __repr__(self):
        return self.sym
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(state(0))
        nfa.is_accepting[nfa.states[0].id] = False
        nfa.states.append(state(1))
        nfa.addTransition(nfa.states[0],nfa.states[1],self.sym)
        nfa.is_accepting[nfa.states[1].id] = True
        return nfa
    pass

class EpsilonRegex(Regex):
    def __init__(self):
        pass
    def __str__(self):
        return '&'
    def __repr__(self):
        return '&'
    def transformToNFA(self):
        nfa = NFA()
        nfa.states.append(state(0))
        nfa.is_accepting[nfa.states[nfa.startS].id] = True
        s = nfa.states[0]
        nfa.addTransition(s,s,'&')
        return nfa
    pass

class ReInput:
    def __init__(self,s):
        self.str=s
        self.pos=0
        pass
    def peek(self):
        if (self.pos < len(self.str)):
            return self.str[self.pos]
        return None
    def get(self):
        ans = self.peek()
        self.pos +=1
        return ans
    def eat(self,c):
        ans = self.get()
        if (ans != c):
            raise ValueError("Expected " + str(c) + " but found " + str(ans)+
                             " at position " + str(self.pos-1) + " of  " + self.str)
        return c
    def unget(self):
        if (self.pos > 0):
            self.pos -=1
            pass
        pass
    pass

# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


#It gets a regular expression string and returns a Regex object. 
def parse_re(s):
    inp=ReInput(s)
    def parseR():
        return rtail(parseC())
    def parseC():
        return ctail(parseS())
    def parseS():
        return stars(parseA())
    def parseA():
        c=inp.get()
        if c == '(':
            ans=parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)
    def rtail(lhs):
        if (inp.peek()=='|'):
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs,x))
        return lhs
    def ctail(lhs):
        if(inp.peek() is not None and inp.peek() not in '|*)'):
            temp=parseS()
            return ctail(ConcatRegex(lhs,temp))
        return lhs
    def stars(lhs):
        while(inp.peek()=='*'):
            inp.eat('*')
            lhs=StarRegex(lhs)
            pass
        return lhs
    return parseR()