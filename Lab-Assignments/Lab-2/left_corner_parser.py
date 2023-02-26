import nltk
import numpy as np 
from collections import deque

from nltk import CFG, Nonterminal

def generate_left_corner_table(grammar, display = False):
	left_corner_table = {}
	for i, production in enumerate(grammar_productions.split('\n')):
		if production == '': continue
		[symbol, nonterminals]  = production.split(" -> ")
		
		if "|" in nonterminals:
			nonterminals = nonterminals.split("|")
			nonterminals = ",".join(nonterminals)

		nonterminals = nonterminals.split(" ")
		if ',' in nonterminals:
			nonterminals = ["".join(nonterminals)]


		if symbol not in left_corner_table:
			left_corner_table.update({symbol: nonterminals[0]})
		else:
			if nonterminals[0] not in left_corner_table[symbol].split(','):
				left_corner_table[symbol] += "," + nonterminals[0]

	if display:
		for key, value in left_corner_table.items():
			print(f"{key} -> {value}")

	return left_corner_table

def iterate_backwards(left_corner_table, word, terminal):
	path = []
	search = word

	while search != terminal:
		path.append(search)
		changed = False
		for key, value in left_corner_table.items():
			# print("S: ", search)
			# print("V: ", value)
			if search in value:
				# print("intra")
				changed = True
				search = key

		if changed == False:
			return False

	path.append(search)
	
	return path


def is_left_corner(rule, symbol):
	if rule == '': return False
	[_, nonterminals] = rule.split(" -> ")

	if symbol in nonterminals.split(" ")[0]:
		return True

	return False


def generate_prediction(grammar_productions, symbol):
	predictions = []
	for rule in grammar_productions.split("\n"):
		if rule == '': continue
		if is_left_corner(rule, symbol) == True:
			[_, nonterminals] = rule.split(" -> ")
			nonterminals = nonterminals.split(" ")

			if len(nonterminals) > 1:
				predictions.append(nonterminals[1])

	return predictions


def left_corner_parser(left_corner_table, start, sentence):
	def left_corner_parser_(left_corner_table, nonterminal, words, current):
		if current >= len(words): return True

		path = iterate_backwards(left_corner_table, words[current], nonterminal)

		if path == False: return False
			
		print(path)

		left_corner = path[-2]

		predictions = generate_prediction(grammar_productions, left_corner)

		for prediction in predictions:
			value = left_corner_parser_(left_corner_table, prediction, words, current + 1)
			if value == True:
				break

		return True
	
	idx   = 0
	words = sentence.split(" ")
	words = ['"' + word + '"' for word in words]

	left_corner_parser_(left_corner_table, start, words, idx)


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

# grammar_productions = """
# S -> NP VP 
# S -> TO VB
# VP -> V NP 
# VP -> V NP PP 
# VP -> V S 
# VP -> V PP
# PP -> P NP  
# V -> "caught" | "ate" | "likes" | "like" | "chase" | "go"
# NP -> Det N 
# NP -> Det N PP 
# NP -> PRP
# Det -> "the" | "a" | "an" | "my" | "some"
# N -> "mice" | "cat" | "dog" |  "school"
# P -> "in" | "to" | "on"
# TO -> "to"
# PRP -> "I" 
# """


left_corner_table = generate_left_corner_table(grammar_productions, False)

start = "S"
sentence = "I am watching a show"
# sentence = "I like my dog"

left_corner_parser(left_corner_table, start, sentence)



