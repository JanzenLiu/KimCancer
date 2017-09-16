import os
import sys
import pickle
import numpy as np
import pandas as pd
from scipy.sparse import hstack, vstack, csr_matrix
from sklearn.base import BaseEstimator
from sklearn.datasets import dump_svmlight_file
sys.path.append("../")
from param_config import config


#### adopted from @Ben Hamner's Python Benchmark code
## https://www.kaggle.com/benhamner/crowdflower-search-relevance/python-benchmark
def identity(x):
    return x

class SimpleTransform(BaseEstimator):
    def __init__(self, transformer=identity):
        self.transformer = transformer

    def fit(self, X, y=None):
        return self

    def fit_transform(self, X, y=None):
        return self.transform(X)

    def transform(self, X, y=None):
        return self.transformer(X)

def load_feat_as_csr(path):
    with open(path, "rb") as f:
        X = pickle.load(f)
    if len(X.shape) == 1:
        X.shape = (-1, 1)
    return csr_matrix(X)

def align_feat_dim(X1, X2):
    dim_diff = abs(X1.shape[1] - X2.shape[1])
    if X2.shape[1] < X1.shape[1]:
        X2 = hstack([X2, csr_matrix((X2.shape[0], dim_diff))])
    elif X2.shape[1] > X1.shape[1]:
        X1 = hstack([X1, csr_matrix((X1.shape[0], dim_diff))])
    return X1, X2

#### function to combine features
def combine_feat(feat_names, feat_path_name):
    
    print("==================================================")
    print("Combining feature group %s (%d in total)..." % (feat_path_name, len(feat_names)))

    ######################
    ## Cross-validation ##
    ######################
    print("For cross-validation...")
    ## for each run and fold
    for run in range(1,config.n_runs+1):
        for fold in range(1,config.n_folds+1):
            print("Run: %d, Fold: %d" % (run, fold))
            read_path = "%s/Run%d/Fold%d" % (config.feat_folder, run, fold)
            save_path = "%s/%s/Run%d/Fold%d" % (config.feat_folder, feat_path_name, run, fold)
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            for i,(feat_name,transformer) in enumerate(feat_names):
                print("Combining feat #%d: %s...".% (i+1, feat_name))

                ## load train and valid feat
                feat_train_file = "%s/train.%s.feat.p" % (read_path, feat_name)
                feat_valid_file = "%s/valid.%s.feat.p" % (read_path, feat_name)
                X_train = load_feat_as_csr(feat_train_file)
                X_valid = load_feat_as_csr(feat_valid_file)

                ## align feat dim
                X_train, X_valid = align_feat_dim(X_train, X_valid)

                ## apply transformation
                X_train = transformer.fit_transform(X_train)
                X_valid = transformer.transform(X_valid)

                ## stack feat
                if i == 0:
                    new_X_train, new_X_valid = X_train, X_valid
                else:
                    new_X_train, new_X_valid = hstack([new_X_train, X_train]), hstack([new_X_valid, X_valid])
                
            print("Feat dim: {}D".format(new_X_train.shape[1]))

            ## load label
            ## change to zero-based for multi-classification in xgboost
            Y_train = pd.read_csv("%s/train.label" % (save_path))['Class'] - 1            
            Y_valid = pd.read_csv("%s/valid.label" % (save_path))['Class'] - 1

            ## dump feats
            dump_svmlight_file(new_X_train, Y_train, "%s/train.feat" % (save_path))
            dump_svmlight_file(new_X_valid, Y_valid, "%s/valid.feat" % (save_path))
    
    ##########################
    ## Training and Testing ##
    ##########################
    print("For training and testing...")
    read_path = "%s/All" % (config.feat_folder)
    save_path = "%s/%s/All" % (config.feat_folder, feat_path_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    for i,(feat_name,transformer) in enumerate(feat_names):
        print("Combining feat #%d: %s...".% (i+1, feat_name))

        ## load train and test feat
        feat_train_file = "%s/train.%s.feat.p" % (read_path, feat_name)
        feat_test_file = "%s/test.%s.feat.p" % (read_path, feat_name)
        X_train = load_feat_as_csr(feat_train_file)
        X_test = load_feat_as_csr(feat_test_file)

        ## align feat dim
        X_train, X_test = align_feat_dim(X_train, X_test)

        ## apply transformation
        X_train = transformer.fit_transform(X_train)
        X_test = transformer.transform(X_test)

        ## stack feat
        if i == 0:
            new_X_train, new_X_test = X_train, X_test
        else:
            new_X_train, new_X_test = np.hstack([new_X_train, X_train]), np.hstack([new_X_test, X_test])

    print("Feat dim: {}D".format(new_X_train.shape[1]))
    
    ## load label
    Y_train = pd.read_csv("%s/train.label" % (save_path))['Class'] - 1            
    Y_test = pd.read_csv("%s/test.label" % (save_path))['Class'] - 1

    ## dump feat
    dump_svmlight_file(new_X_train, Y_train, "%s/train.feat" % (save_path))
    dump_svmlight_file(new_X_test, Y_test, "%s/test.feat" % (save_path))