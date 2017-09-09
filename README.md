# [Kaggle Personalized Medicine Competition][a]

A text classification competition on Kaggle

### Instruction

To reproduce the results, as well as the intermediate product, you need to:

* Download the zipped data file from the [competition data page][b], unzip them and move the extracted data files into ./Data/ (which should be created by yourself) Folder.
* Run `cd Code/Preprocess/` and then `python3 run.py` to generate the preprocessed data.
* Run `cd ../Feat/` and then `python3 run.py` to extract additional features (i.e. feature engineering) and save them.
* To be added...

### Text Preprocessing

* We remove content matched with the patterns specified in ./Code/Preprocess/pattern_dict.py from the original text data (the content removed are saved under ./Pattern/dev/).
* We replace some unicode characters with the alternative word(s) specified in ./Code/Preprocess/unicode_dict.py.
* To be added...

### Feature Engineering

* We add features counting the occurences of specific unicode characters (listed in ./Code/Preprocess/unicode_dict.py).
* To be added...

### Single Model Training

* To be added...

### Model Emsembling

* To be added...

### TODO

- [ ] refactor codes: split Preprocess part to EDA(Explorative Data Analysis).
- [ ] accelerate gensim Word2Vec using cython.
- [ ] add feature counting occurences and unique occurences of specific patterns (listed in ./Code/Preprocess/pattern_dict.py).
- [x] add directory and file examination in kFold generating function.
- [ ] one-hot encode Gene.
- [ ] extract physiological chemistry related features from variant data (i.e. encode Variation).
- [ ] extract basic text-concerning counting features (e.g. digit count, word count , sentence count...)
- [ ] extract TF-IDF and truncated TF-IDF features from text data.
- [ ] extract TF-IDF distance statistics features.
- [ ] extract word2vec features from text data.
- [ ] extract word2vec distance statistics features.
- [ ] extract intersection features between vectorized text features, Gene-related features, and Variation related features.
- [ ] model to use: LogisticRegression (with different penalty terms, e.g. l1, l2)
- [ ] model to use: Random Forest
- [ ] model to use: SVC (with different kernels)
- [ ] model to use: LDA

### Prerequisites

Running this project requires following python packages:
* numpy
* pandas
* sklearn
* nltk (modu should be downloaded)
* gensim
* cython (setup for word2vec acceleration should be done)

### Reference

[a]:https://www.kaggle.com/c/msk-redefining-cancer-treatment
[b]:https://www.kaggle.com/c/msk-redefining-cancer-treatment/data
