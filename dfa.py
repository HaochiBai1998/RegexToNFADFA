import copy
from state import *

# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting= dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass  
    # You should write this function.
    # It takes two states and a symbol/char. It adds a transition from 
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        if sym not in self.alphabet:
            self.alphabet.append(sym)
        if s1 not in self.states:
            self.states.append(s1)
        if sym in s1.transition:
            s1.transition[sym].append(s2)
        else:
            s1.transition.update({sym:[s2]})
        pass
    # You should write this function.
    # It returns a DFA that is the complement of this DFA
    def complement(self):
        dfa = DFA()
        for i in range(len(self.states)):
            dfa.states.append(self.states[i])
            
        for i in range(len(self.alphabet)):
            dfa.alphabet.append(self.alphabet[i])
        
        for i in range(len(self.is_accepting)):
            dfa.is_accepting[i] = not self.is_accepting[i]
        return dfa
    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, str):
        currS = self.states[0]
        for c in str:
            if c not in self.alphabet:
                return False
            currS = currS.transition[c][0]
        return self.is_accepting[currS.id]
    pass
    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        currS = self.states[0]
        visited = [False for i in range(len(self.states))]
        queue = [(currS,'')]
        while queue:
            currS,string = queue.pop()
            if visited[currS.id]:
                continue
            visited[currS.id] = True
            if self.is_accepting[currS.id]:
                return string
            for sym,nextSs in currS.transition.items():
                for nextS in nextSs:
                    queue.append((nextS,string+sym))
        return None