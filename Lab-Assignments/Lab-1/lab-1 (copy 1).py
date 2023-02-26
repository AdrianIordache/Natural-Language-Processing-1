import os.path
import prettytable
import urllib.request

from os import path
from itertools import islice
from collections import defaultdict 

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.collocations import BigramCollocationFinder, TrigramCollocationFinder
from nltk.metrics import BigramAssocMeasures, TrigramAssocMeasures
from nltk.corpus import stopwords 
from word2number import w2n
from num2words import num2words as n2w

nltk.download('punkt')

# 1) Download text
STOPWORDS = set(stopwords.words('english')) 
URL = "https://www.gutenberg.org/cache/epub/42671/pg42671.txt"
TITLE = "PRIDE & PREJUDICE."
PATH_TO_DATA = "data.txt"

text = None
if path.exists(PATH_TO_DATA):
	with open(PATH_TO_DATA, "r") as f:
		text = f.read()
else:
	request = urllib.request.urlopen(URL)
	text = request.read()
	with open(PATH_TO_DATA, "wb") as f:
		f.write(text)

# 2) 'Remove the header'
start = text.find(TITLE)
text  = text[start : ]
# print(text[:200])

# 3) 'Print number of sentences in the text. Print the average length (number of words) of a sentence.'
sentences = sent_tokenize(text)
words = word_tokenize(text)

print("Example of sentences in text: ")
print(sentences[:10])
print("Example of words in text: ")
print(words[:10])

print("Number of sentences in text: {}".format(len(sentences)))
print("Average length (number of words) of a sentence: {}".format(len(words) / len(sentences)))

# 4) 'Find the collocations in the text (bigram and trigram), printed only once.'
filter_stops = lambda word: word in STOPWORDS or len(word) < 3 

biagram_collocation = BigramCollocationFinder.from_words(words) 
biagram_collocation.apply_word_filter(filter_stops) 
biagram_collocation.apply_freq_filter(3) 
print("Most common bigrams: ")
print(set(biagram_collocation.nbest(BigramAssocMeasures.likelihood_ratio, 30)))

trigram_collocation = TrigramCollocationFinder.from_words(words) 
trigram_collocation.apply_word_filter(filter_stops) 
trigram_collocation.apply_freq_filter(3) 
print("Most common trigrams: ")
print(set(trigram_collocation.nbest(TrigramAssocMeasures.likelihood_ratio, 30)))


# 5) 'Create a list of all the words (in lower case) from the text, without the punctuation'
lower = set([word.lower() for word in words if word.isalnum()])
# print(lower)

# 6) 'Print the first N most frequent words (alphanumeric strings) together with their number of appearances.'
N = 10

lower = [word.lower() for word in words if word.isalnum()]
appearances = {word : 0 for word in lower}
for word in lower:
	appearances[word] += 1

appearances = dict(sorted(appearances.items(), key = lambda x: x[1], reverse = True))
N_items = list(islice(appearances.items(), N))
print("First {} most frequent words".format(N))
print(N_items)

# 7) 'Remove stopwords and assign result to variable lws'
lws = [word for word in lower if word not in STOPWORDS]
print(lws[:10])

# 8) 'Apply stemming (Porter) on the list of words (lws). Print the first 200 words. Do you see any words that don't appear in the dictionary?'
N = 200
ps = nltk.PorterStemmer()
stem = [(word, ps.stem(word)) for word in lws]

for i, (word, stemm) in enumerate(stem):
	print(word + "\t" * 5 + stemm)
	if i >= N: break


# 9) 'Print a table of three columns... '
NW = 500
table = prettytable.PrettyTable(['Original', 'Porter', 'Lancaster', 'Snowball'])
ps = nltk.PorterStemmer()
ls = nltk.LancasterStemmer()
ss = nltk.SnowballStemmer('english')

rows = [(word, ps.stem(word), ls.stem(word), ss.stem(word)) for word in lws if ps.stem(word) != ls.stem(word) or ps.stem(word) != ss.stem(word) or ls.stem(word) != ss.stem(word)]

for (i, row) in enumerate(rows):
	table.add_row(row)
	if i > NW:
		break

print(table)

# 10) 'Print a table of two columns...'
NW = 500
table = prettytable.PrettyTable(['Original', 'Snowball', 'WordNetLemmatizer'])

ss  = nltk.SnowballStemmer("english")
wnl = WordNetLemmatizer()

unique = [*set(lws)]
rows = [(word, ss.stem(word), wnl.lemmatize(word, pos = 'v')) for word in unique if ss.stem(word) != wnl.lemmatize(word, pos = 'v')]

for (i, row) in enumerate(rows):
	table.add_row(row)
	if i > NW:
		break

print(table)

# 11) 'Print the first N most frequent lemmas (after the removal of stopwords) together with their number of appearances.'
N = 10

lemmas = [wnl.lemmatize(word, pos = 'v') for word in lws]

counter = {word : 0 for word in lemmas}
for word in lemmas:
	counter[word] += 1

counter = dict(sorted(counter.items(), key = lambda x: x[1], reverse = True))
N_items = list(islice(counter.items(), N))
print("First {} most frequent words after lemmatization".format(N))
print(N_items)

# 12) 'Change all the numbers from lws into words. Print the number of changes, and also the portion of list that contains first N changes (for example N = 10).'
N = 10

change = 0
keep = None
for i, word in enumerate(lws):
	if word.isdigit():
		lws[i] = n2w(word)
		#print(lws[i])
		change += 1
		if change == N:
			keep = i

print("Number of changes: {}".format(change))
print(lws[: keep])

# 13) 'Create a function that receives an integer N and a word W as parameter..'

N = 3
W = ["cat"]
text = "I have two dogs and a cat. Do you have pets too? My cat likes to chase mice. My dogs like to chase my cat."

def clean(text: str = None) -> str:
	wnl = WordNetLemmatizer()

	text = word_tokenize(text)
	text = [word.lower() for word in text if word.isalnum()]
	text = [word for word in text if word not in STOPWORDS]	
	text = [wnl.lemmatize(word, pos = 'v') for word in text]

	return text

def find_concurance_text(W: [str], N: int, text: str) -> [str]:
	words = clean(text)

	word_occurances = []
	for w in W:
		occurances = []
		w = clean(w)[0]

		left  = N // 2
		right = N // 2 + 1

		idxs = [idx for idx, word in enumerate(words) if w == word]

		for idx in idxs:
			start = max(idx - left, 0)
			end   = min(idx + right, len(words))
			selected = words[start : end]
			occurances.append(selected)

		word_occurances.append(occurances)

	return word_occurances


def find_concurance_sentence(W: [str], N: int, text: str) -> [str]:
	texts = sent_tokenize(text)

	occurances_sentences = []
	for text in texts:
		occurances_text = find_concurance_text(W, N, text)
		occurances_sentences.append(occurances_text)

	return occurances_sentences


print("Occurances in text, no sentence delimitaion")
occurances_text = find_concurance_text(W, N, text)
print(occurances_text)

print("Occurances in sentences, with sentence delimitaion")
occurances_sentences = find_concurance_sentence(W, N, text)
print(occurances_sentences)