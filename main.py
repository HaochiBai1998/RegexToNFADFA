import copy
from regex import *
from state import * 
from nfa import *
from dfa import *
def containsSet(target,sSet):
    for i in range(len(sSet)):
        s = sSet[i]
        if len(s)!=len(target):
            continue
        equal = True

        for state in target:
            if state not in s:
                equal = False
                break
        if equal:
            return i
    return -1
def minusNFA(nfa1,nfa2):

    dfa1 = nfaToDFA(nfa1)
    dfa1_comp = dfa1.complement()
    nfa1_comp = dfaToNFA(dfa1_comp)
    nfa_union = nfa1_comp.union(nfa2)
    dfa_union = nfaToDFA(nfa_union)
    dfa_union_comp = dfa_union.complement()
    return dfaToNFA(dfa_union_comp)

# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    table = dict()
    Sets = []
    queue = []
    Sets.append(nfa.epsilonClose([nfa.states[0]]))
    table.update({0:dict()})
    queue.append(0)
    while queue:
        index = queue.pop()
        currSet = Sets[index]
        for sym in nfa.alphabet:
            newSet = nfa.epsilonClose(nfa.findTransSet(currSet,sym))
            i = containsSet(newSet,Sets)
            if i!=-1: 
                table[index].update({sym:i})
            else:
                size = len(Sets)
                Sets.append(newSet)
                table.update({size:dict()})
                queue.append(size)
                table[index].update({sym:size})

    dfa = DFA()
    dfa.alphabet = nfa.alphabet
    for i in range(len(table)):
        dfa.states.append(state(i))
    trap_index = len(dfa.states)
    dfa.states.append(state(trap_index))
    for sym in dfa.alphabet:
        dfa.addTransition(dfa.states[trap_index],dfa.states[trap_index],sym)
    trap_index = trap_index + 1
    for i in range(len(table)):
        for sym in dfa.alphabet:
            if sym in table[i].keys():
                index = table[i][sym]
                dfa.addTransition(dfa.states[i],dfa.states[index],sym)
            else:
                dfa.addTransition(dfa.states[i],dfa.states[trap_index],sym)
    accepting_ids = []
    for i in range(len(nfa.is_accepting)):
        if nfa.is_accepting[i]:
            accepting_ids.append(i)

    for i in range(len(table)):
        accepting_status = False
        for s in Sets[i]:
            if s.id in accepting_ids:
                accepting_status = True
                break
        dfa.is_accepting.update({i:accepting_status})
    dfa.is_accepting.update({len(table):False})
    return dfa
# You should write this function.
# It takes an DFA and returns a NFA
def dfaToNFA(dfa):
    nfa = NFA()
    for i in range(len(dfa.states)):
        nfa.states.append(dfa.states[i])
        
    for i in range(len(dfa.alphabet)):
        nfa.alphabet.append(dfa.alphabet[i])
    
    for i in range(len(dfa.is_accepting)):
        nfa.is_accepting[i] = dfa.is_accepting[i]
    return nfa
# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    nfa4 = re1.transformToNFA()
    nfa3 = re2.transformToNFA()
    minusNFA1_2 = minusNFA(nfa1,nfa2)
    minusNFA2_1 = minusNFA(nfa4,nfa3)
    dfa1 = nfaToDFA(minusNFA1_2)
    dfa2 = nfaToDFA(minusNFA2_1)
    if dfa1.shortestString() is None and dfa2.shortestString() is None:
        return True
    return False



if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(nfa, s, expected):
        # test your dfa conversion
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testDFA(strRe, s, expected):
        # test your dfa conversion
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ",res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res , " on " , s , " but expected " , expected)
            pass
        pass

    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)
        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ",strRe2, ") = ", res, " but expected " , expected)
            pass
        pass

    def testUnion(strRe1, strRe2,string, expected):
        re1 = parse_re(strRe1)
        nfa1 = re1.transformToNFA()
        re2 = parse_re(strRe2)
        nfa2 = re2.transformToNFA()
        nfa_union = nfa1.union(nfa2)
        res = nfa_union.isStringInLanguage(string)
        if res == expected:
            print(strRe1, " union ",strRe2, " gave ",res, " as expected on ", string)
        else:
            print("**** ",strRe1, " union ",strRe2, " Gave ", res , " on " , string , " but expected " , expected)
            pass
        pass
    def pp(r):
        print()
        print("Starting on " +str(r))
        re=parse_re(r)
        print(repr(re))
        print(str(re))
        pass

    # #test your NFA:
    testNFA('&','',True)
    testNFA('a', '', False)
    testNFA('a', 'a', True)
    testNFA('a', 'ab', False)
    testNFA('ab', 'ab', True)
    testNFA('ab', 'ba', False)
    testNFA('abc', 'abc', True)
    testNFA('abc', 'ab', False)
    testNFA('a*', '', True)
    testNFA('a*', 'a', True)
    testNFA('a|c*', 'a', True)
    testNFA('a|c*', 'ccc', True)
    testNFA('a|c*', 'aa', False)
    testNFA('a*|c', 'aa', True)
    testNFA('((a*)c*)*', 'acacaaaccc', True)
    testNFA('((a*)c*)*', 'acacacaacaaca', True)
    testNFA('((a*)c*)*', 'cacaccacacac', True)
    testNFA('((a*)c*)*', 'acacacaccccaca', True)
    testNFA('((a*)c*)*', 'cacaacaccacac', True)
    testNFA('a|b', '', False)
    testNFA('a|b', 'a', True)
    testNFA('a|b', 'b', True)
    testNFA('a|b', 'ab', False)
    testNFA('ab|cd', '', False)
    testNFA('ab|cd', 'ab', True)
    testNFA('ab|cd', 'cd', True)
    testNFA('ab|cd*', '', False)
    testNFA('ab|cd*', 'c', True)
    testNFA('ab|cd*', 'cd', True)
    testNFA('ab|cd*', 'cddddddd', True)
    testNFA('ab|cd*', 'ab', True)
    testNFA('((ab)|(cd))*', '', True)
    testNFA('((ab)|(cd))*', 'ab', True)
    testNFA('((ab)|(cd))*', 'cd', True)
    testNFA('((ab)|(cd))*', 'abab', True)
    testNFA('((ab)|(cd))*', 'abcd', True)
    testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True) #test your NFA:
    testUnion('ab','a','ab',True)
    testUnion('abc','a','abc',True)
    testUnion('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*','a','hijijklmmmmmmmmmmn',True)
    # testDFA('&','',True)
    # testDFA('a', '', False)
    # testDFA('a', 'a', True)
    # testDFA('a', 'aaa', False)
    # testDFA('ab', 'ab', True)
    # testDFA('ab', 'ba', False)
    # testDFA('abc', 'abc', True)
    # testDFA('abc', 'ab', False)
    # testDFA('a*', '', True)
    # testDFA('a*', 'a', True)
    # testDFA('a|c*', 'a', True)
    # testDFA('a|c*', 'ccc', True)
    # testDFA('a|c*', 'aa', False)
    # testDFA('(a*)|c', 'aa', True)
    # testDFA('((a*)c*)*', 'acacaaaccc', True)
    # testDFA('((a*)c*)*', 'acacacaacaaca', True)
    # testDFA('((a*)c*)*', 'cacaccacacac', True)
    # testDFA('((a*)c*)*', 'acacacaccccaca', True)
    # testDFA('((a*)c*)*', 'cacaacaccacac', True)
    # testDFA('a|b', '', False)
    # testDFA('a|b', 'a', True)
    # testDFA('a|b', 'b', True)
    # testDFA('a|b', 'ab', False)
    # testDFA('ab|cd', '', False)
    # testDFA('ab|cd', 'ab', True)
    # testDFA('ab|cd', 'cd', True)
    # testDFA('ab|cd*', '', False)
    # testDFA('ab|cd*', 'c', True)
    # testDFA('ab|cd*', 'cd', True)
    # testDFA('ab|cd*', 'cddddddd', True)
    # testDFA('ab|cd*', 'ab', True)
    # testDFA('((ab)|(cd))*', '', True)
    # testDFA('((ab)|(cd))*', 'ab', True)
    # testDFA('((ab)|(cd))*', 'cd', True)
    # testDFA('((ab)|(cd))*', 'abab', True)
    # testDFA('((ab)|(cd))*', 'abcd', True)
    # testDFA('((ab)|(cd))*', 'cdcdabcd', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    # testDFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)
    # testDFA('(a|b)*abb','aaaabb',True)
    testEquivalence('(a|b)*abb','(a|b)*abb', True)
pass
    
