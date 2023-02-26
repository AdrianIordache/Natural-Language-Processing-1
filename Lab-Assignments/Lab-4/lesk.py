import os
import nltk
import wikipedia
import prettytable
import matplotlib.pyplot as plt

from nltk.wsd import lesk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

STOPWORDS = stopwords.words('english')

"""
Exercise 1
Implement Original Lesk algorithm with the help of a function that computes the score for two given glosses. 
For a given text and a given word, try to find the sense of that word, considering the Lesk measure. 
Print the definition for that sense (synset). 
Check your result with the already implemented (simplified) lesk algorithm in nltk. 
You may have different results, as the simplified Lesk algorithm compares the target word glosses with the words from the context (not their definitions). 
"""
class Lesk:
    def compute_score(gloss_1, gloss_2):
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
            
        gloss_words_1, gloss_words_2 = word_tokenize(gloss_1), word_tokenize(gloss_2)

        words_1 = [word.lower() for word in gloss_words_1 if word.isalnum() and word not in STOPWORDS]
        words_2 = [word.lower() for word in gloss_words_2 if word.isalnum() and word not in STOPWORDS]

        lemmatizer = WordNetLemmatizer()
        words_and_pos_1 = [(word, get_wordnet_pos(nltk.tag.pos_tag([word])[0][1])) for word in words_1]
        words_and_pos_2 = [(word, get_wordnet_pos(nltk.tag.pos_tag([word])[0][1])) for word in words_2]

        lemmatized_1 = [lemmatizer.lemmatize(word, tag) for (word, tag) in words_and_pos_1]
        lemmatized_2 = [lemmatizer.lemmatize(word, tag) for (word, tag) in words_and_pos_2]

        # print(lemmatized_1)
        # print(lemmatized_2)

        score = sum([1 for word_1 in lemmatized_1 for word_2 in lemmatized_2 if word_1 == word_2])
        return score

    def extract_sense_from_context(word, context):
        words_in_context = word_tokenize(context)
        synsets = wordnet.synsets(word)

        best_gloss = None
        maximum_score = 0

        for synset in synsets:
            gloss_score = 0
            for word_in_context in words_in_context:
                for word_in_context_gloss in wordnet.synsets(word_in_context):
                    gloss_score += Lesk.compute_score(word_in_context_gloss.definition(), synset.definition())

            print("Current definition '{}' with score: {}".format(synset.definition(), gloss_score))
            if gloss_score > maximum_score:
                best_gloss = synset
                maximum_score = gloss_score

        return best_gloss


# word = 'school'
# context = 'Students enjoy going to school, studying and reading books'

# best_gloss = Lesk.extract_sense_from_context(word, context)
# print("Sense Predicted by implemented lesk: ", best_gloss.definition())
# nltk_synset = lesk(nltk.word_tokenize(context), word,'n')
# print("Sense Predicted by nltk lesk: ", nltk_synset.definition())


"""
Exercise 2
Implement extended Lesk algorithm. 
Experiment with the measure by using different WordNet relations in computing the score. 
For a list of 7-10 synsets, print the measure for each pair of synsets 
(without repeating the synsets) with five different sets of relations taken into acount in measuring the score. 
Write the observations. Just like in the former exercise, try to obtain the word sense for the given text and word (and print its definition). 
Can you find a text and word where simple Lesk gives the wrong answer, however extended Lesk gives the right answer?
"""


class ExtendedLesk:
    def extend_sense(synset):
        extended_glosses = []

        hypernyms  = synset.hypernyms()
        hyponyms   = synset.hyponyms()
        meronyms   = synset.substance_meronyms() + synset.part_meronyms() + synset.part_meronyms()
        holonyms   = synset.substance_holonyms() + synset.part_holonyms() + synset.part_holonyms()
        troponyms  = synset.entailments()
        attributes = synset.attributes()
        similar_to = synset.similar_tos()
        also_see   = synset.also_sees()

        extended_glosses.append(synset.definition())
        extended_glosses.append(' '.join([word.definition() for word in hypernyms]))
        extended_glosses.append(' '.join([word.definition() for word in hyponyms]))
        extended_glosses.append(' '.join([word.definition() for word in meronyms]))
        extended_glosses.append(' '.join([word.definition() for word in holonyms]))
        extended_glosses.append(' '.join([word.definition() for word in troponyms]))
        extended_glosses.append(' '.join([word.definition() for word in attributes]))
        extended_glosses.append(' '.join([word.definition() for word in similar_to]))
        extended_glosses.append(' '.join([word.definition() for word in also_see]))

        return extended_glosses

    def compute_score(gloss_1, gloss_2):
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
            
        gloss_words_1, gloss_words_2 = word_tokenize(gloss_1), word_tokenize(gloss_2)

        words_1 = [word.lower() for word in gloss_words_1 if word.isalnum() and word not in STOPWORDS]
        words_2 = [word.lower() for word in gloss_words_2 if word.isalnum() and word not in STOPWORDS]

        lemmatizer = WordNetLemmatizer()
        words_and_pos_1 = [(word, get_wordnet_pos(nltk.tag.pos_tag([word])[0][1])) for word in words_1]
        words_and_pos_2 = [(word, get_wordnet_pos(nltk.tag.pos_tag([word])[0][1])) for word in words_2]

        lemmatized_1 = [lemmatizer.lemmatize(word, tag) for (word, tag) in words_and_pos_1]
        lemmatized_2 = [lemmatizer.lemmatize(word, tag) for (word, tag) in words_and_pos_2]

        if len(lemmatized_1) > len(lemmatized_2):
            lemmatized_1, lemmatized_2 = lemmatized_2, lemmatized_1

        score = 0

        # lemmatized_1.append('school')
        # print(lemmatized_1)
        # print(lemmatized_2)

        max_sequence_size = len(lemmatized_1)
        for sequence_size in range(max_sequence_size, 0, -1):
            # print('size: ', sequence_size)

            for i in range(0, len(lemmatized_1), 1):
                patch_1 = lemmatized_1[i : i + sequence_size]
                if len(patch_1) != sequence_size: continue
                # print("i:", i)
                # print('patch 1:', lemmatized_1[i : i + sequence_size])
                
                for j in range(0, len(lemmatized_2), 1):
                    patch_2 = lemmatized_2[j : j + sequence_size]
                    if len(patch_2) != sequence_size: continue
                    # print('j:', j)
                    # print('patch 2:', lemmatized_2[j: j + sequence_size])
                    if patch_1 == patch_2:
                        # print("found and cut")
                        score += sequence_size ** 2
                        lemmatized_1 = lemmatized_1[: i] + lemmatized_1[i + sequence_size :]
                        lemmatized_2 = lemmatized_2[: j] + lemmatized_2[j + sequence_size :]
                        # print('lemmatized_1 cut: ', lemmatized_1)
                        # print('lemmatized_2 cut: ', lemmatized_2)

        return score

    def extract_sense_from_context(word, context):
        words_in_context = word_tokenize(context)
        synsets = wordnet.synsets(word)
        
        best_gloss = None
        maximum_score = 0

        for synset in synsets:
            gloss_score = 0
            extended_glosses = ExtendedLesk.extend_sense(synset)
            for word_in_context in words_in_context:
                for word_in_context_gloss in wordnet.synsets(word_in_context):
                    extended_context_gloss = ExtendedLesk.extend_sense(word_in_context_gloss)
                    for gloss_1 in extended_glosses:
                        for gloss_2 in extended_context_gloss:
                            gloss_score += ExtendedLesk.compute_score(gloss_1, gloss_2)
                            # return None


            print("Current definition '{}' with score: {}".format(synset.definition(), gloss_score))
            if gloss_score > maximum_score:
                best_gloss = synset
                maximum_score = gloss_score

        return best_gloss


# synsets = wordnet.synsets('school')
# for i in range(len(synsets)):
#     for j in range(i, len(synsets)):
#         if i != j:
#             extended_1 = ExtendedLesk.extend_sense(synsets[i])
#             extended_2 = ExtendedLesk.extend_sense(synsets[j])
#             score = 0

#             for gloss_1 in extended_1:
#                 for gloss_2 in extended_2:
#                     score += ExtendedLesk.compute_score(gloss_1, gloss_2)
            
#             print("For synsets '{}' and '{}' we have the score: {}" \
#                 .format(synsets[i].definition(), synsets[j].definition(), score))

# word = 'school'
# context = 'Students enjoy going to school, studying and reading books'
# best_gloss = ExtendedLesk.extract_sense_from_context(word, context)

# print("Sense Predicted by implemented extended lesk: ", best_gloss.definition())
# nltk_synset = lesk(nltk.word_tokenize(context), word,'n')
# print("Sense Predicted by nltk lesk: ", nltk_synset.definition())