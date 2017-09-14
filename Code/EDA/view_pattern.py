import pandas as pd
import numpy as np
import pickle
import nltk
import re
import sys; sys.path.append('../Utils')

with open('../../Data/train_text.processed.p', 'rb') as f:
	train = pickle.load(f)
with open('../../Data/test_text.processed.p', 'rb') as f:
	test = pickle.load(f)

def log_pattern(pattern, flag=re.I|re.U, pattern_name):
	with open('../../Temp/%s.pattern.log', 'w') as f:
		for index, row in train.iterrows()：
			matches = re.findall(pattern, row['Text'], flag)
			if not matches:
				continue
			f.write("train #%d\n" % int(index))
			for match in matches:
				f.write(match, '\n')
			f.write('\n')
			
		for index, row in test.iterrows()：
			matches = re.findall(pattern, row['Text'], flag)
			if not matches:
				continue
			f.write("test #%d\n" % int(index))
			for match in matches:
				f.write(match, '\n')
			f.write('\n')