import pickle
import sys; sys.path.append("../")
from param_config import param_config

# from replace_text import replace_all
# replace_all()

# from extract_pattern import extract_all
# extract_all()

def dump_processed_data():
	df_train_txt, df_test_txt = load_extracted_text()
	df_train_var, df_test_var = load_original_variants()

	df_train = pd.merge(df_train_txt, df_train_var, how="left", on="ID").fillna("")
	df_test = pd.merge(df_test_txt, df_test_var, how="left", on="ID").fillna("")
	
	print("Dumping processed data...")
	with open(config.processed_train_data_path, "wb") as f:
		pickle.dump(df_train, f)
	with open(config.processed_test_data_path, "wb") as f:
		pickle.dump(df_test, f)

dump_processed_data()