import pickle
import sys; sys.path.append("../")
from param_config import config
from reader import load_stratified_kfold

skf = load_stratified_kfold()

def dump_feat(df_train, df_test, feat_name):
	print("Dumping feature %s..." % feat_name)
	## For cross-validation
	for run in range(config.n_runs):
		## use 80% for training and 20% for validation
		for fold, (trainInd, validInd) in enumberate(skf[run]):
			path = "%s/Run%d/Fold%d" % (config.feat_folder, run+1, fold+1)
			X_train = df_train[feat_name].values[trainInd]
			X_valid = df_train[feat_name].values[validInd]
			with open("%s/train.%s.feat.p" % (path, feat_name), "wb") as f:
				pickle.dump(X_train, f)
			with open("%s/valid.%s.feat.p" % (path, feat_name), "wb") as f:
				pickle.dump(X_valid, f)

	## For training and testing
	path = "%s/All" % config.feat_folder
	X_train = df_train[feat_name].values
	X_test = df_test[feat_name].values
	with open("%s/train.%s.feat.p" % (path, feat_name), "wb") as f:
		pickle.dump(X_train, f)
	with open("%s/test.%s.feat.p" % (path, feat_name), "wb") as f:
		pickle.dump(X_test, f)

def dump_feats(df_train, df_test, feat_names):
	print("For cross-validation...")
	for run in range(config.n_runs):
		## use 80% for training and 20% for validation
		for fold, (trainInd, validInd) in enumberate(skf[run]):
			print("Run: %d, Fold: %d" % (run+1, fold+1))
			path = "%s/Run%d/Fold%d" % (config.feat_folder, run+1, fold+1)

			for feat_name in feat_names:
				X_train = df_train[feat_name].values[trainInd]
				X_valid = df_train[feat_name].values[validInd]
				with open("%s/train.%s.feat.p" % (path, feat_name), "wb") as f:
					pickle.dump(X_train, f)
				with open("%s/valid.%s.feat.p" % (path, feat_name), "wb") as f:
					pickle.dump(X_valid, f)
	print("Done.")

	print("For training and testing...")
	path = "%s/All" % config.feat_folder
	for feat_name in feat_names:
		X_train = df_train[feat_name].values
		X_test = df_test[feat_name].values
		with open("%s/train.%s.feat.p" % (path, feat_name), "wb") as f:
			pickle.dump(X_train, f)
		with open("%s/test.%s.feat.p" % (path, feat_name), "wb") as f:
			pickle.dump(X_test, f)
	print("Done.")