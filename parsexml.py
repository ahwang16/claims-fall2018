# parse_xml.py

import xml.etree.ElementTree as et
import spacy
import string
import os

nlp = spacy.load('en')

def parse(f):
	tree = et.parse(f)
	root = tree.getroot()
	text = root[0]
	print(type(text))

	# print(text.text)
	anno = root[3]

	# for r in et.tostring(root[1]):
	# 	print(r.tag, r.text)

	# print(et.tostring(root[1]))
	texttostring = et.tostring(text, encoding="utf8", method="xml").decode()
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

	doc = nlp(finaltext)


	spacy_sents = list(doc.sents) # doc.sents is a list of spans
	startnode = 0

	for sent in sents:
		s = []
		for word in sent:
			s.append(word)
			if startnode in start:
				labels.append(startlabel[startnode])
			else:
				labels.append("Not Applicable")
			startnode += len(word.string)
		sents.append(s)
	


	return sents, labels


if __name__ == "__main__":
	for filename in os.listdir("./"):
		if filename.endswith(".xml"):
			print(filename)
			try:
				parse(filename)
				print("done!")
			except Exception as e:
				print(e)

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
