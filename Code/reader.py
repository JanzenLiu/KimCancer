import numpy as np
import pandas as pd
import pickle
import sys
import os
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
	if not (os.path.exists(replaced_train_text_path) and os.path.exists(replaced_test_text_path)):
		print("[Warning] Replaced text files do not exist")
		return load_original_text()
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
	if not (os.path.exists(extracted_train_text_path) and os.path.exists(extracted_test_text_path)):
		print("[Warning] Extracted text files do not exist")
		return load_original_text()
	print("Loading extracted text for the entire training set...")
	with open(extracted_train_text_path, "rb") as f:
		df_train_txt = pickle.load(f)
	print("Loading extracted text for the entire testing set...")
	with open(extracted_test_text_path, "rb") as f:
		df_test_txt = pickle.load(f)
	return df_train_txt, df_test_txt

def load_processed_data():
	with open(config.processed_train_data_path, "rb") as f:
		df_train = pickle.load(f)
	with open(config.processed_test_data_path, "rb") as f:
		df_test = pickle.load(f)
	return df_train, df_test

def load_combined_data(version="original"):
	if version == "replaced":
		df_train_txt, df_test_txt = load_replaced_text()
	elif version == "extracted":
		df_train_txt, df_test_txt = load_extracted_text()
	else:
		if version != "original":
			print("[Warning] Version not found, return original data")
		df_train_txt, df_test_txt = load_original_text()

	df_train_var, df_test_var = load_original_variants()

	y_train = df_train_var["Class"]
	id_test = df_test_var["ID"]
	df_train = pd.merge(df_train_txt, df_train_var, how="left", on="ID").fillna("")
	df_train = df_train.drop(["ID", "Class"], axis=1)
	df_test = pd.merge(df_test_txt, df_test_var, how="left", on="ID").fillna("")
	df_test = df_test.drop(["ID"], axis=1)
	
	df_combine = pd.concat((df_train, df_test), axis=0, ignore_index=True)
	return df_combine, y_train, id_test

def load_stratified_kfold(stratified_label=config.stratified_label):
	with open("%s/stratifiedKFold.%s.p" % (config.data_folder, stratified_label), "rb") as f:
		skf = pickle.load(f)
	return skf
