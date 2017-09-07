import numpy as np
import pandas as pd
import sys; sys.path.append("../")
from param_config import config

def rescale(pred, inplace=False):
	return pred / pred.sum(axis=1).reshape((-1,1))

'''
@param:
y_true: true label of shape (n_samples,) or (n_samples, 1)
y_pred: predicted probabilities for each class, which is of shape (n_samples, n_classes)
'''
def multiclass_logloss(y_true, y_pred):
	if isinstance(y_true, pd.DataFrame):
		y_true = y_true["Class"].values
	if isinstance(y_pred, pd.DataFrame):
		cols = ["class"+str(i+1) for i in range(config.n_classes)]
		y_pred = y_pred[cols].values

	assert y_true.shape[0] == y_pred.shape[0]
	assert y_pred.shape[1] == config.n_classes

	eps = np.exp(-15)
	prob_true = np.eye(config.n_classes)[y_true-1]
	prob_pred = np.vectorize(lambda x: max(min(x, 1-eps), eps))(rescale(y_pred))
	loss = -(prob_true*np.log(prob_pred)).sum(axis=1) # the loss vector can be returned if necessary
	return loss.mean()
