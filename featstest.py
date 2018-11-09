# featstest.py
# CRFsuite tutorial from github
# https://github.com/scrapinghub/python-crfsuite/blob/master/examples/CoNLL%202002.ipynb


# Make predictions
tagger = crfsuite.Tagger()
tagger.open('claims.crfsuite')