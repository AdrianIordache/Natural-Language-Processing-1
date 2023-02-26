import nltk
import wikipedia
import prettytable
import matplotlib.pyplot as plt

from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget

from typing import List
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.parse.generate import generate
from nltk.tokenize import word_tokenize, sent_tokenize

what = lambda x: print(nltk.help.upenn_tagset(x))

"""
Exercise 1:
Choose a wikipedia article. You will download and acces the article using this python module: wikipedia. 
Use the content property to extract the text. 
Print the title of the article and the first N=200 words from the article to verify that all works well. 
Print the POS-tagging for the first N=20 sentences.
"""

wikipedia.set_lang('en')
wikipedia_page = wikipedia.page("COVID-19 pandemic")
content = wikipedia_page.content

N = 200
print("Wikipedia Page Title: {}".format(wikipedia_page.title))
words = word_tokenize(content)
print(words[: N])

N = 20
sentences = sent_tokenize(content)
pos_taggs = [nltk.pos_tag(word_tokenize(sentence)) for (i, sentence) in enumerate(sentences) if i < N]
print("POS-tagging for the first N sentences")
print(pos_taggs)


"""
Exercise 2:
Create a function that receives a part of speech tag and returns a list with all the words from the text 
(can be given as a parameter too) that represent that part of speech. 
Create a function that receives a list of POS tags and returns a list with words having any of the given POS tags 
(use the first function in implementing the second one).
"""

def get_words_part_of_speech(content: str = None, tag: str = None) -> List[str]:
    sentences = sent_tokenize(content)
    taggs = [nltk.pos_tag(word_tokenize(sentence)) for sentence in sentences]
    return [word for tagg_sentence in taggs for (word, tagg) in tagg_sentence if tagg == tag]

def get_words_parts_of_speech(content: str = None, tags: List[str] = None) -> List[str]:
    result = []
    for pos in tags:
        result.extend(get_words_part_of_speech(content, pos))
    return result

print("Selected words by a single part of speech")
print(get_words_part_of_speech(content, "CD")[:20])
print("Selected words by multiple part of speech")
print(get_words_parts_of_speech(content, ["DT", "CD"])[:50])


"""
Exercise 3:
Use the function above to print all the nouns (there are multiple tags for nouns), 
and, respectively all the verbs (corresponding to all verb tags). 
Also, print the percentage of content words (noun+verbs) from the entire text
"""

nouns = get_words_parts_of_speech(content, ["NN", "NNP", "NNPS", "NNS"])
verbs = get_words_parts_of_speech(content, ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"])

print("All nouns from text")
print(nouns[:50])

print("All verbs from text")
print(verbs[:50])

print("The percent of (nouns + verbs) from all text is: {}%".format((len(nouns) + len(verbs)) * 100 / len(word_tokenize(content))))


"""
Exercise 4:
Print a table of four columns. The columns will be separated with the character "|". 
The head of the table will be: Original word | POS | Simple lemmatization | Lemmatization with POS that will compare 
the results of lemmatization (WordNetLemmatizer) without giving the part of speech and the lemmatization with the given part of speech for each word. 
The table must contain only words that give different results for the two lemmatizations (for example, the word "running" - without POS, 
the result will always be running, but with pos="v" it is "run"). 
The table will contain the results for the first N sentences from the text (each row corresponding to a word). 
Try to print only distinct results inside the table 
(for example, if a word has two occurnces inside the text, and matches the requirments for appearing in the table, it should have only one corresponding row).
"""

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

N = 5
table = prettytable.PrettyTable(["Original word", "POS", "Simple lemmatization", "Lemmatization with POS"])
lemmatizer = WordNetLemmatizer()
sentences = [sentence for (i, sentence) in enumerate(sent_tokenize(content)) if i < N]
words_and_pos = [(word, get_wordnet_pos(nltk.tag.pos_tag([word])[0][1])) for sentence in sentences for word in word_tokenize(sentence)]

words_and_pos = list(set(words_and_pos))

for word, tag in words_and_pos:
    simple_lemmatize = lemmatizer.lemmatize(word)
    pos_lemmatize = lemmatizer.lemmatize(word, tag) 

    if simple_lemmatize != pos_lemmatize:
        table.add_row([word, tag, simple_lemmatize, pos_lemmatize])

print(table)


"""
Exercise 5:
Print a graphic showing the number of words for each part of speech. 
If there are too many different parts of speech, you can print only those with a higher number of corresponding words.
"""

sentences = sent_tokenize(content)
pos_taggs = [nltk.pos_tag(word_tokenize(sentence)) for (i, sentence) in enumerate(sentences)]

counter = {tag : 0 for sentence in pos_taggs for word, tag in sentence}
for sentence in pos_taggs:
    for word, tag in sentence:
        counter[tag] += 1

plt.figure(figsize = (24, 9))
plt.bar(range(len(counter)), list(counter.values()), align = 'center')
plt.xticks(range(len(counter)), list(counter.keys()))
plt.xlabel("Part of speech tag")
plt.ylabel("No. of words")
plt.show()


"""
Exercise 6:
Create your own grammar with different terminal symbols. 
Apply recursive descent parsing on a sentence with at least 5 different parts of speech and a tree of at least level 4.
"""

grammar_productions = """  
S -> SB VB ADV
SB -> PN | SC | SP
PN -> PP | PNP
VB -> CJ VBI | VBP | VBN
ADV -> CJ VBI UDN
UDN -> LA SC
LA -> 'la'
SC -> 'magazin'
VBI -> 'merg' 
PP -> 'Eu'
PNP -> 'ma'
VBP -> 'vreau'
CJ -> 'sa'
"""

sentence = "Eu vreau sa merg la magazin"

grammar = nltk.CFG.fromstring(grammar_productions)

# print(grammar)
# for sentence in generate(grammar, n=10):
#     print(' '.join(sentence))

words = word_tokenize(sentence)
#print(words)

# RecursiveDescentParser, ShiftReduceParser
rdp = nltk.RecursiveDescentParser(grammar)
for tree in rdp.parse(words):
    print(tree)

"""
Exercise 7:
Apply shift reduce parsing on the same sentence and check programatically if the two trees are equal. 
Find a sentence with equal trees and a sentence with different results 
(we consider the tree different even when it has no sollution for one of the parsers, but has for the other). 
"""


sentence = "Eu vreau sa merg la magazin"
words = word_tokenize(sentence)

rdp = nltk.RecursiveDescentParser(grammar)
srp = nltk.ShiftReduceParser(grammar)

tree1 = None
for tree in rdp.parse(words):
    tree1 = tree

print(type(tree1))

tree2 = None
for tree in srp.parse(words):
    tree2 = tree

print(type(tree2))

if tree1 == tree2:
    print("Trees are the same")
else:
    print("Trees are different")