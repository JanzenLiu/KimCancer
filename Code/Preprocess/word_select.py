#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import pickle
import json
import sys; sys.path.append('../')
from param_config import config
from reader import load_vocabulary
# load vocabulary


def extract_special_words(words, vocab):
    special_words = set()
    common_words = set()

    for w in words:
        if w.lower() not in vocab:
            if s[-1] != 's' or (s[:-1].lower() not in vocab and \
               s[:-2].lower() not in vocab):
                special_words.add(w)
                is_special = True
        if not is_special:
            common_words.add(w)

    return special_words, common_words

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
    special_words = dict()
    common_words = dict()

    with open('../../Data/train.tokens.json') as text_file:
        text_dict = json.load(text_file)
    print('complete loading processed training text')

    for index in text_dict:
        print('processing %s' % index)
        words = set()
        for sent in text_dict[index]:
            words |= set(sent)
        special, common = extract_special_words(words, vocabulary)
        special_words[index] = list(special)
        common_words[index] = list(common)

    with open(config.special_words_train_savepath, 'w') as output_file:
        json.dump(special_words, output_file, indent=2)
    with open(config.common_words_train_savepath, 'w') as output_file:
        json.dump(common_words, output_file, indent=2)
    print('complete extracting special words from training text')

    with open('../../Data/test.tokens.json') as text_file:
        text_dict = json.load(text_file)
    print('complete loading processed testing text')

    for index in text_dict:
        print('processing %s' % index)
        words = set()
        for sent in text_dict[index]:
            words |= set(sent)
        special, common = extract_special_words(words, vocabulary)
        special_words[index] = list(special)
        common_words[index] = list(common)

    with open(config.special_words_test_savepath, 'w') as output_file:
        json.dump(special_words, output_file, indent=2)
    with open(config.common_words_test_savepath, 'w') as output_file:
        json.dump(common_words, output_file, indent=2)
    print('complete extracting special words from testing text')
