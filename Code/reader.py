import numpy as np
import pandas as pd
import pickle
import sys
from param_config import config

def load_original_text():
	df_train_txt = pd.read_csv(config.original_train_text_path, 
		sep="\|\|", header=None, skiprows=1, names=["ID", "Text"], engine="python")
	df_test_txt = pd.read_csv(config.original_test_text_path, 
		sep="\|\|", header=None, skiprows=1, names=["ID", "Text"], engine="python")
	return df_train_txt, df_test_txt

def load_original_variants():
	df_train_var = pd.read_csv(config.original_train_variant_path)
	df_test_var = pd.read_csv(config.original_test_variant_path)
	return df_train_var, df_test_var

def load_replaced_text():
	replaced_train_text_path = "%s/training_text.replaced_unicode.p" % config.data_folder
	replaced_test_text_path = "%s/test_text.replaced_unicode.p" % config.data_folder
	print("Loading replaced text for the entire training set...")
	with open(replaced_train_text_path, "rb") as f:
		df_train_txt = pickle.load(f)
	print("Loading replaced text for the entire testing set...")
	with open(replaced_test_text_path, "rb") as f:
		df_test_txt = pickle.load(f)
	return df_train_txt, df_test_txt

def load_extracted_text():
	extracted_train_text_path = "%s/training_text.extracted_pattern.p" % config.data_folder
	extracted_test_text_path = "%s/test_text.extracted_pattern.p" % config.data_folder
	print("Loading extracted text for the entire training set...")
	with open(extracted_train_text_path, "rb") as f:
		df_train_txt = pickle.load(f)
	print("Loading extracted text for the entire testing set...")
	with open(extracted_test_text_path, "rb") as f:
		df_test_txt = pickle.load(f)
	return df_train_txt, df_test_txt