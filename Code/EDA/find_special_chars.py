import re
import sys; sys.path.append('../'); sys.path.append('../Utils/')
from param_config import config
from reader import load_original_text
from writer import dump_words

normal_chars = [',', '.', '?', '!', ':', ';', 
				'(', ')', '[', ']', '{', '}',
				'>', '<', '=', '+', '-', '/',
				'@', '#', '$', '%', '^', '&',
				'*', '`', '~', '\'', '\"', '\\', '\t']

def special_char_set_lct(text):
	res = re.sub(r'\w', '', text)
	res = res.replace(" ", "")
	for char in normal_chars:
		res = res.replace(char, '')
	return set(res)

def special_char_set_lkc(text):
	return set(re.findall(r'[\u00ff-\uffff]', text))

if __name__ == "__main__":
	df_train_txt, df_test_txt = load_original_text()
	train_special_chars = set()
	test_special_chars = set()

	for index, row in df_train_txt.iterrows():
		# train_special_chars_lct.update(special_char_set(row['Text']))
		train_special_chars.update(special_char_set_lkc(row['Text']))
	for index, row in df_test_txt.iterrows():
		# test_special_chars_lct.update(special_char_set(row['Text']))
		test_special_chars.update(special_char_set_lkc(row['Text']))
	special_chars = train_special_chars.copy()
	special_chars.update(test_special_chars)

	dump_words(special_chars, config.special_characters_path, "Saving special characters...")
