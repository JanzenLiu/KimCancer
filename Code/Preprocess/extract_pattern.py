import numpy as np
import pandas as pd
import re
import json
import sys
sys.path.append("../")
from param_config import config
from reader import df_train_txt, df_test_txt
from pattern_dict import patterns

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

def extract_all():
	for key, value in patterns.items():
		if not value is None:
			extract_pattern(key, value, config.pattern_folder)