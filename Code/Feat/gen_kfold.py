import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import StratifiedKFold
import sys; sys.path.append("../"); sy.path.append("../Helper/")
from param_config import config
from reader import load_original_variants

'''
generate stratified kfold with specific parameters
@param:
    n_runs, n_folds: number of runs and folds
    label: column name indicating the target used for stratification
    df: dataframe to produce kfold
@return:
    skf[i][j] indicates the indices for training and validation subset in the (j+1) fold in the (i+1)th run
'''
def gen_kfold(n_runs=config.n_runs, n_folds=config.n_folds, label, df):
    skf = [0]*config.n_runs
    for run in range(n_runs):
        random_seed = 2017 + 1000 * (run+1)
        skf_helper = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=random_seed)
        skf[run] = list(skf_helper.split(df, df[label]))
        for fold, (trainInd, validInd) in enumerate(skf[run]):
            print("================================")
            print("Index for run: %s, fold: %s" % (run+1, fold+1))
            print("Train (num = %s)" % len(trainInd))
            print(trainInd[:10])
            print("Valid (num = %s)" % len(validInd))
            print(validInd[:10])
    return skf

if __name__ == "__main__":
    old_skf = load_stratified_kfold()
    if old_skf == "error" or len(old_skf) != config.n_runs or len(old_skf[0]) != config.n_folds:
        ## load data
        df_train_var, df_test_var = load_original_variants()

        ## generate kfold using 'Class' and 'Gene' as stratification target and save them
        for stratified_label,key in zip(["disease_class", "mutated_gene"], ["Class", "Gene"]):
            with open("%s/stratifiedKFold.%s.p" % (config.data_folder, stratified_label), "wb") as f:
                pickle.dump(gen_kfold(label=key, df=df_train_var), f)