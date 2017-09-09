import nltk
import sys; sys.path.append('../')
from reader import load_processed_data

def tokenize(df):
	docs = dict()
	for index, row in df.iterrows():
		sents = list()
		for sent in nltk.sent_tokenize(row['Text']):
			sents.append(nltk.word_tokenize(sent))
		docs[str(index)] = sents
		break
	return docs

if __name__ == '__main__':
	df_train, df_test = load_processed_data()
	docs_train = tokenize(df_train)
	docs_test = tokenize(df_test)
	with open('../../Data/tokens_train.json', 'w') as f:
		json.dump(f, docs_train, indent=2)