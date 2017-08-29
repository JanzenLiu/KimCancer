#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import json
import sys; sys.path.append("../")
import pickle
from param_config import config
from reader import df_train_txt, df_test_txt
from pattern_dict import patterns, other_patterns

df_train_txt_copy = df_train_txt.copy()
df_test_txt_copy = df_test_txt.copy()

## extract single pattern
def extract_pattern(name, pattern, path, remove_match=False):
	print("Extracting pattern %s from the entire training set..." % name)
	# res_train = {row['ID']:re.findall(pattern, row['Text']) for index,row in df_train_txt.iterrows()}
	res_train = {}
	for index, row in df_train_txt_copy.iterrows():
		res_train[row['ID']] = re.findall(pattern, row['Text'])
		if remove_match:
			row['Text'] = re.sub(pattern, "", row['Text'])
	filename  = "%s/%s.train.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_train, f, indent=2)

	print("Extracting pattern %s from the entire testing set..." % name)
	# res_test = {row['ID']:re.findall(pattern, row['Text']) for index,row in df_test_txt.iterrows()}
	res_test = {}
	for index, row in df_test_txt_copy.iterrows():
		res_test[row['ID']] = re.findall(pattern, row['Text'])
		if remove_match:
			row['Text'] = re.sub(pattern, "", row['Text'])
	filename  = "%s/%s.test.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_test, f, indent=2)

def extract_all():
	with open(config.pattern_cache_file, "rb") as f:
		old_patterns = pickle.load(f)
	for key, value in patterns.items():
		if not value or old_patterns.get(key) == value:
			print("Skip the process of extracting pattern %s, it hasn't changed since last extraction" % key)
			continue
		extract_pattern(key, value, config.pattern_folder, remove_match=True)
		print("Updating pattern %s in cache..." % key)
		old_patterns[key] = value
		with open(config.pattern_cache_file, "wb") as f:
			pickle.dump(old_patterns, f)
	for key,value in other_patterns.items():
		if not value or old_patterns.get(key) == value:
			print("Skip the process of extracting pattern %s, it hasn't changed since last extraction" % key)
			continue
		extract_pattern(key, value, config.pattern_folder)
		print("Updating pattern %s in cache..." % key)
		old_patterns[key] = value
		with open(config.pattern_cache_file, "wb") as f:
			pickle.dump(old_patterns, f)
	output_train_txt_file = "%s/training_text.processed.p" % config.data_folder
	output_test_txt_file = "%s/test_text.processed.p" % config.data_folder
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train_txt_copy, f)
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test_txt_copy, f)
