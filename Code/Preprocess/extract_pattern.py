#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import json
import os
import sys; sys.path.append("../"); sys.path.append("../Utils/")
import pickle
from collections import Counter
from param_config import config
from reader import load_original_text
from pattern_dict import patterns, other_patterns


'''
1. Extract text segment matching a specified pattern
2. Save the text extracted to a json file (for train and test data each)
@param
	pattern: regular expression for the pattern
	name: name of the pattern, used to save the extracted text
	df_train, df_test: train and test data with column "Text"
	path: directory to save the extracted text
'''
def extract_pattern(pattern, name, df_train, df_test, path):
	print("Extracting pattern %s..." % name)
	res_train = {row['ID']:re.findall(pattern, row['Text'], re.UNICODE) for index, row in df_train.iterrows()}
	filename  = "%s/train.%s.pattern.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_train, f, indent=2)
	res_test = {row['ID']:re.findall(pattern, row['Text'], re.UNICODE) for index, row in df_test.iterrows()}
	filename  = "%s/test.%s.pattern.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_test, f, indent=2)


'''
Remove text segment matching a specified pattern
@param
	pattern: regular expression for the pattern
	dfs: a list of dataframes with column "Text"
	name: name of the pattern
'''
def remove_pattern(pattern, dfs, name=""):
	if name:
		print("Removing pattern %s..." % name)
	for df in dfs:
		for index, row in df.iterrows():
			df.set_value(index, 'Text', re.sub(pattern, "", row['Text'], re.UNICODE))


'''dicarded function'''
def extract_speical_chars_freq(df_train, df_test):
	print("Extracting frequencies of special characters...")
	counter_train = Counter()
	for index, row in df_train.iterrows():
		counter_train += Counter(re.findall(r'[\u00ff-\uffff]', row['Text'], re.UNICODE))
	counter_test = Counter()
	for index, row in df_test.iterrows():
		counter_test += Counter(re.findall(r'[\u00ff-\uffff]', row['Text'], re.UNICODE))
	counter_all = counter_train + counter_test

	df = pd.DataFrame(columns=["character", "hex", "count"])
	for index,(char, count) in enumerate(counter_all.most_common()):
		df.loc[index, "character"] = char
		df.loc[index, "hex"] = "0x%04x" % ord(char)
		df.loc[index, "count"] = count

	path = "%s/all.special_chars.freq.csv" % (config.vocabulary_folder)
	df.to_csv(path, index=False)


'''
1. Perform extraction and removal of all patterns specified in pattern_dict.py
2. Save the processed text to path specified inside the function
@param:
	df_train, df_test: dataframes to perform operations on
	pats: patterns to extract and remove from the text
	other_pats: patterns to extract after pats were removed from the text
'''
def extract_and_remove_all(df_train, df_test, pats, other_pats=other_patterns):
	output_path = config.pattern_folder
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	## extract patterns
	for key, value in pats.items():
		extract_pattern(value, key, df_train, df_test, output_path)

	## remove patterns
	for key, value in pats.items():
		remove_pattern(value, [df_train, df_test], key)

	## extract others patterns
	for key, value in other_pats.items():
		extract_pattern(value, key, df_train, df_test, output_path)

	output_train_txt_file = "%s/training_text.no_pattern.p" % config.data_folder
	output_test_txt_file = "%s/test_text.no_pattern.p" % config.data_folder
	print("Saving text with speicial patterns removed...")
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train['Text'].values, f)
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test['Text'].values, f)

if __name__ == "__main__":
	df_train_txt, df_test_txt = load_original_text()
	extract_speical_chars_freq(df_train_txt, df_test_txt)
	# extract_and_remove_all(df_train_txt, df_test_txt, patterns, other_patterns)
