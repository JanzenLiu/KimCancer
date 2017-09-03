import pandas as pd
import numpy as np
import pickle
import sys; sys.path.append("../")
from param_config import config
from reader import load_original_variants
from sklearn.model_selection import StratifiedKFold

## load data
df_train_var, df_test_var = load_original_variants()

skf = [0]*config.n_runs
for stratified_label,key in zip(["disease_class", "mutated_gene"], ["Class", "Gene"]):
    for run in range(config.n_runs):
        random_seed = 2017 + 1000 * (run+1)
        skf_helper = StratifiedKFold(n_splits=config.n_folds, shuffle=True, random_state=random_seed)
        skf[run] = list(skf_helper.split(df_train_var.drop([key], axis=1), df_train_var[key]))
        for fold, (trainInd, validInd) in enumerate(skf[run]):
            print("================================")
            print("Index for run: %s, fold: %s" % (run+1, fold+1))
            print("Train (num = %s)" % len(trainInd))
            print(trainInd[:10])
            print("Valid (num = %s)" % len(validInd))
            print(validInd[:10])
    with open("%s/stratifiedKFold.%s.p" % (config.data_folder, stratified_label), "wb") as f:
        pickle.dump(skf, f)