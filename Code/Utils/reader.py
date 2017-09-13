import numpy as np
import pandas as pd
import pickle
import json
import sys; sys.path.append('../')
import os
from param_config import config

'''return original train and test text data'''
def load_original_text():
	print("Loading original text...")
	df_train_txt = pd.read_csv(config.original_train_text_path, 
		sep="\|\|", header=None, skiprows=1, names=["ID", "Text"], engine="python").fillna("")
	df_test_txt = pd.read_csv(config.original_test_text_path, 
		sep="\|\|", header=None, skiprows=1, names=["ID", "Text"], engine="python").fillna("")
	return df_train_txt, df_test_txt

'''return original variants data'''
def load_original_variants():
	print("Loading original variants data...")
	df_train_var = pd.read_csv(config.original_train_variant_path)
	df_test_var = pd.read_csv(config.original_test_variant_path)
	return df_train_var, df_test_var

''' return original data'''
def load_original_data():
	print("Loading original data...")
	df_train_txt, df_test_txt = load_original_text()
	df_train_var, df_test_var = load_original_variants()
	df_train = pd.merge(df_train_txt, df_train_var, how="left", on="ID").fillna("")
	df_test = pd.merge(df_test_txt, df_test_var, how="left", on="ID").fillna("")
	return df_train, df_test

'''return processed variants data'''
def load_processed_variants():
	print("Loading processed variants data...")
	df_train_var = pd.read_csv(config.processed_train_variant_path)
	df_test_var = pd.read_csv(config.processed_test_variant_path)
	return df_train_var, df_test_var

'''return last saved processed data, with text and variants merged'''
def load_processed_data():
	print("Loading processed data...")
	with open(config.processed_train_data_path, "rb") as f:
		df_train = pickle.load(f)
	with open(config.processed_test_data_path, "rb") as f:
		df_test = pickle.load(f)
	return df_train, df_test

'''return processed variants data'''
def load_current_data():
	print("Loading current data (with text unchanged and variants processed)...")
	df_train_txt, df_test_txt = load_original_text()
	df_train_var, df_test_var = load_processed_variants()
	df_train = pd.merge(df_train_txt, df_train_var, how="left", on="ID").fillna("")
	df_test = pd.merge(df_test_txt, df_test_var, how="left", on="ID").fillna("")
	return df_train, df_test

'''return tokens extracted from text data'''
def load_tokens(version="original"):
	if version not in ["original", "no_pattern"]:
		print("[Error] version %s not found" % version)
	train_tokens_path = "%s/train.%s.tokens.json" % (config.data_folder, version)
	test_tokens_path = "%s/test.%s.tokens.json" % (config.data_folder, version)

	print("Loading tokens...")
	with open(train_tokens_path, "r") as f:
		train_tokens = json.load(f)
	with open(test_tokens_path, "r") as f:
		test_tokens = json.load(f)
	return train_tokens, test_tokens

'''return vocabulary of common words'''
def load_vocabulary():
    vocab = set()

    print("Loading vocabulary...")
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


'''return special characters'''
def load_special_chars():
    chars = set()

    print("Loading special characters...")
    with open(config.special_characters_path) as f:
        char = f.readline().strip()
        while char != '':
            chars.add(char)
            char = vocab_file.readline().strip()
    return chars

def load_special_chars_csv():
	df = pd.read_csv("../../all.special_chars.freq.csv")
	return df

'''
@param: stratified_label: label used to generated the stratified kfold
@return: StratifiedKFold indices for each run and fold
'''
def load_stratified_kfold(stratified_label=config.stratified_label):
	path = "%s/stratifiedKFold.%s.p" % (config.data_folder, stratified_label)
	if not os.path.exists(path):
		print("[Error] Dumped stratifiedKFold not found")
		return "error"

	print("Loading stratified kfold...")
	with open(path, "rb") as f:
		skf = pickle.load(f)
	return skf
