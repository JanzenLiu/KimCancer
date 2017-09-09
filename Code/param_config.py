#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import pickle
import numpy as np

############
## Config ##
############
class ParamConfig:
	def __init__(self,
		     feat_folder,
		     pattern_folder,
		     basic_tfidf_ngram_range=(1,3),
		     basic_tfidf_vocabulary_type="common",
		     cooccurrence_tfidf_ngram_range=(1,1),
		     cooccurrence_word_exclude_stopword=False,
		     stemmer_type="snowball",
		     count_feat_transform=np.sqrt):

		self.n_rows_train = 3321 # hardcoded value
		self.n_rows_test = 5668 # hardcoded value
		self.n_classes = 9

		## CV params
		self.n_runs = 3
		self.n_folds = 5
		self.stratified_label = "disease_class"

		## path
		self.data_folder = "../../Data"
		self.feat_folder = feat_folder # directory to store processed feature data
		self.pattern_folder = pattern_folder # directory to store extracted subtext from text using specific patterns
		self.original_train_text_path = "%s/training_text" % self.data_folder
		self.original_train_variant_path = "%s/training_variants" % self.data_folder
		self.original_test_text_path = "%s/test_text" % self.data_folder
		self.original_test_variant_path = "%s/test_variants" % self.data_folder
		self.processed_train_data_path = "%s/train.processed.p" % self.data_folder
		self.processed_test_data_path = "%s/test.processed.p" % self.data_folder
		self.pattern_cache_file = "%s/patterns.last_processed.p" % self.pattern_folder
		self.unicode_cache_file = "%s/unicodes.last_processed.p" % self.data_folder

		self.main_dictionary_path = '../../External/350k_dictionary.txt'
		self.suppliment_dict_path = '../../External/10k_dictionary.txt'
		self.special_words_train_savepath = '../../Vocabulary/special_words.train.json'
		self.special_words_test_savepath = '../../Vocabulary/special_words.test.json'
		self.common_words_train_savepath = '../../Vocabulary/common_words.train.json'
		self.common_words_test_savepath = '../../Vocabulary/common_words.test.json'

		## nlp related
		self.basic_tfidf_ngram_range = basic_tfidf_ngram_range
		self.basic_tfidf_vocabulary_type = basic_tfidf_vocabulary_type
		self.cooccurrence_tfidf_ngram_range = cooccurrence_tfidf_ngram_range
		self.cooccurrence_word_exclude_stopword = cooccurrence_word_exclude_stopword
		self.stemmer_type = stemmer_type

		## transform for count features
		self.count_feat_transform = count_feat_transform

		## create cache file for special unicodes used to extract features
		if not os.path.exists(self.unicode_cache_file):
			unicodes = {}
			with open(self.unicode_cache_file, "wb") as f:
				pickle.dump(unicodes, f)

		## create feat folder
		if not os.path.exists(self.feat_folder):
			os.makedirs(self.feat_folder)

		## create folder for the training, testing feat and raw output
		if not os.path.exists("%s/All" % self.feat_folder):
			os.makedirs("%s/All" % self.feat_folder)
		if not os.path.exists("%s/Raw" % self.feat_folder):
			os.makedirs("%s/Raw" % self.feat_folder)

		## create pattern folder and cache file for processed patterns
		if not os.path.exists(self.pattern_folder):
			os.makedirs(self.pattern_folder)
		if not os.path.exists(self.pattern_cache_file):
			patterns = {}
			with open(self.pattern_cache_file, "wb") as f:
				pickle.dump(patterns, f)

		## create folder for each run and fold
		for run in range(1, self.n_runs+1):
			for fold in range(1, self.n_folds+1):
				path = "%s/Run%d/Fold%d" % (self.feat_folder, run, fold)
				if not os.path.exists(path):
					os.makedirs(path)

		## create folder for vocabulary
		if not os.path.exists('../../Vocabulary'):
			os.makedirs('../../Vocabulary')

## initialize a param config
config = ParamConfig(feat_folder="../../Feat/dev",
		     pattern_folder="../../Pattern/dev",
		     stemmer_type="porter",
		     cooccurrence_word_exclude_stopword=False)
