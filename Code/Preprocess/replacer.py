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
			"jpg": r"[\w\.]+\.jpg", #should be processed earlier than url
			"url": r"(?:https?|ftp)?(?:\/{1,2})?(?:www\.)?[\w+\.\-]+\.(?:com|org|fr|jp|us|hk|cn|net|ch|gov|edu|ca|uk|de|info|dk|tw|il)(?:\:\d+)?(?:\/[^\b ,\)\]]+)*\/?", # case sensitive
			"doi": r"doi:[\w\.\/\-]+",
			"equation": r"[a-z\u00ff-\uffff]+ ?[=<>≥≤∈≦≠][\d\.\-\^\*:+,\/\u00ff-\uffff ex]+(?![A-Z ])",
			"version": r"(?<![\-\w])v(?:er(?:sion)?)?[ \.]{,2}\d{1,2}(?:\.\d+)*(?![\w\-])", # for each match: match[0] != 'V' or match[1:].isdigit())
			"comma_number": r"\d{1,3}(?:,\d{3})+(?:\.\d+)?",
			# "number": r"\d+(?:,\d{3})?(?:\.\d+)?",
			"all_del": r"(?:[cgmrp]\.)?[A-Z]?\d+(?:_?[A-Z]?\d+)?del(?:[A-Z]+)",
			"all_ins": r"(?:[cgmrp]\.)?[A-Z]?\d+(?:_?[A-Z]?\d+)?ins(?:[A-Z]+)?",
			"all_delins": r"(?:[cgmrp]\.)?[A-Z]?\d+(?:_?[A-Z]?\d+)?delins(?:[A-Z]+)?",
			"all_dup": r"(?:[cgmrp]\.)?[A-Z]?\d+(?:_?[A-Z]?\d+)?dup(?:[A-Z]+)?",
			"all_trunc": r"(?:[cgmrp]\.)?[A-Z]?\d+(?:_?[A-Z]?\d+)?trunc(?:[A-Z]+)?",
			"all_splice": r"(?:[cgmrp]\.)?[A-Z]?\d+(?:_?[A-Z]?\d+)?splice(?:[A-Z]+)?",
			"all_fs": r"(?:[cgmrp]\.)?[A-Z]\d+[A-Z]?fs(?:(?:\*|Ter)\d+)?", # exclusion: "E2Fs", "Y527FS"
			"all_mut": r"(?:[cgmrp]\.)?\d+[A-Z]+ ?> ?[A-Z]+",
			"all_null": r"null\d+[A-Z]",
			"table":,
			"figure":
			# "sentence_segmentation": # actually it should be called shitty sentence segmentation
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
