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
	word = sent.split()[i]
	feats = [
		"word.upper=" + word.upper(),
		"word.islower=%s" % word.islower()
	]

	return feats

# Return list of lists of features for each word in a sentence
def sent2feats(sent) :
	return [word2feats(sent, i) for i in range(len(sent.split()))]

# Import dataset
sampledata = ["i am hungry", "computer science is cool"]

for l in sampledata :
	print(sent2feats(l))

# CRFsuite tutorial from github
# https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb