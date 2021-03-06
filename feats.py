# feats.py
'''
feats
0: lexical and syntactic, no context
1: lexical with context
2: lexical with context, syntactic no conext
3: lexical and syntactic with context
'''

from itertools import chain
import nltk
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelBinarizer
import sklearn
import pycrfsuite
import spacy
import parsexml
from collections import Counter
import os, sys



# Functions to extract features
# For the ith word in a sentence, return list of features
def word2feats(sent, i, feature) :
	token = sent[i]
#	print(sent, i)
#	print("token:", token, ", token type:", type(token), ", sent type:", type(sent))
	daughters = {c.text.lower() for c in token.children}
	ancestors = {h.lemma_.lower() for h in token.ancestors}
	lemmas = {"tell", "accuse", "insist", "seem", "believe", "say", "find", "conclude", "claim", "trust", "think", "suspect", "doubt", "suppose"}
	auxdaughter = "nil"
	moddaughter = "nil"
	for c in token.children:
		if c.pos_ == "AUX":
			auxdaughter = c.text
		if c.tag_ == "MD":
			moddaughter = c.text

	'''
	all features
	feats = [
		"isNumeric=%s" % token.is_alpha,
		"POS=" + token.pos_,
		"verbType=" + token.tag_ if token.pos_ == "VERB" else "nil",
		"whichModalAmI=" + token if token.tag_ == "MD" else "nil",
		"amVBwithDaughterTo=%s" % token.pos_ == "VERB" and "to" in daughters,
		"haveDaughterPerfect=%s" % "has" in daughters or "have" in daughters or "had" in daughters, #check if labeled as modal
		"haveDaughterShould=%s" % "should" in daughters,
		"haveDaughterWh=%s" % "where" in daughters or "when" in daughters or "while" in daughters or "who" in daughters or "why" in daughters,
		"haveReportingAncestor=%s" % token.pos_=="VERB" and len(lemmas.intersection(ancestors))!=0,
		"parentPOS=" + token.head.pos_,
		"whichAuxIsMyDaughter=" + auxdaughter,
		"whichModalIsMyDaughter=" + moddaughter
	]
	'''
	feats = []
	# lexical and syntactic features with no context
	if feature == 0:
		feats = [
			"POS=" + token.pos_,
			"whichModalAmI=" + token.text if token.tag_ == "MD" else "nil",
			"parentPOS=" + token.head.pos_,

		]

	# lexical features with context
	elif feature == 1:
		feats = [
			"POS=" + token.pos_,
			"whichModalAmI=" + token.text if token.tag_ == "MD" else "nil",
			"verbType=" + token.tag_ if token.pos_ == "VERB" else "nil",
			"isNumeric%s" % str(token.is_alpha),
			"haveReportingAncestor=%s" % str(token.pos_=="VERB" and len(lemmas.intersection(ancestors))!=0),
			"whichModalIsMyDaughter=" + moddaughter,
			"whichAuxIsMyDaughter=" + auxdaughter,
			"haveDaughterShould=%s" % str("should" in daughters)
		]

	# lexical features with context and syntactic features with no context
	elif feature == 2:
		feats = [
			"POS=" + token.pos_,
			"whichModalAmI=" + token.text if token.tag_ == "MD" else "nil",
			"parentPOS=" + token.head.pos_,
			"haveReportingAncestor=%s" % str(token.pos_=="VERB" and len(lemmas.intersection(ancestors))!=0),
			"whichModalIsMyDaughter=" + moddaughter,
			"whichAuxIsMyDaughter=" + auxdaughter,
			"haveDaughterShould=%s" % str("should" in daughters)
		]

	# lexical and syntactic features with context
	elif feature == 3:
		feats = [
			"POS=" + token.pos_,
			"whichModalAmI=" + token.text if token.tag_ == "MD" else "nil",
			"parentPOS=" + token.head.pos_,
			"haveReportingAncestor=%s" % str(token.pos_=="VERB" and len(lemmas.intersection(ancestors))!=0),
			"whichModalIsMyDaughter=" + moddaughter,
			"haveDaughterPerfect=%s" % str("has" in daughters or "have" in daughters or "had" in daughters),
			"whichAuxIsMyDaughter=" + auxdaughter,
			"haveDaughterWh=%s" % str("where" in daughters or "when" in daughters or "while" in daughters or "who" in daughters or "why" in daughters),
			"haveDaughterShould=%s" % str("should" in daughters)
		]
	

	return feats
 



# Return list of lists of features for each word in a sentence
# sent is a sentence parsed by spacy
def sent2feats(sent, feature) :
	return [word2feats(sent, i, feature) for i in range(len(sent))]


def classify(y_true, y_pred):
	lb = LabelBinarizer()
	y_true_combined = lb.fit_transform(list(chain.from_iterable(y_true)))
	y_pred_combined = lb.transform(list(chain.from_iterable(y_pred)))

	tagset = set(lb.classes_) - {'O'}
	tagset = sorted(tagset, key=lambda tag: tag.split('-', 1)[::-1])
	class_indices = {cls: idx for idx, cls in enumerate(lb.classes_)}

	return classification_report(
        y_true_combined,
        y_pred_combined,
        labels = [class_indices[cls] for cls in tagset],
        target_names = tagset,
    )


def print_transitions(trans_features):
    for (label_from, label_to), weight in trans_features:
        print("%-6s -> %-7s %0.6f" % (label_from, label_to, weight))


def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-6s %s" % (weight, label, attr))    


if __name__ == "__main__":
	# Import dataset
	# Data is list of pairs of words and tags [(word, tag)]
	sents, labels = parsexml.parse("20000410_nyt-NEW.xml")

	# Test data
	test_sents = []
	test_labels = []
	for filename in os.listdir("./featsdata/"):
		if filename.endswith(".xml"):
			print(filename)
			try:
				s, l = parsexml.parse("./featsdata/" + filename)
				test_sents += s
				test_labels += l
				print("done!")
			except Exception as e:
				print(e)



	# CRFsuite tutorial from github
	# https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb
	feature = int(sys.argv[1])
	# Extract features from data
	X_train = [sent2feats(s, feature) for s in sents]
	y_train = labels
	X_test = [sent2feats(s, feature) for s in test_sents]
	y_test = test_labels

	# Train model
	trainer = pycrfsuite.Trainer(verbose=True)
#	print(X_train, "\n", y_train)
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
	tagger = pycrfsuite.Tagger()
	tagger.open('claims.crfsuite')

	y_pred = [tagger.tag(xseq) for xseq in X_test]
	print(classify(y_test, y_pred))

	# Check what classifier learned
	info = tagger.info()

	print("Top likely transitions:")
	print_transitions(Counter(info.transitions).most_common(15))

	print("\nTop unlikely transitions:")
	print_transitions(Counter(info.transitions).most_common()[-15:])

	print("Top positive:")
	print_state_features(Counter(info.state_features).most_common(20))

	print("\nTop negative:")
	print_state_features(Counter(info.state_features).most_common()[-20:])

