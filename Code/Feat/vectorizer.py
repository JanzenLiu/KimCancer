import re
import sys; sys.path.append('../')
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from param_config import config


##############
### TF-IDF ###
##############
class StemmedTfidfVectorizer(TfidfVectorizer):
	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, self).build_analyzer()
		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

token_pattern = r"(?u)\b\w\w+\b"
tfidf__norm = "l2"
tfidf__max_df = 0.75
tfidf__min_df = 3
tfidf__vocabulary = None
def getTFV(token_pattern = token_pattern,
           norm = tfidf__norm,
           max_df = tfidf__max_df,
           min_df = tfidf__min_df,
	   vocabulary = tfidf__vocabulary,
           ngram_range = (1, 1),
           stop_words = 'english'):
    tfv = StemmedTfidfVectorizer(min_df=min_df, max_df=max_df, max_features=None, 
                                 strip_accents='unicode', analyzer='word', token_pattern=token_pattern,
                                 ngram_range=ngram_range, use_idf=True, smooth_idf=True, sublinear_tf=True,
                                 stop_words = stop_words, norm=norm, vocabulary=vocabulary)
    return tfv

###########
### BOW ###
###########
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(CountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))
   
token_pattern = r"(?u)\b\w\w+\b"
bow__max_df = 0.75
bow__min_df = 3
bow__vocabulary = None
def getBOW(token_pattern = token_pattern,
           max_df = bow__max_df,
           min_df = bow__min_df,
	   vocabulary = bow__vocabulary,
           ngram_range = (1, 1),
           stop_words = 'english'):
    bow = StemmedCountVectorizer(min_df=min_df, max_df=max_df, max_features=None, 
                                 strip_accents='unicode', analyzer='word', token_pattern=token_pattern,
                                 ngram_range=ngram_range,
                                 stop_words = stop_words, vocabulary=vocabulary)
    return bow
