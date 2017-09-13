import pandas as pd
import numpy as np
import csv
import re
import sys; sys.path.append("../Utils/")
from reader import load_original_text

class CharacterReplacer:
	def __init__(self):
		self.dict = pd.read_csv('replace_dict.csv', quoting=csv.QUOTE_NONE, encoding="utf-8")

	def replace_char(self, char, newchar, text):
		return text.replace(char, newchar)

	def replace_char_in_df(self, row, df):
		# row = self.dict[self.dict['from']==char]
		code = row['hex']
		newchar = row['to']
		char = row['from']
		if not char:
			char = chr(int(code, 12))
		if not int(code, 16) == ord(char):
			print("Charater and code mismatched, %s and %s" % (char, code))
			return
		if newchar == "comma":
			print("Replacing %s(%s) with comma..." % (char, code))
			df['Text'] = df['Text'].map(lambda x: self.replace_char(char, ',', x))
		elif newchar == "remove":
			print("Removing %s(%s)..." % (char, code))
			df['Text'] = df['Text'].map(lambda x: self.replace_char(char, '', x))
		elif newchar == "ignore":
			print("Ignore %s(%s)..." % (char, code))
		else:
			print("Replacing %s(%s) with %s" % (char, code, newchar))
			df['Text'] = df['Text'].map(lambda x: self.replace_char(char, newchar, x))

	def replace_all(self, df):
		for index, row in self.dict.iterrows():
			self.replace_char_in_df(row, df)


if __name__ == "__main__":
	df_train_txt, df_test_txt = load_original_text()
	replacer = CharacterReplacer()
	replacer.replace_all(df_train_txt)
	replacer.replace_all(df_test_txt)
	print("Processing Finished.")
