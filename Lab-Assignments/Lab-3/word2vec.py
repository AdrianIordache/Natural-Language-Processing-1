import nltk
import spacy
import string
import gensim
import wikipedia
import prettytable
import numpy as np
import matplotlib.pyplot as plt

from nltk.corpus import wordnet
from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize, sent_tokenize

from sklearn.cluster import KMeans

PATH_TO_MODEL = 'GoogleNews-vectors-negative300.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(PATH_TO_MODEL, binary = True)

wikipedia.set_lang('en')
wikipedia_page = wikipedia.page("Generative adversarial network")
content = wikipedia_page.content

print("Wikipedia Page Title: {}".format(wikipedia_page.title))

table = str.maketrans('', '', string.punctuation)
content = content.translate(table)

words = word_tokenize(content)
sentences = sent_tokenize(content)
print("Number of words in article: {}".format(len(words)))
print("Number of sentences in article: {}".format(len(sentences)))

"""
Use a pretrained Word2vec model (Google news). 
Choose a short English text (about 400-500 words). 
For example you can take a wikipedia article or book excerpt.
The text must also contain proper nouns. Solve the following tasks:"""


"""
Exercise 1
"Print the number of words in the model's vocabulary."
"""

found = [1 for word in words if word in model.vocab]
print("Number of words in article that were found in vocabulary: {}".format(sum(found)))

"""
Exercise 2
"Print all the words in the text that do not appear in the model's vocabulary."
"""

not_found = [word for word in words if word not in model.vocab]
print("Words that are not in the model vocabulary")
print(not_found)

"""
Exercise 3
"Which are the two most distant words in the text, and which are the closest? Print the distance too."
"""

min_similarity = np.inf
max_similarity = -np.inf

far_words = None
close_words = None
for word_1 in words:
	if word_1 not in model.vocab: continue
	for word_2 in words:
		if word_2 not in model.vocab: continue

		if word_1 == word_2: continue
		similarity = model.similarity(word_1, word_2)

		if similarity > max_similarity:
			max_similarity = similarity
			close_words = (word_1, word_2)

		if similarity < min_similarity:
			min_similarity = similarity
			far_words = (word_1, word_2)

print("The closest two words are ({}, {}) with a similarity of {}".format(close_words[0], close_words[1], max_similarity))
print("The most distant two words are ({}, {}) with a similarity of {}".format(far_words[0], far_words[1], min_similarity))	


"""
Exercise 4
"Using NER (Named Entity Recognition) find the named entities in the text. Print the first 5 most similar words to them both in upper and lowercase."
"""

nlp = spacy.load('en_core_web_sm')

for sentence in sentences:
	doc = nlp(sentence)
	for entity in doc.ents:
		print("Entity Found: {}".format(entity))
		lower_entity_similarity = [(word, model.similarity(word, entity.text.lower())) for word in words \
								if word != entity.text and word in model.vocab and entity.text.lower() in model.vocab ]

		upper_entity_similarity = [(word, model.similarity(word, entity.text.upper())) for word in words \
								if word != entity.text and word in model.vocab and entity.text.upper() in model.vocab ]

		print('Most similar 5 words for the entity: "{}" (lowercase)'.format(entity.text.lower()))
		lower_entity_similarity = sorted(lower_entity_similarity, key = lambda x: x[1], reverse = True)[: 5]
		print("Entity Not in model.vocab" if len(lower_entity_similarity) == 0 else lower_entity_similarity)

		print('Most similar 5 words for the entity: "{}" (uppercase)'.format(entity.text.upper()))
		upper_entity_similarity = sorted(upper_entity_similarity, key = lambda x: x[1], reverse = True)[: 5]
		print("Entity Not in model.vocab" if len(upper_entity_similarity) == 0 else upper_entity_similarity)


""" The Exercise can be interpreted in two ways (Second Method below) """

for sentence in sentences:
	doc = nlp(sentence)
	for entity in doc.ents:
		print("Entity Found: {}".format(entity))
		entity_similarity = [(word, model.similarity(word, entity.text)) for word in words \
								if word != entity.text and word in model.vocab and entity.text in model.vocab ]

		print('Most similar 5 words for the entity: "{}"'.format(entity.text))
		entity_similarity = sorted(entity_similarity, key = lambda x: x[1], reverse = True)[: 5]
		
		if len(entity_similarity) == 0:
			print("Entity Not in model.vocab")
			continue

		print([word.lower() for word, _ in entity_similarity])
		print([word.upper() for word, _ in entity_similarity])


"""
Exercise 5
"Print the clusters of words that are the most similar in the text (you can use sklearn's Kmeans) based on their vectors in the model."
"""

embeddings = [model.get_vector(word) for word in words if word in model.vocab]
kmeans = KMeans(n_clusters = 5, random_state = 42).fit(embeddings)
# predictions = [(word, cluster) for word, cluster in zip(words, kmeans.labels_)]

THRESHOLD = 0.75
for word_1 in words:
	if word_1 not in model.vocab: continue
	for word_2 in words:
		if word_2 not in model.vocab: continue

		if word_1 == word_2: continue
		similarity = model.similarity(word_1, word_2)

		if similarity > THRESHOLD:
			print('Words "{}", "{}" with similarity {} and clusters predicted {}, {}' \
				.format(word_1, word_2, similarity, kmeans.predict(model.get_vector(word_1).reshape(1, -1))[0], kmeans.predict(model.get_vector(word_2).reshape(1, -1))[0]))