import pandas as pd
import numpy as np
import nltk

doc = [
		"Ius eu tale aeque, quo erat verterem nominati ex, usu solum erroribus concludaturque ad. Id vel electram signiferumque, purto omittantur ne sea. Eum quod epicuri inimicus ad, eu ocurreret dignissim adolescens mei, usu te legere nonumes maiorum. Vis ne tota meliore. Ei est probo dignissim. Vis cu mazim ceteros disputando, mea velit nostro iracundia at.",
		"Vis tota zril facilisis ne. Ut postea ceteros sed, cum odio mundi eu, id nam velit periculis. Vim error graeci philosophia an, mea ea mucius facilisi indoctum. Cu vim mutat tempor, rebum recusabo efficiendi duo et, mea id pertinacia reformidans. Diam debet sed id, has et prompta molestie perpetua, eam epicurei maiestatis scribentur ei.",
		"Salutandi sententiae duo cu, sed cu utamur oportere, eos unum tempor inermis no. Eam iudico civibus officiis at. Ei ius expetenda moderatius, sea ne honestatis accommodare. Enim augue summo nam ex. Quaeque singulis ut pro, vix an ridens nusquam, et vel posse choro reformidans. Duo at eros vocent insolens.",
		"Dolor semper detraxit sit ne. Dicunt graecis no mei, novum homero laudem an nec, te cibo maluisset ius. Doctus mnesarchum cum ad, ea detracto iracundia mel. Sit ne munere maiestatis, putant nostrud fierent ad vim, eu nostrud adipisci mea. Cu oblique rationibus nec. Inani detracto inciderint vix at, porro epicurei ei usu.",
		"Adipiscing necessitatibus an pro, vel stet omnium appareat no. Euismod voluptaria et nam, per an errem latine. Et sed ludus conclusionemque, alterum corpora explicari eum te. Esse singulis moderatius per ea. Homero aliquid his te, ei eam everti tritani accommodare, luptatum accusata ei nam."
	]

class Debug():
	def __init__(self, doc=doc):
		self.doc = doc
		self.df_txt = pd.DataFrame(data=list(range(5)), columns=['ID'])
		self.df_txt["Text"] = self.doc

debug = Debug()