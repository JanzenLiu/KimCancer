import numpy as np
import pandas as pd
import re
import json
import sys
import pickle
sys.path.append("../")
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
	for key, value in patterns.items():
		if not value is None:
			extract_pattern(key, value, config.pattern_folder, remove_match=True)
	for key,value in other_patterns.items():
		if not value is None:
			extract_pattern(key, value, config.pattern_folder)
	output_train_txt_file = "%s/training_text.processed.p" % config.data_folder
	output_test_txt_file = "%s/test_text.processed.p" % config.data_folder
	with open(output_train_txt_file, "wb") as f:
		pickle.dump(df_train_txt_copy, f)
	with open(output_test_txt_file, "wb") as f:
		pickle.dump(df_test_txt_copy, f)