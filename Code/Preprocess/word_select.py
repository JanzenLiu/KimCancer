#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import pickle
import json
import sys; sys.path.append('../')
from param_config import config
from reader import load_vocabulary
from tools import save_words

'''
Extract speical words and common words from a word list
@param:
    words: a list of words
    vocab: a vocabulary of words indicating common words
@return:
    a set of special words and a set of common words
'''
def extract_special_words(words, vocab):
    special_words = set()
    common_words = set()

    for w in words:
        if w.lower() not in vocab:
            if w[-1] != 's' or (w[:-1].lower() not in vocab and \
               w[:-2].lower() not in vocab):
                special_words.add(w)
                continue
        common_words.add(w)

    return special_words, common_words


def extract_special_words_from_docs(text_dict, vocab):
    special_words = dict()
    common_words = dict()
    step = 200
    counter = 0

    ## extract common and special words for each document
    for key, value in text_dict.items(): 
        if(counter % step == 0):
            print('processing #%d' % counter)
        words = set() # to store unique words of each document
        for sent in value:
            words |= set(sent)
        special, common = extract_special_words(words, vocab)
        special_words[key] = list(special)
        common_words[key] = list(common)
        counter += 1
    print('done.')
    return special_words, common_words

def get_unique_words(words_dict):
    unique_words = set()
    for words in words_dict.values():
        unique_words |= set(words)
    return unique_words


'''Outdated function to extract special and common words'''
def extract_special_words_old(text, vocab):
    # split text into sentences
    text = ' '.join(text.split('. '))
    text = ' '.join(text.split(', '))
    text = ' '.join(text.split('? '))
    text = ' '.join(text.split('; '))
    text = ' '.join(text.split(': '))

    # split sentences into words
    words = text.split()

    # remove empty splits
    words = [w for w in words if w != '']

    common_words = set()
    special_words = set()
    for w in words:
        # remove redundant parenthesis
        if re.match(r'^\(.*\)$', w):
            w = w[1:-1]
        elif re.match(r'^\([^)]*$', w):
            w = w[1:]
        elif re.match(r'^[^(]*\)$', w):
            w = w[:-1]
        if len(w) == 0:
            continue

        # remove all numerics
        if re.match(r'^-?(\d+,)*\d+(\.\d+)?$', w):
            continue

        alphanumerics = re.split(r'\W', w)
        alphanumerics = [s for s in alphanumerics if s != '']
        is_special = False
        for s in alphanumerics:
            if s.lower() not in vocab:
                if s[-1] != 's' or (s[:-1].lower() not in vocab and \
                   s[:-2].lower() not in vocab):
                    special_words.add(w)
                    is_special = True
                    break

        if not is_special:
            common_words |= set(alphanumerics)

    # with open(COMMON_WORDS_SAVEPATH, 'w') as common_file:
    #     for w in common_words:
    #         common_file.write(w + '\n')
    #
    # with open(SPECIAL_WORDS_SAVEPATH, 'w') as special_file:
    #     for w in special_words:
    #         special_file.write(w + '\n')

    return special_words, common_words


if __name__ == '__main__':
    vocabulary = load_vocabulary()
    unique_special_words = set()
    unique_common_words = set()

    #########################
    ##### Training Data #####
    #########################
    ## load tokens extracted from train text
    with open(config.train_tokens_path) as text_file:
        text_dict = json.load(text_file)
    print('complete loading processed training text')
    special_words, common_words = extract_special_words_from_docs(text_dict)

    ## save common and special words extracted
    with open(config.special_words_train_savepath, 'w') as output_file:
        json.dump(special_words, output_file, indent=2)
    with open(config.common_words_train_savepath, 'w') as output_file:
        json.dump(common_words, output_file, indent=2)
    print('complete extracting special words from training text')

    ## update unique special and common words
    unique_special_words.update(get_unique_words(special_words))
    unique_common_words.update(get_unique_words(common_words))

    ########################
    ##### Testing Data #####
    ########################
    ## load tokens extracted from test text
    with open('../../Data/test.tokens.json') as text_file:
        text_dict = json.load(text_file)
    print('complete loading processed testing text')
    special_words, common_words = extract_special_words_from_docs(text_dict)

    ## save common and speical words extracted
    with open(config.special_words_test_savepath, 'w') as output_file:
        json.dump(special_words, output_file, indent=2)
    with open(config.common_words_test_savepath, 'w') as output_file:
        json.dump(common_words, output_file, indent=2)
    print('complete extracting special words from testing text')

    ## update unique special and common words
    unique_special_words.update(get_unique_words(special_words))
    unique_common_words.update(get_unique_words(common_words))

    ###################
    ##### For All #####
    ###################
    save_words(unique_special_words, config.unique_special_words_path)
    save_words(unique_common_words, config.unique_common_words_path)
