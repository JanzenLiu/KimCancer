import nltk

def find_map(sent):
	dic = dict()
	if type(sent) == str:
		sent = nltk.word_tokenize(sent)
	for index, word in enumerate(sent):
		if (index+3 < len(sent)) and (sent[index+1] == "(" and sent[index+3] == ")"):
			if dic.get(word, None) == None:
				dic[word] = list()
			dic[word].append(sent[index+2])
	return dic

# def find_map_doc(doc):
# 	if
