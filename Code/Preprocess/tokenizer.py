import nltk
import json
import pickle
import numpy as np
import pandas as pd
import sys; sys.path.append('../')
from reader import load_processed_data, load_original_text
from tools import seriesToJson

def tokenize(doc):
	tokenized_doc = list()
	for sent in nltk.sent_tokenize(doc):
		tokenized_doc.append(nltk.word_tokenize(sent))
	return tokenized_doc

def tokenize_df(df):
	df['tokenized_text'] = df['Text'].map(tokenize)

def dump_tokenized_json(df, path):
	if not 'tokenized_text' in df.columns:
		tokenize_df(df)
	tokens_json = seriesToJson(df['tokenized_text'], str)
	with open(path, 'w') as f:
		json.dump(tokens_json, f, indent=2)

def dump_tokenized_csv(df, path):
	if not 'tokenized_text' in df.columns:
		tokenize_df(df)
	df[['ID', 'tokenized_text']].to_csv(path, index=False)

def dump_tokenized_pickle(df, path):
	if not 'tokenized_text' in df.columns:
		tokenize_df(df)
	with open(path, 'wb') as f:
		pickle.dump(df['tokenized_pattern'].values, f)

if __name__ == '__main__':
	df_train_txt, df_test_txt = load_original_text()
	dump_tokenized_json(df_train_txt, '../../Data/train.tokens.json')
	dump_tokenized_json(df_test_txt, '../../Data/test.tokens.json')
	