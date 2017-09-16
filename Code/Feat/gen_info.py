import os
import sys; sys.path.append("../"); sys.path.append("Utils")
import pickle
import numpy as np
import pandas as pd
from param_config import config
from reader import load_original_variants

'''
@ param:
feat_path_name: name for the feature combination, e.g. "svd100_and_wmd_Sep23"
'''
def gen_info(feat_path_name):
    ###############
    ## Load Data ##
    ###############
    ## load data
    df_train_var, df_test_var = load_original_variants()
    ## insert fake label for test
    df_test_var["Class"] = np.ones((df_test_var.shape[0]))
    df_test_var["relevance_variance"] = np.zeros((df_test_var.shape[0]))

    ## load pre-defined stratified k-fold index
    with open("%s/stratifiedKFold.%s.p" % (config.data_folder, config.stratified_label), "rb") as f:
        skf = pickle.load(f)
        
    ##########################
    ## Generate Information ##
    ##########################
    print("Generating info...")
    print("For cross-validation...")
    for run in range(config.n_runs):
        ## use 80% for training and 20% for validation
        for fold, (trainInd, validInd) in enumerate(skf[run]):
            print("Run: %d, Fold: %d" % (run+1, fold+1))
            path = "%s/%s/Run%d/Fold%d" % (config.feat_folder, feat_path_name, run+1, fold+1)
            if not os.path.exists(path):
                os.makedirs(path)

            ## get and dump weights
            # to be extended (if necessary and time permitted)
            weight = np.ones(df_train_var.shape[0])
            np.savetxt("%s/train.feat.weight" % path, weight[trainInd], fmt="%.6f")
            np.savetxt("%s/valid.feat.weight" % path, weight[validInd], fmt="%.6f")

            ## get and dump group info
            np.savetxt("%s/train.feat.group" % path, [len(trainInd)], fmt="%d")
            np.savetxt("%s/valid.feat.group" % path, [len(validInd)], fmt="%d")
                
            ## dump labels
            df_train_var.iloc[trainInd]['Class'].to_csv("%s/train.label" % path, index=False, header=True)
            df_train_var.iloc[validInd]['Class'].to_csv("%s/valid.label" % path, index=False, header=True)
    print("Done.")

    print("For training and testing...")
    path = "%s/%s/All" % (config.feat_folder, feat_path_name)
    if not os.path.exists(path):
        os.makedirs(path)
    ## weight
    weight = np.ones(df_train_var.shape[0])
    np.savetxt("%s/train.feat.weight" % path, weight, fmt="%.6f")
    
    ## group
    np.savetxt("%s/train.feat.group" % path, [df_train_var.shape[0]], fmt="%d")
    np.savetxt("%s/test.feat.group" % path, [df_test_var.shape[0]], fmt="%d")
    
    ## labels
    df_train_var['Class'].to_csv("%s/train.label" % path, index=False, header=True)
    
    print("All Done.")