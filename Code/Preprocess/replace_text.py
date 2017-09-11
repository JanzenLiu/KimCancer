#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import re
import pickle
import sys; sys.path.append("../"); sys.path.append("../Utils/")
from param_config import config
from reader import load_original_text
from unicode_dict import unicodes

'''
Replace a specific Unicode character with a specified piece of text.
Note: The replacement happens on the global variable df_train_txt and df_test_txt, which should be improved
@param:
	code_regex: regular expression for the Unicode character
	new_code: text used to replace the character
	dfs: a list of dataframes with 'Text' column
'''
def replace_unicode(code_regex, new_code, dfs):
	print("Replacing unicode %s (%s)..." % (code_regex[1:], new_code))
	for df in dfs:
		for index, row in df.iterrows():
			df.set_value(index, 'Text', re.sub(code_regex, new_code, row['Text'], re.UNICODE))

'''
1. Perform replacement with all charcater/substitute specified in unicode_dict.py
2. Save the replaced text to path specified inside the function
@param:
	dfs: a list of dataframes to perform replacement on
	codes: a dictionary for code replacement
'''
def replace_all(dfs, codes):
	for key, value in codes.items():
		replace_unicode(key, value, dfs)


if __name__ == "__main__":
	df_train_txt, df_test_txt = load_original_text()
	replace_all([df_train_txt, df_test_txt], unicodes)
	output_train_txt_file = "%s/training_text.replaced_unicode.p" % config.data_folder
	output_test_txt_file = "%s/test_text.replaced_unicode.p" % config.data_folder
	print("Saving text with speicial characters replaced...")
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train_txt, f)
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test_txt, f)