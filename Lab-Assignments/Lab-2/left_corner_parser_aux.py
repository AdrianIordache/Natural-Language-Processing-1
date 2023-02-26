import nltk
import numpy as np 
from collections import deque

from nltk import CFG, Nonterminal

grammar_productions = """
S -> NP VP
S -> VP
NP -> DT NN
NP -> DT JJ NN
NP -> PRP
VP -> VBP NP
VP -> VBP VP
VP -> VBG NP
VP -> TO VP
VP -> VB
VP -> VB NP
NN -> "show" | "book"
PRP -> "I"
VBP -> "am"
VBG -> "watching"
VB -> "show"
DT -> "a" | "the"
MD -> "will" 
"""

grammar = nltk.CFG.fromstring(grammar_productions)
sentence = ['I', 'am', 'watching', 'a', 'show']

# rdp = nltk.RecursiveDescentParser(grammar)
# for tree in rdp.parse(sentence):
#     print(tree)

def find_productions_by_left_corners(grammar, N):
    return grammar.productions(rhs = N) # start with N e.g. ... -> N...

def bottom_up(word, top, grammar):
    aux = []
    deq = deque()

    start_productions = find_productions_by_left_corners(grammar, word)

    output = []
    for production in start_productions:
        deq.append(production)
        if production.lhs() == top:
            output.append([production])

    if len(output):
        return output

    #print("Aici")
    #print("Init deq: ", deq)
    while len(deq) != 0:
        curr_production = deq.popleft()
        
        #print("Current Prod: ", curr_production)
        #print("Deq after pop: ", deq)

        productions = find_productions_by_left_corners(grammar, curr_production.lhs())

        #print("New Productions for current: ", productions)

        aux.append((curr_production, len(productions)))

        #print("Aux list of results (prod, len): ", aux)

        while aux[-1][1] == 0: #clean aux list
            #print("!!!!!!!!!!! Intra: ", aux)
            aux.pop(-1)
            if len(aux):
                aux[-1] = (aux[-1][0], aux[-1][1]-1) 
            else:
                break

        #print("Aux list of results (prod, len) after clean: ", aux)

        for production in productions:
            if production.lhs() == top:
                #print("intra production.lhs() == top")
                aux.append((production, None))

                solution = []
                for elem in aux:
                    #print("Iterate solution: ", elem)
                    solution.append(elem[0])

                #print("Solution: ", solution)

                output.append(solution)

                #print("Aux list: ", aux)
                aux = aux[:1]
                #print("Aux list without last elem: ", aux)

            deq.appendleft(production)

        #print("Output deq: ", deq)
        #print("!!!!!!!!!!!!!!!!!!! END !!!!!!!!!!!!!!")

    if output == []:
        return False
    else:
        return output

def left_corner_parser(grammar, sentence):
    def left_corner_parser_(grammar, index, flag):
        rest = 0
        print("Flag: ", flag)
        productions = bottom_up(words[index], flag, grammar)
        print("Productions Init: ", productions)

        if productions == False:
            print("Iese")
            return False

        returnValue = True
        for productionList in productions:
            print("Production List", productionList)
            for production in productionList[1:]:
                print("Production: ", production)

                # if len(production.rhs()) == 1:
                #     print("Intra len(production.rhs()) == 1")
                #     continue # I'm ok, there is no need for top-down
                # else: # need top-down step

                if len(production.rhs()) > 1:
                    print("Intra len(production.rhs()) > 1")
                    for symbol in production.rhs()[1:]:
                        print("Symbol: ", symbol)
                        index += 1
                        print("Index: ", index)
                        if index >= len(words): #case for insufficient words
                            print("Intra index >= len(words)")
                            returnValue = False
                            break

                        returnValue = left_corner_parser_(grammar, index, symbol)
                        # if not rest:
                        #     returnValue = False
                        #     #print(index, symbol, production)
                        #     break
                        # else:
                        #     returnValue = True
            index -= 1
            if returnValue:
                print("!!!!!!!!!!!!!!!!!!!!!")
                print(productionList)
                break
        #print(index, flag, returnValue)
        return returnValue

    words = sentence.split()
    flag  = grammar.start()
    index = 0

    return left_corner_parser_(grammar, index, flag)

#print(bottom_up('am', Nonterminal('VP'), grammar))

#print(bottom_up("am", Nonterminal("VP"), grammar))
print(left_corner_parser(grammar, 'I am watching a show'))