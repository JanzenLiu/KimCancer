import nltk
import json
import pickle
import numpy as np
import pandas as pd
import sys; sys.path.append('../'); sys.path.append('../Utils/')
from param_config import config
from reader import load_processed_data, load_original_text
from converter import series_to_json

def tokenize(doc):
	tokenized_doc = list()
	for sent in nltk.sent_tokenize(doc):
		tokenized_doc.append(nltk.word_tokenize(sent))
	return tokenized_doc

def tokenize_df(df, text_col="Text"):
	df['tokenized_text'] = df[text_col].map(tokenize)

def dump_tokenized_json(df, path):
	if not 'tokenized_text' in df.columns:
		tokenize_df(df)
	tokens_json = series_to_json(df['tokenized_text'], str)
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
	dump_tokenized_json(df_train_txt, config.train_tokens_path)
	dump_tokenized_json(df_test_txt, config.test_tokens_path)
	

