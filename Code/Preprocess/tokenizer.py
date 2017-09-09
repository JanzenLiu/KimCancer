import nltk
import json
import sys; sys.path.append('../')
from reader import load_processed_data

def tokenize(df):
	docs = dict()
	for index, row in df.iterrows():
		print('processing %d' % index)
		sents = list()
		for sent in nltk.sent_tokenize(row['Text']):
			sents.append(nltk.word_tokenize(sent))
		docs[str(index)] = sents
	return docs

if __name__ == '__main__':
	df_train, df_test = load_processed_data()
	docs_train = tokenize(df_train)
	docs_test = tokenize(df_test)
	with open('../../Data/train.tokens.json', 'w') as f:
		json.dump(docs_train, f, indent=2)
	with open('../../Data/test.tokens.json', 'w') as f:
		json.dump(docs_test, f, indent=2)
