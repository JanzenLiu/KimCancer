import numpy as np
import pandas as pd
import re
import json
import sys
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
			re.sub(pattern, "", row['Text'])
	filename  = "%s/%s.train.json" % (path, name)
	with open(filename, 'w') as f:
		json.dump(res_train, f, indent=2)

	print("Extracting pattern %s from the entire testing set..." % name)
	# res_test = {row['ID']:re.findall(pattern, row['Text']) for index,row in df_test_txt.iterrows()}
	res_test = {}
	for index, row in df_test_txt_copy.iterrows():
		res_test[row['ID']] = re.findall(pattern, row['Text'])
		if remove_match:
			re.sub(pattern, "", row['Text'])
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
	if remove_match:
		output_train_txt_file = "%s/training_text.processed" % config.data_folder
		output_test_txt_file = "%s/test_text.processed" % config.data_folder
		df_train_txt_copy.to_csv(output_train_txt_file, sep="\|\|")
		df_test_txt_copy.to_csv(output_test_txt_file, sep="\|\|")