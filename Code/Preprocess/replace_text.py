#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import re
import pickle
import sys; sys.path.append("../")
from param_config import config
from reader import load_original_text
from unicode_dict import unicodes

df_train_txt, df_test_txt = load_original_text()

def replace_unicode(code_regex, new_code):
	print("Replacing unicode %s in the entire training set..." % new_code)
	for index, row in df_train_txt.iterrows():
		df_train_txt.set_value(index, 'Text', re.sub(code_regex, new_code, row['Text'], re.UNICODE))
	print("Replacing unicode %s in the entire testing set..." % new_code)
	for index, row in df_test_txt.iterrows():
		df_test_txt.set_value(index, 'Text', re.sub(code_regex, new_code, row['Text'], re.UNICODE))

def replace_all():
	for key, value in unicodes.items():
		replace_unicode(key, value)

	output_train_txt_file = "%s/training_text.replaced_unicode.p" % config.data_folder
	output_test_txt_file = "%s/test_text.replaced_unicode.p" % config.data_folder
	print("Saving replaced text data of the entire training set...")
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train_txt, f)
	print("Saving replaced text data of the entire testing set...")
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test_txt, f)