# sentiment.py

import math
from nltk.corpus import wordnet as wn
import nltk
from collections import Counter


def dal():
	daldict = {}
	with open("dict_of_affect.txt", "r") as dal:
		for line in dal :
				linesplit = line.split()
				daldict[linesplit[0]] = [float(linesplit[1]), float(linesplit[2]), float(linesplit[3])]
	return daldict


# finite state machine to RETAIN or INVERT (negation)
# Invert state: sign of pleasantness score is inverted
# Retain state: sign of pleasantness score stays the same
# sent: sentence (string)
# scores: vector of DAL pleasantness scores
# return updated pleasant scores
def fsm_negate(sent, scores):

	# search for list of negation words --> look at 2005 paper on contextual polarity
	# expand example of negation words https://www.grammarly.com/blog/negatives/
	# on the word wont: one's customary behavior in a particular situation.
	# "Constance, as was her wont, had paid her little attention" --> infrequent
	negate = ["not", "no", "never", "cannot", "didn't", "can't", "cant", "didnt", "couldnt",
				"shouldnt", "couldn't", "shouldn't", "nobody", "nothing", "nowhere", "neither",
				"nor", "none", "doesn't", "doesnt", "isn't", "isnt", "wasn't", "wasnt",
				"wouldn't", "wouldnt", "won't", "wont"]

	# comparative degree adjectives http://www.sparklebox.co.uk/literacy/vocabulary/word-lists/comparatives-superlatives/#.W8E_2xNKjyw
	comp_adj = ["worse", "better", "angrier", "bigger", "blacker", "blander", "bluer", "bolder", "bossier",
				"braver", "briefer", "brighter", "broader", "busier", "calmer", "cheaper", "chewier", "chubbier",
				"classier", "cleaner", "cleverer", "closer", "cloudier", "clumsier", "coarser", "colder",
				"cooler", "crazier", "creamier", "creepier", "crispier", "crunchier", "curly", "curvier",
				"cuter", "damper", "darker", "deadlier", "deeper", "denser", "dirtier", "drier", "duller",
				"dumber", "dustier", "earlier", "easier", "fainter", "fairer", "fancier", "farther",
				"faster", "fatter", "fewer", "fiercer", "filthier", "finer", "firmer", "fitter", "flakier", "flatter",
				"fresher", "friendlier", "fuller", "funnier", "gentler", "gloomier", "greasier", "greater", "greedier",
				"grosser", "hairier", "handier", "happier", "harder", "harsher", "healthier", "heavier", "higher",
				"hipper", "hotter", "humbler", "hungrier", "icier", "itchier", "juicier", "kinder", "larger", "later",
				"lazier", "lighter", "likelier", "littler", "livelier", "longer", "louder", "lovelier", "lower", "madder",
				"meaner", "messier", "milder", "moister", "narrower", "nastier", "naughtier", "nearer", "neater", "needier",
				"newer", "nicer", "noisier", "odder", "oilier", "older", "elder", "plainer", "politer",
				"poorer", "prettier", "prouder", "purer", "quicker", "quieter", "rarer", "rawer", "richer",
				"riper", "riskier", "roomier", "rougher", "ruder", "rustier", "sadder", "safer", "saltier", "saner",
				"scarier", "shallower", "sharper", "shinier", "shorter", "shyer", "sillier", "simpler", "sincerer",
				"skinnier", "sleepier", "slimmer", "slimier", "slower", "smaller", "smarter", "smellier", "smokier",
				"smoother", "softer", "sooner", "sorer", "sorrier", "sourer", "spicier", "steeper", "stingier",
				"stranger", "stricter", "stronger", "sunnier", "sweatier", "sweeter", "taller", "tanner", "tastier",
				"thicker", "thinner", "thirstier", "tinier", "tougher", "truer", "uglier", "warmer", "weaker",
				"wealthier", "weirder", "wetter", "wider", "wilder", "windier", "wiser", "worldlier", "worthier", "younger"]

	# state is True for RETAIN and False for INVERT
	# start with RETAIN
	state = False

	index = 0 # to reference corresponding pleasantness score in scores
	for word in sent:
		# INVERT: negate score
		# switch to RETAIN if current word is but or a comparative degree adjective
		if state:
			scores[index] *= -1
			state = not (word=="but" or word in comp_adj)
		
		# RETAIN: leave score
		# switch to INVERT if current word is a negation
		else:
			state = word in comp_adj

		index += 1

	return scores


# assigning DAL values
# assume input is a string (1 sentence)
# return pleasant, activation, imagery vectors
TODO
def assign_dal(sent, dal):
	tokens = sent.split()
	pleasant = []
	activation = []
	imagery = []

	for t in tokens:
		try:
			pleasant.append(dal[t][0])
		except:
			pleasant.append(pleasant(sent, dal))
		try:
			activation.append(dal[t][1])
		except:
			activation.append(activation(sent, dal))
		try:
			imager.append(dal[t][2])
		except:
			imagery.append(imagery(sent, dal))
		

	return pleasant, activation, imagery


def pleasant(sent, dal):
	syns = wn.synsets(t)
	setlen = len(syns)
	synlen = len(syns[0])
	x, y = 0

	while x < setlen:
		while y < synlen:
			try:
				return dal[syns[x].lemmas()[y].name()][0]
			except:
				y += 1
		y = 0
		x += 1
		synlen = len(syns[x])

	for syn in syns:
		for l in syn.lemmas():
			ants = l.antonyms()
			if ants:
				for a in ants:
					try:
						return -1 * dal[a.name()][0]
	return 0.0


def activation(sent, dal):
	syns = wn.synsets(t)
	setlen = len(syns)
	synlen = len(syns[0])
	x, y = 0

	while x < setlen:
		while y < synlen:
			try:
				return dal[syns[x].lemmas()[y].name()][1]
			except:
				y += 1
		y = 0
		x += 1
		synlen = len(syns[x])

	for syn in syns:
		for l in syn.lemmas():
			ants = l.antonyms()
			if ants:
				for a in ants:
					try:
						return -1 * dal[a.name()][1]
	return 0.0


def imagery(sent, dal):
	syns = wn.synsets(t)
	setlen = len(syns)
	synlen = len(syns[0])
	x, y = 0

	while x < setlen:
		while y < synlen:
			try:
				return dal[syns[x].lemmas()[y].name()][2]
			except:
				y += 1
		y = 0
		x += 1
		synlen = len(syns[x])

	for syn in syns:
		for l in syn.lemmas():
			ants = l.antonyms()
			if ants:
				for a in ants:
					try:
						return -1 * dal[a.name()][2]
	return 0.0


# Z-normalize scores using mean and stdev found in manual (Whissel, 1989)
# boost score by multiplying by normalized score distance from mean
# https://www.god-helmet.com/wp/whissel-dictionary-of-affect/index.htm
# plea(santry): mean 1.85, stdev 0.36
# acti(vation): mean 1.67, stdev 0.36
# imag(ery):	mean 1.52, stdev 0.63
def normalize_dal(plea, acti, imag):
	meanp, stdevp = 1.85, 0.36
	meana, stdeva = 1.67, 0.36
	meani, stdevi = 1.52, 0.63
	for x in range(len(plea)):
		plea[x] = (plea[x] - meanp) / stdevp
		plea[x] *= abs(plea[x] - meanp)
		acti[x] = (acti[x] - meana) / stdeva
		acti[x] *= abs(acti[x] - meana)
		imag[x] = (imag[x] - meani) / stdevi
		imag[x] *= (imag[x] = meani)

	return plea, acti, imag


# input three vectors: pleasant, activation, imagery
# return averages of pleasantness, activation, imagery
# this method should be used for subjective phrases (not whole sent)
def compute_phrases(plea, acti, imag):
	p = sum(plea) / len(plea)
	a = sum(acti) / len(acti)
	i = sum(imag) / len(imag)

	return p, a, i


# input three floats: pleasant, activation, imagery average for phrase
# return norm (combination of the three scores)
# need to call this method after calling compute_phrases()
def add_norm(p, a, i):
	return math.pow(math.pow(i, 2) + math.pow(a, 2), 0.5) / i


# count number of occurrences of each POS in subjective phrase
# represent POS as integer in feature vector
# bigrams as binary feature vector
# original uses Stanford Tagger --> use NLTK interface to Stanford Tagger
# type phrase: str, one subjective phrase
# rtype counts: Counter, tag : freq
# rtype bg: generator of bigrams in phrase
def extract_lexical(phrase):
	tokens = nltk.word_tokenize(phrase)
	text = nltk.Text(tokens)
	tags = nltk.pos_tag(text)
	counts = Counter(tag for word, tag in tags)

	bg = nltk.bigrams(phrase.split())
	return counts, bg


def chunk(sent):
	












