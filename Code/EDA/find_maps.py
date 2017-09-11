import nltk
import json
import sys; sys.path.append("../"); sys.path.append("../Utils/")
from reader import load_tokens
from writer import dump_json
from param_config import config

class WordMap:
	def __init__(self):
		self.dic = dict()

	def map_sent(self, sent):
		if type(sent) == str:
			sent = nltk.word_tokenize(sent)
		for index, word in enumerate(sent):
			if (index+3 < len(sent)) and (sent[index+1] == "(" and sent[index+3] == ")") \
				and (not sent[index+2].replace(".","",1).isdigit()):
				if not word in self.dic:
					self.dic[word] = set()
				self.dic[word].add(sent[index+2])

	def map_doc(self, doc):
		for sent in doc:
			self.map_sent(sent)

	def map_docs(self, docs):
		for doc in docs:
			self.map_doc(doc)

	def map_df(self, df, col_name='tokenized_text'):
		self.map_docs(df[col_name].values)

	def map_json(self, json):
		for value in json.values():
			self.map_doc(value)

	def clear_map(self):
		self.dic = dict()

if __name__ == "__main__":
	word_map = WordMap()
	tokens_train, tokens_test = load_tokens()

	print("Constructing word map for original text...")
	word_map.map_json(tokens_train)
	word_map.map_json(tokens_test)

	obj = word_map.dic.copy()
	for key, value in obj.items():
		obj[key] = list(value)

	dump_json(obj, config.wordmap_path, "Saving word map for original text...")
