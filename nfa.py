from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are acceping
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass
    def __str__(self):
        pass
    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym = '&'):
        if sym !='&' and sym not in self.alphabet:
            self.alphabet.append(sym)
        if s1 not in self.states:
            self.states.append(s1)
        if sym in s1.transition:
            s1.transition[sym].append(s2)
        else:
            s1.transition.update({sym:[s2]})
        pass
    # You should write this function.
    # It takes an nfa, adds all the states from that nfa and return a 
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def union(self,nfa1):

        nfa_union = NFA()
        nfa_union.states.append(state(0))
        nfa_union.is_accepting[0] = False

        nfa_union.addStatesFrom(nfa1)
        nfa_union.addTransition(nfa_union.states[0],nfa_union.states[1],'&')

        size = len(nfa_union.states)
        nfa_union.addStatesFrom(self)
        nfa_union.addTransition(nfa_union.states[0],nfa_union.states[size],'&')
        return nfa_union

    def addStatesFrom(self, nfa):
        for c in nfa.alphabet:
            if c not in self.alphabet:
                self.alphabet.append(c)
        offset = len(self.states)
        size = len(nfa.states)
        for i in range(size):
            state = nfa.states[i]
            is_accepting_status =  nfa.is_accepting[state.id]
            state.id = state.id + offset
            self.states.append(state)
            self.is_accepting[state.id] = is_accepting_status
        pass
    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    # on epsilon transitions.
    def findTransSet(self,ns,sym):
        states = []
        for n in ns:
            for sym_n , nn in n.transition.items():
                if sym_n == sym:
                    for s in nn:
                        states.append(s)
        return states
    def epsilonClose(self, ns):
        states = []
        queue = []
        for n in ns:
            queue.append(n)
        while queue:
            n = queue.pop()
            states.append(n)
            for sym, nn in n.transition.items():
                if sym == '&':
                    for s in nn:
                        if s not in states:
                            queue.append(s)
        return states
        # for n in ns:
        #     for sym, nn in self.states[n.id].transition.items():  
        #         if sym == '&':
        #             for s in nn:
        #                 states.append(s)
        # return states
    def findStateById(self,id):
        for state in self.states:
            if state.id == id:
                return state
        pass
    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        queue = [(self.states[0], 0)]
        currS = self.states[0]
        pos = 0
        visited = [[] for i in range(len(string)+1)]
        while queue:
            currS, pos = queue.pop()
            if pos == len(string):
                if currS.id in self.is_accepting and self.is_accepting[currS.id]:
                    return self.is_accepting[currS.id]
                for n in self.epsilonClose([currS]):
                    if n not in visited[pos]:
                        queue.append((n, pos))  
                        visited[pos].append(n)
                continue
            for s in self.states:
                if s.id == currS.id:
                    if string[pos] in s.transition:
                        stats = s.transition[string[pos]]
                        for stat in stats:
                            if stat not in visited[pos+1]:
                                queue.append((stat, pos+1))  
                                visited[pos+1].append(stat)
                            # queue.extend([(stat,pos+1)])
                            for s in self.epsilonClose([stat]):
                                if s not in visited[pos+1]:
                                    queue.append((s, pos+1))  
                                    visited[pos+1].append(s)
                                # queue.extend([(s,pos+1)])
                    else:
                        for n in self.epsilonClose([currS]):
                            if n not in visited[pos]:
                                queue.append((n, pos))  
                                visited[pos].append(n)
                            # queue.append((n, pos))
                    break
        if pos == len(string):
            return currS.id in self.is_accepting and self.is_accepting[currS.id]
        else:
            return False
    pass
