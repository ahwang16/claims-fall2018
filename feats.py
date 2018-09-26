# feats.py

from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import crfsuite
import spacy

# Functions to extract features
# For the ith word in a sentence, return list of features
def word2feats(sent, i) :
	token = sent[i]
	daughters = set(c.text.lower() for c in token.children)
	ancestors = set(h.lemma_.lower() for h in token.ancestors)
	lemmas = set("tell", "accuse", "insist", "seem", "believe", "say", "find", "conclude", "claim", "trust", "think", "suspect", "doubt", "suppose")
	auxdaughter = "nil"
	moddaughter = "nil"
	for c in token.children:
		if c.pos_ == "AUX":
			auxdaughter = c.text
		if c.tag_ == "MD":
			moddaughter = c.text


	feats = [
		"isNumeric=%s" % token.is_alpha,
		"POS=" + token.pos_,
		"verbType=" + token.tag_ if token.pos_ == "VERB" else "nil",
		"whichModalAmI=", token if token.tag_ == "MD" else "nil",
		"amVBwithDaughterTo=%s" % token.pos_ == "VERB" and "to" in daughters,
		"haveDaughterPerfect=%s" % "has" in daughters or "have" in daughters or "had" in daughters, #check if labeled as modal
		"haveDaughterShould=%s" % "should" in daughters,
		"haveDaughterWh=%s" % "where" in daughters or "when" in daughters or "while" in daughters or "who" in daughters or "why" in daughters,
		"haveReportingAncestor=%s" % token.pos_=="VERB" and len(lemmas.intersectin(ancestors))!=0,
		"parentPOS=" + token.head.pos_,
		"whichAuxIsMyDaughter=" + auxdaughter,
		"whichModalIsMyDaughter=" + moddaughter
	]

	return feats

# Return list of lists of features for each word in a sentence
# sent is a sentence parsed by spacy
def sent2feats(sent) :
	return [word2feats(sent, i) for i in range(len(sent))]

# Import dataset
# Dataset will be a csv with one sentence per line
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
# y_train = # labels from other document?
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



