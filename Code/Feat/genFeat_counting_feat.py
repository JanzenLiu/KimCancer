#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import re
import pickle
import sys; sys.path.append("../"); sys.path.append("../Preprocess/")
from param_config import config
from reader import load_original_text, load_stratified_kfold
from feat_utils import dump_feat, dump_feats
from unicode_dict import unicodes

df_train_txt, df_test_txt = load_original_text()
skf = load_stratified_kfold()

def count_unicode_in_text(text, code_regex):
	return len(re.findall(code_regex, text, re.UNICODE))

def extract_unicode_count(code_regex, dump=False):
	feat_name = "count_of_unicode_%s" % code_regex[1:]
	df_train_txt[feat_name] = df_train_txt["Text"].apply(lambda x: count_unicode_in_text(x, code_regex))
	df_test_txt[feat_name] = df_test_txt["Text"].apply(lambda x: count_unicode_in_text(x, code_regex))
	if dump:
		dump_feat(df_train_txt, df_test_txt, feat_name)

def extract_all():
	############################
	## get unicode count feat ##
	############################
	with open(config.unicode_cache_file, "rb") as f:
		old_unicodes = pickle.load(f)
	for key, value in unicodes.items():
		# skip if the counting feature of the unicode has been extracted
		if key in old_unicodes.keys():
			continue
		extract_unicode_count(key, True)
