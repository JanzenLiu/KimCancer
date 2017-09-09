import numpy as np
import pandas as pd
import pickle
import json
import sys
import os
from param_config import config

'''return original train and test text data'''
def load_original_text():
	df_train_txt = pd.read_csv(config.original_train_text_path, 
		sep="\|\|", header=None, skiprows=1, names=["ID", "Text"], engine="python")
	df_test_txt = pd.read_csv(config.original_test_text_path, 
		sep="\|\|", header=None, skiprows=1, names=["ID", "Text"], engine="python")
	return df_train_txt, df_test_txt

'''return original variants data'''
def load_original_variants():
	df_train_var = pd.read_csv(config.original_train_variant_path)
	df_test_var = pd.read_csv(config.original_test_variant_path)
	return df_train_var, df_test_var

''' return original data'''
def load_original_data():
	df_train_txt, df_test_txt = load_original_text()
	df_train_var, df_test_var = load_original_variants()
	df_train = pd.merge(df_train_txt, df_train_var, how="left", on="ID").fillna("")
	df_test = pd.merge(df_test_txt, df_test_var, how="left", on="ID").fillna("")
	return df_train, df_test


'''return last saved text data with special characters replaced'''
def load_replaced_text():
	replaced_train_text_path = "%s/training_text.replaced_unicode.p" % config.data_folder
	replaced_test_text_path = "%s/test_text.replaced_unicode.p" % config.data_folder
	if not (os.path.exists(replaced_train_text_path) and os.path.exists(replaced_test_text_path)):
		print("[Warning] Replaced text files do not exist")
		return load_original_text()
	print("Loading replaced text for the entire training set...")
	with open(replaced_train_text_path, "rb") as f:
		df_train_txt = pickle.load(f)
	print("Loading replaced text for the entire testing set...")
	with open(replaced_test_text_path, "rb") as f:
		df_test_txt = pickle.load(f)
	return df_train_txt, df_test_txt

'''return last saved text data with special patterns removed'''
def load_extracted_text():
	extracted_train_text_path = "%s/training_text.extracted_pattern.p" % config.data_folder
	extracted_test_text_path = "%s/test_text.extracted_pattern.p" % config.data_folder
	if not (os.path.exists(extracted_train_text_path) and os.path.exists(extracted_test_text_path)):
		print("[Warning] Extracted text files do not exist")
		return load_original_text()
	print("Loading extracted text for the entire training set...")
	with open(extracted_train_text_path, "rb") as f:
		df_train_txt = pickle.load(f)
	print("Loading extracted text for the entire testing set...")
	with open(extracted_test_text_path, "rb") as f:
		df_test_txt = pickle.load(f)
	return df_train_txt, df_test_txt

'''return last saved processed data, with text and variants merged'''
def load_processed_data():
	with open(config.processed_train_data_path, "rb") as f:
		df_train = pickle.load(f)
	with open(config.processed_test_data_path, "rb") as f:
		df_test = pickle.load(f)
	return df_train, df_test

'''return tokens extracted from text data'''
def load_tokens():
	train_tokens_path = "%s/train.tokens.p" % config.data_folder
	test_tokens_path = "%s/test.tokens.p" % config.data_folder
	with open(train_tokens_path, "r") as f:
		train_tokens = json.load(f)
	with open(test_tokens_path, "r") as f:
		test_tokens = json.load(f)
	return train_tokens, test_tokens

'''return vocabulary of common words'''
def load_vocabulary():
    vocab = set()
    with open(config.main_dictionary_path) as vocab_file:
        word = vocab_file.readline().strip()
        while word != '':
            vocab.add(word)
            word = vocab_file.readline().strip()
    with open(config.suppliment_dictionary_path) as vocab_file:
        word = vocab_file.readline().strip()
        while word != '':
            vocab.add(word)
            word = vocab_file.readline().strip()
    return vocab


'''
@param: stratified_label: label used to generated the stratified kfold
@return: StratifiedKFold indices for each run and fold
'''
def load_stratified_kfold(stratified_label=config.stratified_label):
	path = "%s/stratifiedKFold.%s.p" % (config.data_folder, stratified_label)
	if not os.path.exists(path):
		print("[Error] Dumped stratifiedKFold not found")
		return "error"
	with open(path, "rb") as f:
		skf = pickle.load(f)
	return skf
