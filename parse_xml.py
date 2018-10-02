# parse_xml.py

import xml.etree.ElementTree as et
import spacy

tree = et.ElementTree(file="20000410_nyt-NEW.xml")
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
	if texttostring[x] == "<" or texttostring[x] == "&":
		openbracket = True
	if texttostring[x] == ">":
		openbracket = False
	elif not openbracket:
		finaltext += texttostring[x]
	x += 1

nlp = spacy.load('en')
doc = nlp(finaltext)
print(list(doc.sents))


attribs = []
for child in anno:
	attribs.append((int(child.attrib['StartNode']), int(child.attrib['EndNode']), child.attrib['Type']))
# print(attribs)

for t in attribs:
	if t[0] > 11:
		print(finaltext[t[0]-39:t[1]-39], t[2])
	else:
		print(finaltext[t[0]:t[1]], t[2])


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