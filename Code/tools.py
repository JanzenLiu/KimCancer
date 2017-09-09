import pandas as pd
import json

'''
Convert a json object to a pandas Series
Note:
	the keys of the json object are suggested to be index numbers,
	and the json itself is suggested to be of only one level nested.
'''
def jsonToSeries(json):
	series = pd.Series()
	for key, value in json.items():
		series.set_value(int(key), value)
	return series


'''
Convert a pandas Series to a json object
@param:
	series: pandas Series to convert
	index_type: data type of keys assigned to the json object, should be int or str
'''
def seriesToJson(series, index_type=int):
	assert index_type in [int, str]
	obj = dict()
	for index, value in series.iteritems():
		obj[index_type(index)] = value
	return obj


def save_words(words, path):
	with open(path, "w") as f:
		for word in words:
			f.write("%s\n" % word)