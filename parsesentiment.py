#parsesentiment.py

'''
Directory structure (of relevant files):
	database.mpqa.1.2/
		man_anns/
			outer_directory/
				unique_code/
					gateman.mpqa.lre.1.2 (for 2005 terminology, in accordance to paper specifications)
		docs/
			outer_directory/
				unique_code (text file with matching file name as annotation file)
'''

import re

'''
type doc_name: (file name of) text
type ann_name: (file name of) annotation file, annotations separated by tabs
	id
	span [start byte, stop byte)
	data_type (always string)
	ann_type (GATE_expressive-subjectivity or GATE_direct-subjective)
	attributes (separated by space) --> possible relevant attrs: polarity="positive", polarity="neutral", polarity="negative"
rtype sents: list of subjective phrases (string)
rtype labels: list of positive, neutral, negative, none polarity labels for each phrase
'''
def parse(doc_name, ann_name, sent_name):
	sents = []
	phrases = []
	labels = []

	# open files
	doc = open(doc_name, "rb")
	ann = open(ann_name, "r")
	sen = open(sent_name, "f")
	out = open("sentimentphrases.txt", "w")

	# skip initial comment lines
	while True:
		line = ann.readline()
		if not line.startswith("#"):
			break

	# line.split('\t') = [id, span, data_type, ann_type, attributes]
	# for each line
		# if ann_type == GATE_expressive_subjectivity or GATE_direct-subjective
			# if regex polarity in attributes
				# labels.append(substring between " ")
				# sents.append(docs bytes span)

	polarity = re.compile(r'polarity=\"\w*\"')
	label = re.compile(r"\"(\w*)\"")
	while line:
		l = line.split('\t')

		if l[3] == "GATE_expressive_subjectivity" or l[3] == "GATE_direct-subjective":
			result = polarity.findall(l[4])
			if len(result) > 0:
				# positive/negative/neutral label
				pol = label.findall(result[0])[0]
				labels.append(pol)

				# actual phrase from doc
				span = l[1].split(",")
				start, stop = int(span[0]), int(span[1])
				doc.seek(start)
				phrase = ""

				while(start < stop):
					phrase += doc.read(1).decode('utf-8')
					start += 1

				phrases.append(phrase)

				out.write("{} {}\n".format(pol.upper(), phrase))
		
		line = ann.readline()


	while True:
		line = sen.readline()
		if not line.startswith("#"):
			break

	while line:
		l = line.split('\t')

		span = l[1].split(",")
		start, stop = int(span[0]), int(span[1])
		doc.seek(start)
		sent = ""

		while start < stop:
			sent += doc.read(1).decode('utf-8')
			start += 1

		sents.append(sent)

		out.write("{}\n").format(sent)

		line = sen.readline()

	return sents, phrases, labels


if __name__ == "__main__":
	ann = "/proj/nlp/users/alyssa/claims-fall2018/database.mpqa.1.2/man_anns/20010620/13.40.05-15087/gateman.mpqa.lre.1.2"
	doc = "/proj/nlp/users/alyssa/claims-fall2018/database.mpqa.1.2/docs/20010620/13.40.05-15087"
	sen = "/proj/nlp/users/alyssa/claims-fall2018/database.mpqa.1.2/man_anns/20010620/13.40.05-15087/gatesentences.mpqa.1.2"

	parse(doc, ann)
