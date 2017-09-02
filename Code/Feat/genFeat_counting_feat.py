#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import re
import pickle
import sys; sys.path.append("../"); sys.path.append("../Preprocess/")
from param_config import config
from reader import load_original_text
from unicode_dict import unicodes

df_train_txt, df_test_txt = load_original_text()

def count_unicode_in_text(text, code_regex):
	return len(re.findall(code_regex, text, re.UNICODE))

def extract_unicode_count(code_regex, code_name):
	feat_name = "count_of_unicode_%s" % code_name
	output_train_count_file = "%s/%s.train.p" % (config.feat_folder, feat_name)
	output_test_count_file = "%s/%s.test.p" % (config.feat_folder, feat_name)

	print("Generating feature %s for the entire training set..." % feat_name)
	df_train_txt[feat_name] = df_train_txt["Text"].apply(count_unicode_in_text)
	with open(output_train_count_file, "wb") as f:
		pickle.dump(df_train_txt[feat_name], f)	
	print("Generating feature %s for the entire testing set..." % feat_name)
	df_test_txt[feat_name] = df_test_txt["Text"].apply(count_unicode_in_text)
	with open(output_test_count_file, "wb") as f:
		pickle.dump(df_test_txt[feat_name], f)

def extract_all():
	for key, value in unicodes.items():
		extract_unicode_count(key, value)