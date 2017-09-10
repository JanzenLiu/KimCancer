import nltk

class WordMap():
	def __init__(self):
		self.dic = dict()

	def map_sent(self, sent):
		if type(sent) == str:
			sent = nltk.word_tokenize(sent)
		for index, word in enumerate(sent):
			if (index+3 < len(sent)) and (sent[index+1] == "(" and sent[index+3] == ")") and (not sent[index+2].isdigit()):
				if not word in self.dict:
					self.dic[word] = set()
				self.dic[word].add(sent[index+2])

	def map_doc(self, doc):
		for sent in doc:
			self.map_sent(sent)

	def map_docs(self, docs):
		for doc in docs:
			self.map_doc(doc)

	def map_df(self, df, col_name='Text'):
		self.map_docs(df[col_name].values)

	def clear_map(self):
		self.map = dict()


