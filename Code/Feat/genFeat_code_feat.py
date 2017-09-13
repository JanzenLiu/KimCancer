import pandas as pd

def extract_onehot_encoding_feat(df, feat_name):
	df = pd.concat([df, pd.get_dummies(df[feat_name])], axis=1)

