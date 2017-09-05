# [Kaggle Personalized Medicine Competition][a]

A text classification competition on Kaggle

### Instruction

To reproduce the results, as well as the intermediate product, you need to:

* Download the zipped data file from the [competition data page][b], unzip them and move the extracted data files into ./Data/ (which should be created by yourself) Folder.
* Run `cd Code/Preprocess/` and then `python3 run.py` to generate the preprocessed data.
* Run `cd ../Code/Feat/` and then `python3 run.py` to extract additional features (i.e. feature engineering) and save them.
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

- [ ] add feature counting occurences and unique occurences of specific patterns (listed in ./Code/Preprocess/pattern_dict.py).
- [ ] add directory and file examination in kFold generating function.
- [ ] extract TF-IDF and truncated TF-IDF features from text data.
- [ ] extract word2vec features from text data.
- [ ] extract physiological chemistry related features from variant data.

### Prerequisites

Running this project requires following python packages:
* numpy
* pandas
* sklearn

### Reference

[a]:https://www.kaggle.com/c/msk-redefining-cancer-treatment
[b]:https://www.kaggle.com/c/msk-redefining-cancer-treatment/data
