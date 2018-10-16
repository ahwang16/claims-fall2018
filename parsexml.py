# parse_xml.py

import xml.etree.ElementTree as et
import spacy
import string
import os


def parse(f):
	tree = et.ElementTree(file=f)
	root = tree.getroot()
	text = root[1]

	# print(text.text)
	anno = root[3]

	# for r in et.tostring(root[1]):
	# 	print(r.tag, r.text)

	# print(et.tostring(root[1]))
	texttostring = et.tostring(root[1]).decode().strip()
	# print(texttostring)
	openbracket = False
	finaltext = ""
	x = 0

	while x < len(texttostring):
		if texttostring[x] == "<":
			openbracket = True
		elif texttostring[x] == "&" and texttostring[x+1]=="l" and texttostring[x+2]=="t" and texttostring[x+3]==";":
			openbracket = True
			x += 3
		elif texttostring[x] == ">":
			openbracket = False
		elif texttostring[x] == "&" and texttostring[x+1]=="g" and texttostring[x+2]=="t" and texttostring[x+3]==";":
			openbracket = False
			x += 3
		elif not openbracket:
			finaltext += texttostring[x]
		x += 1

	attribs = []
	for child in anno:
		attribs.append((int(child.attrib['StartNode']), int(child.attrib['EndNode']), child.attrib['Type']))

	start = []
	startlabel = {}
	for t in attribs:
		if t[0] > 11 and t[0] < 1161:
			start.append(t[0]-13)
			startlabel[t[0]-13] = t[2] 
		elif t[0] > 1160:
			start.append(t[0]-36)
			startlabel[t[0]-36] = t[2]
		else:
			start.append(t[0])
			startlabel[t[0]] = t[2]

	sents = [] # list of sentences, each sentence is a list of words
	labels = [] # label of corresponding word
	word = ""
	index = 0
	label = ""

	nlp = spacy.load('en')
	doc = nlp(finaltext)

	sents = list(doc.sents)
	startnode = 0

	for sent in sents:
		for word in sent:
			if startnode in start:
				labels.append(startlabel[startnode])
			else:
				labels.append("Not Applicable")
			startnode += len(word.string)


	return sents, labels



for filename in os.listdir("./"):
	if filename.endswith(".xml"):
		print(parse(filename))

	# tokenize with spacy first --> each word is a spacy object
	# keep a count variable to keep track if the start/end nodes match up
	# for l in range(len(finaltext)):

	# 	if finaltext[l]=="\n":
	# 		continue
	# 	elif finaltext[l] != " ":
	# 		word += finaltext[l]
	# 	else:
	# 		if index in start:
	# 			label = startlabel[index]
	# 		else:
	# 			label = "Not Applicable"
	# 		word = word.strip(string.punctuation).strip()
	# 		pairs.append((word, label))
	# 		index = l + 1
	# 		word = ""

	# return pairs

#for p in pairs:
#	print(p)





# write own code to parse through body of text
# id numbers correspond to character indices


# Child nodes for annotations
# Id --> int (start and end characters of text without xml tags)
# Type --> annotation type
# for child in anno:
# 	print(child.attrib['StartNode'], child.attrib['EndNode'], child.attrib['Type'])
# 	print(child.tag, child.text, child.attrib)

# for e in text.iter():
# 	print(e.text)
