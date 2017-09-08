#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import json
import os
import sys; sys.path.append("../")
import pickle
from collections import Counter
from param_config import config
from reader import load_replaced_text
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

'''
1. Counting occurence(s) of a pattern(s) in text data
2. Save the frequencies of different content calculated to path specified inside the function
3. This function is initially designed to count frequencies for special unicode characters
@param:
	df_train, df_test: dataframes with a "Text" column to count occurence(s) of the pattern on.
	pattern: pattern (which is supposed to match with different content) to match content for counting
	name: name of the pattern, used to save the result
'''
def extract_unicode_freq(df_train, df_test, pattern, name):
	print("Extracting frequencies of unicode pattern...")
	counter_train = Counter()
	for index, row in df_train.iterrows():
		counter_train += Counter(re.findall(pattern, row['Text'], re.UNICODE))
	counter_test = Counter()
	for index, row in df_test.iterrows():
		counter_test += Counter(re.findall(pattern, row['Text'], re.UNICODE))
	counter_all = counter_train + counter_test
	output_freq_file = "%s/%s.freq" % (config.data_folder, name)
	with open(output_freq_file, "w"):
		f.write("unicode,occurence" + os.linesep)
		for key, value in counter_all.most_common():
			f.write("%s,%d"%(key,value) + os.linesep)

'''
1. Perform extraction and removal of all patterns specified in pattern_dict.py
2. Save the processed text to path specified inside the function
@param:
	df_train, df_test: dataframes to perform operations on
	pats: patterns to extract and remove from the text
	other_pats: patterns to extract after pats were removed from the text
'''
def extract_and_remove_all(df_train, df_test, pats, other_pats=other_patterns):
	## load cached patterns
	with open(config.pattern_cache_file, "rb") as f:
		old_patterns = pickle.load(f)
	update_other = False # flag to determine whether to extract others patterns again

	output_path = "%s/Raw" % config.pattern_folder
	if not os.path.exists(output_path):
		os.makedirs(output_path)

	## extract patterns
	for key, value in pats.items():
		# skip current pattern if it hasn't changed from the cache
		# little bug：the pattern will also be skipped even though the upstream preprocessor was changed
		pattern_unchanged = (old_patterns.get(key) == value)
		if pattern_unchanged:
			print("Skip extracting pattern %s, since it hasn't changed" % key)
			continue
		update_other = True
		extract_pattern(value, key, df_train, df_test, output_path)
		print("Updating pattern %s in cache..." % key)
		old_patterns[key] = value
		with open(config.pattern_cache_file, "wb") as f:
			pickle.dump(old_patterns, f)

	## remove patterns
	for key, value in pats.items():
		remove_pattern(value, [df_train, df_test], key)

	## extract others patterns
	for key, value in other_pats.items():
		pattern_unchanged = (old_patterns.get(key) == value)
		if (not update_other) and pattern_unchanged:
			print("Skip extracting pattern %s, since it hasn't changed" % key)
			continue
		extract_pattern(value, key, df_train, df_test, output_path)
		if not pattern_unchanged:
			print("Updating pattern %s in cache..." % key)
			old_patterns[key] = value
			with open(config.pattern_cache_file, "wb") as f:
				pickle.dump(old_patterns, f)

	output_train_txt_file = "%s/training_text.removed_pattern.p" % config.data_folder
	output_test_txt_file = "%s/test_text.removed_pattern.p" % config.data_folder
	print("Saving text with speicial patterns replaced...")
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train, f)
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test, f)

if __name__ == "__main__":
	df_train_txt, df_test_txt = load_replaced_text()
	extract_and_remove_all(df_train_txt, df_test_txt, patterns, other_patterns)
