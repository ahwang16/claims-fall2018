# feats.py

from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import crfsuite
# import spacy

# Functions to extract features
# For the ith word in a sentence, return list of features
def word2feats(sent, i) :
	token = sent[i]
	daughters = [c.text for c in token.children]
	feats = [
		"isNumeric=%s" % token.is_alpha,
		"POS=" + token.pos_,
		"verbType=" + token.tag_ if token.pos_ == "VERB" else "nil",
		"whichModalAmI=",
		"amVBwithDaughterTo=%s" % token.pos_ == "VERB" and "to" in daughters,
		"haveDaughterPerfect=%s" % "has" in daughters or "have" in daughters or "had" in daughters,
		"haveDaughterShould=%s" % "should" in daughters,
		"haveDaughterWh=%s" % "where" in daughters or "when" in daughters or "while" in daughters or "who" in daughters or "why" in daughters,
		"haveReportingAncestor=",
		"parentPOS=" + token.head.pos_,
		"whichAuxIsMyDaughter=",
		"whichModalIsMyDaughter="
	]

	return feats

# Return list of lists of features for each word in a sentence
# sent is a sentence parsed by spacy
def sent2feats(sent) :
	return [word2feats(sent, i) for i in range(len(sent))]

# Import dataset
sampledata = "i am hungry. computer science is cool."

nlp = spacy.load('en')
doc = nlp(sampledata)

# features for entire dataset
# each element is a list of features for each sentence
# each list of sentence features is a list of features for each word
# [[[sent1word1], [sent1word2]], [[sent2word1]]]
feats = []
for sent in list(doc.sents) :
	feats.append(sent2feats(sent))

# CRFsuite tutorial from github
# https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb

# Extract features from data
X_train = [sent2feats(s) for s in train_sents]
y_train = # labels from other document?
# also need X_test and y_test

# Train model
trainer = crfsuite.Trainer(verbose=True)

for xseq, yseq in zip(X_train, y_train) :
	trainer.append(xseq, yseq)

trainer.set_params({
	'c1': 1.0,
	'c2': 1e-3,
	'max_iterations': 50,
	'feature.possible_transitions': True
})

trainer.train('claims.crfsuite')

# Make predictions
tagger = crfsuite.Tagger()
tagger.open('claims.crfsuite')



