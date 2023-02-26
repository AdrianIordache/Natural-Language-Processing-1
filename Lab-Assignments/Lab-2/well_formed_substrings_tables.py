import nltk
import numpy as np
import queue

from nltk import CFG, Nonterminal, Production
from nltk.tokenize import sent_tokenize, word_tokenize

def grammar_preprocessing(grammar_productions, display):
    valid, invalid = [], []
    for production in grammar.productions():
        if len(production.rhs()) == 2:
            valid.append(production)
        else:
            invalid.append(production)

    counter = 0
    while invalid:
        production = invalid[0]
        invalid = invalid[1 : ]
        
        if len(production.rhs()) > 2:
            generated = Production(production.lhs(), [production.rhs()[0], Nonterminal('FK{}'.format(counter))])
            valid.append(generated)

            generated = Production(Nonterminal('FK{}'.format(counter)), production.rhs()[1:])
            invalid.append(generated)

            counter += 1

        if len(production.rhs()) < 2:
            if isinstance(production.rhs()[0], Nonterminal):
                productions_next = grammar.productions(lhs = production.rhs()[0])
                for prod in productions_next:
                    generated = Production(production.lhs(), prod.rhs())
                    
                    if len(generated.rhs()) == 2 or isinstance(generated.rhs()[0], Nonterminal) == False:
                        valid.append(generated)
                    else:
                        invalid.append(generated)
            else:
                valid.append(production)

        if len(production.rhs()) == 2:
            valid.append(production)

    if display:
        for production in valid:
            print(production)

    return valid


grammar_productions = """  
S -> NP VP | TO VB
VP -> V NP | V NP PP | V S | V PP
PP -> P NP  
V -> "caught" | "ate" | "likes" | "like" | "chase" | "go"
NP -> Det N | Det N PP | PRP
Det -> "the" | "a" | "an" | "my" | "some"
N -> "mice" | "cat" | "dog" |  "school"
P -> "in" | "to" | "on"
TO -> "to"
PRP -> "I"  
"""

# grammar_productions = """
# S -> NP VP
# S -> VP
# NP -> DT NN
# NP -> DT JJ NN
# NP -> PRP
# VP -> VBP NP
# VP -> VBP VP
# VP -> VBG NP
# VP -> TO VP
# VP -> VB
# VP -> VB NP
# NN -> "show" | "book"
# PRP -> "I"
# VBP -> "am"
# VBG -> "watching"
# VB -> "show"
# DT -> "a" | "the"
# MD -> "will" 
# """

grammar_productions = """
    S -> RB S | NP VP PP | NP VP
    PP -> P NP
    NP -> Det N | Det J N | PRP
    VP -> V NP | V NP PP
    Det -> 'a' | 'the'
    RB ->  'Yesterday'
    J -> 'pink'
    N -> 'fridge' | 'elephant'
    V -> 'found'
    P -> 'in'
    PRP -> 'I'
"""

grammar = nltk.CFG.fromstring(grammar_productions)

productions = grammar_preprocessing(grammar, False)

grammar = CFG(grammar.start(), productions)

#print(grammar)

sentence = 'I like my dog'
#sentence = 'I am watching a show'
sentence = 'Yesterday I found a pink elephant in the fridge'
words = word_tokenize(sentence)

N = len(words)
T = np.ndarray(shape = (N + 1, N + 1), dtype = object)

for i in range(N + 1):
  for j in range(N + 1):
      T[i][j] = []

#print(T)

for i, word in enumerate(words):
  productions = grammar.productions(rhs = word)
  for production in productions:
      if len(production.rhs()) == 1:
          T[i][i + 1].append(production)

#print(T)


change = True
while change:
  change = False
  for i in range(N + 1):
      for k in range(N + 1):
          for j in range(N + 1):
              # print(i, k, j)
              productions_i = T[i][k]
              productions_j = T[k][j]
              #print(productions_i, productions_j)
              for production_i in productions_i:
                  for production_j in productions_j:
                      for production in grammar.productions():
                        if len(production.rhs()) == 2:
                          if production.rhs()[0] == production_i.lhs() and \
                                production.rhs()[1] == production_j.lhs() and \
                                    production not in T[i][j]:
                              T[i][j].append(production)
                              change = True



for i in range(N + 1):
    for j in range(N + 1):
        if T[i][j] == []: T[i][j] = None 

print(T)