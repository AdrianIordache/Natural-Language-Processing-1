import nltk
import random
import string
import pandas as pd
import pdb

from nltk.corpus import senseval
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import brown

from IPython.display import display
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

STOP = set(stopwords.words('english'))
    
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

content_tags = ['JJ', 'JJR', 'JJS', 'NN', 'NNS', 'RB', 'RBR', 'RBS', 'VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']

lemmatizer = WordNetLemmatizer()
instances  = senseval.instances('interest.pos')
dataset    = pd.DataFrame(columns = ['text', 'label'])
for idx, instance in enumerate(instances):
	words = [(word, tag) for word, tag in instance.context if tag in content_tags]
	words = [(word, tag) for word, tag in words if word not in ".,!?~#$%^&*()_+:''-``--]["]
	words = [(word, tag) for word, tag in words if word not in STOP]
	words = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in words]
	words = [word for word in words if word not in STOP]
	words = [word for word in words if len(word) > 2]

	text  = ' '.join(words) 
	label = instance.senses[0].split('_')[-1]

	sample  = [text, label]
	dataset.loc[len(dataset) + 1] = sample

pdb.set_trace()
dataset = dataset.sample(frac = 1, random_state = 42).reset_index(drop = True)
display(dataset.head())

train = dataset[: int(0.9 * len(dataset))]
test  = dataset[int(0.9 * len(dataset)) :]

X_train, y_train, X_test, y_test = train['text'], train['label'], test['text'], test['label']

vectorizer = CountVectorizer(analyzer = 'word', ngram_range = (1, 3))
vectorizer.fit(X_train)

X_train = vectorizer.transform(X_train)
X_test  = vectorizer.transform(X_test)

X_train = X_train.toarray()
X_test  = X_test.toarray()

model = GaussianNB()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("Accuracy: {}".format(accuracy_score(y_pred, y_test)))

file = open('a_file.txt', 'w')
for i in range(test.shape[0]):
	sample = test.values[i]
	file.write("Sample: '{}', with label {} and prediction {}" \
		.format(sample[0], sample[1], model.predict(X_test[i].reshape(1, -1))[0]))
	file.write('\n')