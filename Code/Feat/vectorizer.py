import re
import sys; sys.path.append('../')
import nltk
import gensim
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from param_config import config

##################
### stop words ###
##################
english_stopwords = nltk.corpus.stopwords.words("english")
english_stopwords += ["(", ")", "[", "]", "{", "}"]
english_stopwords += [",", "."]
english_stopwords = set(stopwords)


################
### stemming ###
################
if config.stemmer_type == "porter":
	english_stemmer = nltk.stem.PorterStemmer()
elif config.stemmer_type == "snowball":
	english_stemmer = nltk.stem.SnowballStemmer("english")


##############
### TF-IDF ###
##############
class StemmedTfidfVectorizer(TfidfVectorizer):
	def build_analyzer(self):
		analyzer = super(TfidfVectorizer, self).build_analyzer()
		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

token_pattern = r"(?u)\b\w\w+\b"
tfidf_norm = "l2"
tfidf_max_df = 0.75
tfidf_min_df = 3
tfidf_stopwords = english_stopwords
def getTFV(token_pattern = token_pattern,
			norm = tfidf_norm,
			max_df = tfidf_max_df,
			min_df = tfidf_min_df,
			ngram_range = (1,1),
			vocabulary = None,
			stop_words = tfidf_stopwords):
	tfv = StemmedTfidfVectorizer(min_df=min_df, max_df=max_df, max_features=None,
								strip_accents='unicode', analyzer='word', token_pattern=token_pattern,
								ngram_range=ngram_range, use_idf=True, smooth_idf=True, sublinear_tf=True,
								stop_words=_stopwords, norm=norm, vocabulary=vocabulary)
	return tfv


###########
### BOW ###
###########
class StemmedCountVectorizer(CountVectorizer):
	def build_analyzer(self):
		analyzer = super(CountVectorizer, self).build_analyzer()
		return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

token_pattern = r"(?u)\b\w\w+\b"
bow_max_df = 0.75
bow_min_df = 3
bow_stopwords = english_stopwords
def getBOW(token_pattern = token_pattern,
			max_df = bow_max_df,
			min_df = bow_min_df,
			ngram_range = (1,1),
			vocabulary = None,
			stop_words = bow_stopwords):
	bow = StemmedCountVectorizer(min_df=min_df, max_df=max_df, max_features=None,
								strip_accents='unicode', analyzer='word', token_pattern=token_pattern,
								ngram_range=ngram_range,
								stop_words=_stopwords, vocabulary=vocabulary)
	return bow


################
### Word2Vec ###
################
class StemmedW2VTokenizer(object):
	def __init__(self, *arrays):
		self.arrays = arrays

	def __iter__(self):
		for array in arrays:
			for document in array:
				for sentence in nltk.sent_tokenize(document):
					yield [english_stemmer.stem(word.lower()) for word in nltk.word_tokenize(sentence) if word not in english_stopwords]

w2v_size = 200
w2v_window = 5
w2v_min_count = 5
w2v_seed = 2017
w2v_workers = 8
'''
Use closure to avoid training the w2v model at unexpected time, which will cost a lot of time 
	e.g. while importing this module
Example of usage:
	vec = getW2V(*params) 			# training won't happen at this time
	model = vec.fit(some_sentences)	# where the training happens, then you will get the model trained
'''
def getW2V(size = w2v_size,
			window = w2v_window,
			min_count = w2v_min_count,
			seed = w2v_seed,
			workers = w2v_workers):
	class ModelWrapper(object):
		def __init__(self):
			self.params = {
				"size": size,
				"window": window,
				"min_count": min_count,
				"seed": seed,
				"workers": workers
			}
			self.model = None

		def fit(self, sentences):
			print("Training word2vec model...")
			self.model = gensim.models.Word2Vec(sentences, size=self.params["size"], window=self.params["window"],
										min_count=self.params["min_count"], seed=self.params["seed"], workers=self.params["workers"])
			print("Model training done.")
			return self.model

	return ModelWrapper()