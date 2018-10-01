# sentiment.py

import math

def dal():
	daldict = {}
	with open("dict_of_affect.txt", "r") as dal:
		for line in dal :
				linesplit = line.split()
				daldict[linesplit[0]] = [float(linesplit[1]), float(linesplit[2]), float(linesplit[3])]
	return daldict


# finite state machine to RETAIN or INVERT (negation)


# assigning DAL values
# assume input is a string (1 sentence)
# return [(e, a, i) (e, a, i) ...]
def assign_dal(sent, dal):
	vec = []
	tokens = sent.split()

	for t in tokens:
		d = [0.0, 0.0, 0.0]
		try:
			d[0] = dal[t][0]
		try:
			d[1] = dal[t][1]
		try:
			d[2] = dal[t][2]
		vec.append(d)

	return vec


# input [[p, a, i], [p, a, i]...]
# return [average_p, average_a, average_i]
def compute_phrases(vec):
	phrase = []
	p = 0
	a = 0
	i = 0
	count = 0

	for v in vec:
		p += v[0]
		a += v[1]
		i += v[2]
		count += 1

	r.append(p / count)
	r.append(a / count)
	r.append(i / count)

	return phrase


def add_norm(phrase):
	e2 = phrase[0] * phrase[0]
	a2 = phrase[1] * phrase[1]

	n = math.pow(e2+a2, 0.5) / phrase[2]

	pn = phrase.append(n)

	return pn








