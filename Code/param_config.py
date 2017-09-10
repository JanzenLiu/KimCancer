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
		self.external_data_folder = "../../External"
		self.vocabulary_folder = "../../Vocabulary"
		self.feat_folder = feat_folder # directory to store processed feature data
		self.pattern_folder = pattern_folder # directory to store extracted subtext from text using specific patterns
		self.original_train_text_path = "%s/training_text" % self.data_folder
		self.original_train_variant_path = "%s/training_variants" % self.data_folder
		self.original_test_text_path = "%s/test_text" % self.data_folder
		self.original_test_variant_path = "%s/test_variants" % self.data_folder
		self.debug_data_path = "%s/debug.p" % self.data_folder
		self.special_characters_path = "%s/special_characters.txt" % self.vocabulary_folder
		self.train_tokens_path = "%s/train.tokens.json" % self.data_folder
		self.test_tokens_path = "%s/test.tokens.json" % self.data_folder
		self.processed_train_data_path = "%s/train.processed.p" % self.data_folder
		self.processed_test_data_path = "%s/test.processed.p" % self.data_folder
		self.main_dictionary_path = '%s/350k_dictionary.txt' % self.external_data_folder
		self.suppliment_dictionary_path = '%s/10k_dictionary.txt' % self.external_data_folder
		self.bio_corpus_path = "%s/bioCorpus_5000.txt" % self.external_data_folder
		self.special_words_train_savepath = '%s/special_words.train.json' % self.vocabulary_folder
		self.special_words_test_savepath = '%s/special_words.test.json' % self.vocabulary_folder
		self.common_words_train_savepath = '%s/common_words.train.json' % self.vocabulary_folder
		self.common_words_test_savepath = '%s/common_words.test.json' % self.vocabulary_folder
		self.unique_special_words_path = "%s/all.special_words.txt" % self.vocabulary_folder
		self.unique_common_words_path = "%s/all.common_words.txt" % self.vocabulary_folder

		## nlp related
		self.basic_tfidf_ngram_range = basic_tfidf_ngram_range
		self.basic_tfidf_vocabulary_type = basic_tfidf_vocabulary_type
		self.cooccurrence_tfidf_ngram_range = cooccurrence_tfidf_ngram_range
		self.cooccurrence_word_exclude_stopword = cooccurrence_word_exclude_stopword
		self.stemmer_type = stemmer_type

		## transform for count features
		self.count_feat_transform = count_feat_transform

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
		if not os.path.exists(self.vocabulary_folder):
			os.makedirs(self.vocabulary_folder)

## initialize a param config
config = ParamConfig(feat_folder="../../Feat/dev",
		     pattern_folder="../../Pattern/dev",
		     stemmer_type="porter",
		     cooccurrence_word_exclude_stopword=False)
