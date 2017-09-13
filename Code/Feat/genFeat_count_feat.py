#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import nltk
import re
import pickle
import sys
sys.path.append("../")
sys.path.append("../EDA/")
sys.path.append("../Preprocess/")
sys.path.append("../Utils/")
from param_config import config
from tokenizer import tokenize, tokenize_df
from reader import load_original_text
from writer import dump_feature
from unicode_dict import unicodes


###########################
### auxiliary functions ###
###########################
def count_pattern_in_text(text, regex, ignore_case=True):
	if not ignore_case:
		return len(re.findall(regex, text, re.UNICODE))
	return len(re.findall(regex, text, re.UNICODE|re.I))

def count_sent_in_doc(doc):
	if type(doc) == str:
		doc = nltk.sent_tokenize(doc)
	return len(doc)

def count_word_in_sent(sent):
	if type(sent) == str:
		sent = nltk.word_tokenize(sent)
	# add filter? filter out tokens like comma, period and so on
	return len(sent)

def extract_tokens(df):
	tokenize_df(df)


##########################################
### extract count of specified segment ###
##########################################
def extract_word_count(df, word, text_col="Text"):
	print("Extracting count of word %s..." % word)
	feat_name = "count_of_word_%s" % word.lower()
	df[feat_name] = df[text_col].map(lambda x: count_pattern_in_text(x, word))

def extract_pattern_count(df, regex, pattern_name, text_col="Text"):
	print("Extracting count of pattern %s..." % pattern_name)
	feat_name = "count_of_pattern_%s" % pattern_name.replace(" ", "_").lower()
	df[feat_name] = df[text_col].map(lambda x: count_pattern_in_text(x, regex))

def extract_char_count(df, char, text_col="Text"):
	print("Extracting count of character %s..." % char)
	feat_name = "count_of_char_0x%04x" % ord(char)
	df[feat_name] = df[text_col].map(lambda x: count_pattern_in_text(x, char))


###########################################
### extract count of basic nlp elements ###
###########################################
def extract_sents_count(df, text_col="Text"):
	print("Extracting count of sentences in %s..." % text_col)
	df["count_of_sents"] = df[text_col].map(count_sent_in_doc)

def extract_words_count(df, text_col="Text"):
	print("Extracting count of words in %s..." % text_col)
	feat_name = "count_of_words_in_%s" % text_col.lower()
	df[feat_name] = df[text_col].map(count_word_in_sent)

def extract_chars_count(df, text_col="Text"):
	print("Extracting length of %s..." % text_col)
	feat_name = "count_of_chars_in_%s" % text_col.lower()
	df[feat_name] = df[text_col].map(lambda x: len(x))


##########################################################
### extract count of biological/chemical/medical terms ###
##########################################################
def extract_gene_share(df):
	print("Extracting gene share...")
	df["share_gene"] = df.apply(lambda x: count_pattern_in_text(x["Text"], x["Gene"]))

def extract_variation_share(df):
	print("Extracting variation share...")
	df["share_variation"] = df.apply(lambda x: count_pattern_in_text(x["Text"], x["Variation"]))

def extract_gene_count(df, gene):
	print("Extracting count of gene %s..." % gene)
	feat_name = "count_of_gene_%s" % gene.upper().replace(" ","_")
	df[feat_name] = df["Text"].map(lambda x: count_pattern_in_text(x, gene))

def extract_variation_count(df, var):
	print("Extracting count of vairation %s..." % var)
	feat_name = "count_of_variation_%s" % var.upper().replace(" ","_")
	df[feat_name] = df["Text"].map(lambda x: count_pattern_in_text(x, var))

def extract_all_gene_count(df, gene_list=None):
	print("Extracting count of all genes...")
	if not gene_list:
		gene_list = df["Gene"].unique()
	for gene in gene_list:
		extract_gene_count(df, gene)

def extract_all_variation_count(df, var_list=None):
	print("Extractig count of all variations...")
	if not var_list:
		var_list = df["Variation"].unique()
	for var in var_list:
		extract_variation_count(df, var)


