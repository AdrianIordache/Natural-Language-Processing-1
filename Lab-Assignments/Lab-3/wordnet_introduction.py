import nltk
import wikipedia
import prettytable
import matplotlib.pyplot as plt

from nltk.corpus import wordnet

"""
Exercise 1
"Create a function that receives a word and prints the associated glosses for all the possible senses of that word 
(you must find all its corresponding synsets and print the gloss for each)."
"""

def generate_glosses_by_word(word):
	for i, syn in enumerate(wordnet.synsets(word)):
		print("Gloss {}: {}".format(i + 1, syn.definition()))

# generate_glosses_by_word("human")

"""
Exercise 2
"Create a function that receives two words as parameters. 
The function will check, using WordNet if the two words can be synonyms 
(there is at least one synset that contains the two words). 
If such synset is found, rint the gloss for that synset."
"""

def check_synonyms(word_1, word_2):
	are_synonyms = False
	for syn in wordnet.synsets(word_1):
		if syn in wordnet.synsets(word_2):
			print("Definition: {}".format(syn.definition()))
			are_synonyms = True

	if are_synonyms == False:
		print("Words: {}, {} are not synonyms".format(word_1, word_2))
	else:
		print("Words: {}, {} are synonyms".format(word_1, word_2))

# check_synonyms("help", "assistance")

"""
Exercise 3
"Create a function that receives a synset object and returns a tuple with 2 lists. 
The first list contains the holonyms (all types of holonyms) and the second one the meronyms (all types). 
Find a word that has either holonyms or meronyms of different types. 
Print them separately (on cathegories of holonyms/meronyms) and then all together using the created function 
(in order to check that it prints them all)."
"""

def generate_holonyms_and_meronyms(synset):
	holonyms = synset.part_holonyms() + synset.substance_holonyms() + synset.member_holonyms()
	meronyms = synset.part_meronyms() + synset.substance_meronyms() + synset.member_meronyms()
	return (holonyms, meronyms)

# word = 'animal'
# synset = wordnet.synsets(word)[0]
# print("Part holonyms for the word {}: {}".format(word, synset.part_holonyms()))
# print("Substance holonyms for the word {}: {}".format(word, synset.substance_holonyms()))
# print("Member holonyms for the word {}: {}".format(word, synset.member_holonyms()))
# print(); print();
# print("Part meronyms for the word {}: {}".format(word, synset.part_meronyms()))
# print("Substance meronyms for the word {}: {}".format(word, synset.substance_meronyms()))
# print("Member meronyms for the word {}: {}".format(word, synset.member_meronyms()))
# print(); print();
# (holonyms, meronyms) = generate_holonyms_and_meronyms(synset)
# print("All type of holonyms for the word {}: {}".format(word, holonyms))
# print("All type of meronyms for the word {}: {}".format(word, meronyms))


"""
Exercise 4
"Create a function that for a given synset, prints the path of hypernyms 
(going to the next hypernym, and from that hypernym to the next one and so on, until it reaches the root)."
"""

def generate_all_hypernyms(synset):
	print("Current synset: {}".format(synset))
	synset = synset.hypernyms()
	if synset != []: generate_all_hypernyms(synset[0])

# word = 'animal'
# synset = wordnet.synsets(word)[0]
# generate_all_hypernyms(synset)

"""
Exercise 5
"Create a function that receives two synsets as parameters. 
We consider d1(k) the length of the path from the first word to the hypernym k 
(the length of the path is the number of hypernyms it goes through, to reach k) 
and d2(k) the length of the path from the second word to the hypernym k. 
The function will return the list of hypernyms having the property that d1(k)+d2(k) is minimum"
"""

pass

"""
Exercise 6
"Create a function that receives a synset object and a list of synsets 
(the list must contain at least 5 elements). 
The function will return a sorted list. 
The list will be sorted by the similarity between the first synset and the synsets in the list. 
For example (we consider we take the firs synset for each word) 
we can test for the word cat and the list: animal, tree, house, object, public_school, mouse."
"""

def similarity_sort(synset, list_of_synsets):
	sims = [(syn, synset.path_similarity(syn)) for syn in list_of_synsets]
	return sorted(sims, key = lambda x: x[1], reverse = True)

# word = 'cat'
# list_of_words = ['animal', 'tree', 'house', 'object', 'public_school', 'mouse']
# synset = wordnet.synsets(word)[0]
# list_of_synsets = [wordnet.synsets(word)[0] for word in list_of_words]
# sims = similarity_sort(synset, list_of_synsets)
# print("List of synsets sorted by similarity")
# print([sim[0] for sim in sims])
# print(sims)

"""
Exercise 7
"Create a function that checks if two synsets can be indirect meronyms for the same synset. 
An indirect meronym is either a part of the givem element or a part of a part of the given element 
(and we can exten this relation as being part of part of part of etc....). 
This applies to any type of meronym. "
"""

def check_indirect_meronyms(synset_1, synset_2):
	def generate_meronyms(synset):
		list_of_meronyms = synset.part_meronyms() + synset.substance_meronyms() + synset.member_meronyms()
		meronyms = set(list_of_meronyms)
		while True:
			meronyms_length = len(meronyms)

			next_level_meronyms = []
			for meronym in meronyms:
				next_level_meronyms.extend(meronym.part_meronyms())
				next_level_meronyms.extend(meronym.substance_meronyms())
				next_level_meronyms.extend(meronym.member_meronyms())

			meronyms.update(next_level_meronyms)
			updated_length = len(meronyms)

			if meronyms_length == updated_length:
				break

		return meronyms

	meronyms_1 = generate_meronyms(synset_1)
	meronyms_2 = generate_meronyms(synset_2)

	common_meronyms = [meronym for meronym in meronyms_1 if meronym in meronyms_2]

	if len(common_meronyms) == 0:
		print("The given synsets are not indirect meronyms")
		return False
	else:
		print("The given synsets are indirect meronyms")
		print("Common synsets: {}".format(common_meronyms))
		return True

# word_1 = 'water'
# word_2 = 'earth'
# synset_1 = wordnet.synsets(word_1)[0]
# synset_2 = wordnet.synsets(word_2)[0]
# check_indirect_meronyms(synset_1, synset_2)


"""
Exercise 8
"Print the synonyms and antonyms of an adjective (for example, "beautiful"). 
If it's polisemantic, print them for each sense, also printing the gloss for that sense (synset)."
"""

def generate_synonyms_and_antonyms(word):
	for synset in wordnet.synsets(word):
		if len(wordnet.synsets(word)) > 1:
			print('Word Gloss: {}'.format(synset.definition()))
		
		synonyms = [syn.lemma_names() for syn in synset.similar_tos()]
		antonyms = [syn.name() for syn in synset.lemmas()[0].antonyms()]

		print("List of Synonyms for current gloss")
		print(synonyms)
		print("List of Anotnyms for current gloss")
		print(antonyms)

# generate_synonyms_and_antonyms('beautiful')