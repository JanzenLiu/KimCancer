import pandas as pd
import numpy as np
import pickle
import csv
import re
import sys; sys.path.append("../Utils/")
from reader import load_original_text

class CharacterReplacer:
	def __init__(self):
		self.dict = pd.read_csv('char_map', quoting=csv.QUOTE_NONE, encoding="utf-8")

	def replace_char(self, char, newchar, text):
		return text.replace(char, newchar)

	def replace_char_in_df(self, row, df):
		# row = self.dict[self.dict['from']==char]
		code = row['hex']
		newchar = row['to']
		char = row['from']
		if not code or not newchar:
			return
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
			print("Replacing %s(%s) with %s..." % (char, code, newchar))
			df['Text'] = df['Text'].map(lambda x: self.replace_char(char, newchar, x))

	def replace_all(self, df):
		for index, row in self.dict.iterrows():
			self.replace_char_in_df(row, df)


class PatternReplacer:
	def __init__(self):
		self.dict = {
			"base sequence": r"(?<=[^\w])[ATCUG]{4,}(?=[^\w])",
			"url": r"(?:https?|ftp)?(?:\/{1,2})?(?:www\.)?[\w+\.\-]+\.(?:com|org|fr|jp|us|hk|cn|net|ch|gov|edu|ca|uk|de|info|dk|tw|il)(?:\:\d+)?(?:\/[^\b ,\)\]]+)*\/?", # case sensitive
			"jpg": r"[\w\.]+\.jpg",
			"doi": r"doi:[\w\.\/\-]+",
			"equation": r"[a-z\u00ff-\uffff]+ ?=[\d\.\-:+,\/ e]+",
			"version": r"v(?:er(?:sion)?)?\.? ?\d{1,2}[\.\d]*",
			"sentence_segmentation": # actually it should be called shitty sentence segmentation
		}

	def replace_base_sequence(self, text):
		return re.sub(self.dict["base sequence"], "baseseq", text, re.I)

	def replace_url(self, text):
		return re.sub(self.dict["url"], "urllink", text, re.I)

	def replace_jpg(self, text):
		return re.sub(self.dict["jpg"], "jpg figure", text ,re.I)


def view_pattern(pattern, array):
	for doc in array:
		for match in re.findall(pattern, doc):
			print(match)

if __name__ == "__main__":
	df_train_txt, df_test_txt = load_original_text()
	replacer = CharacterReplacer()
	replacer.replace_all(df_train_txt)
	replacer.replace_all(df_test_txt)
	print("Processing Finished.")

	print("Saving processed text...")
	with open('../../Data/train_text.processed.p', 'wb') as f:
		pickle.dump(df_train_txt, f)
	with open('../../Data/test_text.processed.p', 'wb') as f:
		pickle.dump(df_test_txt, f)
