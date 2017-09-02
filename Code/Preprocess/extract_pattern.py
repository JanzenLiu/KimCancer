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
from pattern_dict import patterns, other_patterns, unicode_pattern

df_train_txt, df_test_txt = load_replaced_text()
df_train_txt_copy = df_train_txt.copy()
df_test_txt_copy = df_test_txt.copy()

## extract single pattern
def extract_pattern(name, pattern, path):
	print("Extracting pattern %s from the entire training set..." % name)
	res_train = {row['ID']:re.findall(pattern, row['Text']) for index,row in df_train_txt.iterrows()}
	filename  = "%s/%s.train.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_train, f, indent=2)

	print("Extracting pattern %s from the entire testing set..." % name)
	res_test = {row['ID']:re.findall(pattern, row['Text']) for index,row in df_test_txt.iterrows()}
	filename  = "%s/%s.test.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_test, f, indent=2)

## remove single pattern from text
def remove_pattern(name, pattern):
	print("Removing pattern %s from the entire training set..." % name)
	for index, row in df_train_txt_copy.iterrows():
		df_train_txt_copy.set_value(index, 'Text', re.sub(pattern, "", row['Text']))

	print("Removing pattern %s from the entire testing set..." % name)
	for index, row in df_test_txt_copy.iterrows():
		df_test_txt_copy.set_value(index, 'Text', re.sub(pattern, "", row['Text']))

def extract_unicode(df_train, df_test, unicode_pattern):
	print("Extracting frequencies of unicode pattern...")
	counter_train = Counter()
	for index, row in df_train.iterrows():
		counter_train += Counter(re.findall(unicode_pattern, row['Text']))
	counter_test = Counter()
	for index, row in df_test.iterrows():
		counter_test += Counter(re.findall(unicode_pattern, row['Text']))
	counter_all = counter_train + counter_test
	output_unicode_freq_file = "%s/unicode.freq" % config.pattern_folder
	with open(output_unicode_freq_file, "w"):
		f.write("unicode,occurence" + os.linesep)
		for key, value in counter_all.most_common():
			f.write("%s,%d"%(key,value) + os.linesep)

def extract_all():
	with open(config.pattern_cache_file, "rb") as f:
		old_patterns = pickle.load(f)
	update_other = False # if false, no need to extract others patterns again
	
	for key, value in patterns.items():
		if not value or old_patterns.get(key) == value:
			print("Skip extracting pattern %s, since it hasn't changed" % key)
			continue
		update_other = True
		extract_pattern(key, value, config.pattern_folder)
		print("Updating pattern %s in cache..." % key)
		old_patterns[key] = value
		with open(config.pattern_cache_file, "wb") as f:
			pickle.dump(old_patterns, f)
	
	for key, value in patterns.items():
		remove_pattern(key, value)

	for key,value in other_patterns.items():
		if not update_other and (not value or old_patterns.get(key) == value):
			print("Skip extracting pattern %s, since it hasn't changed" % key)
			continue
		extract_pattern(key, value, config.pattern_folder)
		print("Updating pattern %s in cache..." % key)
		old_patterns[key] = value
		with open(config.pattern_cache_file, "wb") as f:
			pickle.dump(old_patterns, f)

	output_train_txt_file = "%s/training_text.cleaned_pattern.p" % config.data_folder
	output_test_txt_file = "%s/test_text.cleaned_pattern.p" % config.data_folder
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train_txt_copy, f)
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test_txt_copy, f)
