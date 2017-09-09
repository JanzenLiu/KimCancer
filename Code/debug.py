import pandas as pd
import numpy as np
import pickle
import nltk
import os
import sys
sys.path.append('../')
sys.path.append('../EDA/')
sys.path.append('../Preprocess/')
sys.path.append('../Feat/')
sys.path.append('../Model/')
from param_config import config
from reader import *
from tools import *

class Debug():
	def __init__(self, doc, df, vocab):
		self.doc = doc
		self.df = df
		self.vocab = vocab


if not os.path.exists(config.debug_data_path):
	###################################
	### random meaningless document ###
	###################################
	doc = [
			"Ius eu tale aeque, quo erat verterem nominati ex, usu solum erroribus concludaturque ad. Id vel electram signiferumque, purto omittantur ne sea. Eum quod epicuri inimicus ad, eu ocurreret dignissim adolescens mei, usu te legere nonumes maiorum. Vis ne tota meliore. Ei est probo dignissim. Vis cu mazim ceteros disputando, mea velit nostro iracundia at.",
			"Vis tota zril facilisis ne. Ut postea ceteros sed, cum odio mundi eu, id nam velit periculis. Vim error graeci philosophia an, mea ea mucius facilisi indoctum. Cu vim mutat tempor, rebum recusabo efficiendi duo et, mea id pertinacia reformidans. Diam debet sed id, has et prompta molestie perpetua, eam epicurei maiestatis scribentur ei.",
			"Salutandi sententiae duo cu, sed cu utamur oportere, eos unum tempor inermis no. Eam iudico civibus officiis at. Ei ius expetenda moderatius, sea ne honestatis accommodare. Enim augue summo nam ex. Quaeque singulis ut pro, vix an ridens nusquam, et vel posse choro reformidans. Duo at eros vocent insolens.",
			"Dolor semper detraxit sit ne. Dicunt graecis no mei, novum homero laudem an nec, te cibo maluisset ius. Doctus mnesarchum cum ad, ea detracto iracundia mel. Sit ne munere maiestatis, putant nostrud fierent ad vim, eu nostrud adipisci mea. Cu oblique rationibus nec. Inani detracto inciderint vix at, porro epicurei ei usu.",
			"Adipiscing necessitatibus an pro, vel stet omnium appareat no. Euismod voluptaria et nam, per an errem latine. Et sed ludus conclusionemque, alterum corpora explicari eum te. Esse singulis moderatius per ea. Homero aliquid his te, ei eam everti tritani accommodare, luptatum accusata ei nam."
		]

	#######################################################################################################
	### select 9 records from train data (one from each class) and 16 from test data to form debug data ###
	#######################################################################################################
	df_train, df_test = load_original_data()

	# insert fake class to selected test records
	num_test_in_debug = 16
	df_debug_test = df_test.iloc[-num_test_in_debug:].copy()
	df_debug_test['Class'] = np.ones(num_test_in_debug)

	df_debug = pd.DataFrame(columns=df_train.columns)
	for i in range(1, 1+config.n_classes):
		df_debug = df_debug.append(df_train[df_train['Class']==i].iloc[0], ignore_index=True)
	df_debug = df_debug.append(df_debug_test, ignore_index=True)

	###########################
	### shrinked vocabulary ###
	###########################
	vocab_real = list(load_vocabulary())
	vocab_debug = vocab_real[:1000] + vocab_real[-1000:]

	### initiate debug instance
	debug = Debug(doc=doc, df=df_debug, vocab=vocab_debug)
	with open(config.debug_data_path, "wb") as f:
		pickle.dump(debug, f)

else:
	with open(config.debug_data_path, "rb") as f:
		debug = pickle.load(f)