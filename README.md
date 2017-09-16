# [Kaggle Personalized Medicine Competition][a]

A text classification competition on Kaggle

### Instruction

To reproduce the results, as well as the intermediate product, you need to:

* Download the zipped data file from the [competition data page][b], unzip them and move the extracted data files into ./Data/ (which should be created by yourself) Folder.
* Run `cd Code/Preprocess/` and then `python3 run.py` to generate the preprocessed data.
* Run `cd ../Feat/` and then `python3 run.py` to extract additional features (i.e. feature engineering) and save them.
* To be added...

### Text Preprocessing

* We remove content matched with the patterns specified in `./Code/Preprocess/pattern_dict.py` from the original text data (the content removed are saved under `./Pattern/dev/`).
* We replace some unicode characters with the alternative word(s) specified in `./Code/Preprocess/unicode_dict.py`.
* To be added...

### Feature Engineering

* We add features counting the occurences of specific unicode characters (listed in `./Code/Preprocess/unicode_dict.py`).
* To be added...

### Single Model Training

* To be added...

### Model Emsembling

* To be added...

### TODO

- [x] refactor codes: split Preprocess part to EDA(Explorative Data Analysis).
- [x] refactor codes: split loading file, dumping file, converting data parts to different modules.
- [ ] add code spec.
- [x] extract special characters.
- [x] extract common and speical words(tokens):
	- [x] on original text data.
	- [ ] on processed text data.
- [ ] get common and special words counter for each document:
	- [ ] on original text data.
	- [ ] on processed text data.
- [x] get unique common and special words.
- [ ] extract special biological/chemical/medical terms from the text.
- [ ] build word map:
	- [x] build 1-to-1 map.
	- [ ] build m-to-n map.
	- [ ] build map with counter (to determine the reliability of the map).
- [ ] observe others patterns and replenish pattern dictionary.
- [ ] crawl external data
	- [ ] function of Gene/AA
	- [ ] effects of same mutations found in the past
- [ ] accelerate gensim Word2Vec using cython.
- [ ] add feature counting occurences and unique occurences of specific patterns (listed in ./Code/Preprocess/pattern_dict.py).	
- [x] add directory and file examination in kFold generating function.
- [x] one-hot encode Gene.
- [ ] extract physiological chemistry related features from variant data (i.e. encode Variation).
- [ ] add standard/non-standard label to variation.
- [ ] extract basic NLP-related counting features (e.g. digit count, word count , sentence count...).
- [ ] extract TF-IDF(transformed) and truncated BOW features:
	- [ ] on original text data.
	- [ ] on processed text data.
- [ ] extract TF-IDF and truncated TF-IDF features:
	- [ ] on original text data.
	- [ ] on processed text data.
- [ ] extract TF-IDF distance statistics features:
	- [ ] on original text data.
	- [ ] on processed text data.
- [ ] extract word2vec features:
	- [ ] on original text data.
	- [ ] on processed text data.
- [ ] perform k-Mean clustering on word vectors obtained above.
	- [ ] on original text data.
	- [ ] on processed text data.
- [ ] extract word counting features for each cluster of words obtained above 
	- [ ] on original text data.
	- [ ] on processed text data.
- [ ] extract word2vec distance statistics features on processed test data.
- [ ] extract intersection features between vectorized text features, Gene-related features, and Variation related features.
- [ ] model to use: LogisticRegression (Ridge, Lasso, plain LR)
- [ ] model to use: Random Forest
- [ ] model to use: SVC (with different kernels)
- [ ] model to use: LDA
- [ ] model to use: LSTM
- [ ] model to use: KNN
- [ ] XGBoost (with all kinds of available voters specified above)

### Prerequisites

Running this project requires following python packages:
* numpy
* pandas
* sklearn
* scipy
* nltk (module should be downloaded before running)
* gensim
* cython (setup for word2vec acceleration should be done)

### Reference
1. [DNA Recommendations][1]
2. [Recommendations for the description of protein sequence variants][2]
3. [Standards Nucleotides (DNA / RNA)][3]

[a]:https://www.kaggle.com/c/msk-redefining-cancer-treatment
[b]:https://www.kaggle.com/c/msk-redefining-cancer-treatment/data
[1]:http://varnomen.hgvs.org/recommendations/DNA/
[2]:http://www.hgvs.org/mutnomen/recs-prot.html
[3]:http://varnomen.hgvs.org/bg-material/standards/
