import pandas as pd
import pickle
import os
import sys; sys.path.append("../"); sys.path.append("../Utils/")
from param_config import config
from reader import load_extracted_text, load_original_variants

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

if __name__ == "__main__":
	cmd = "python3 replace_text.py"
	os.system(cmd)

	cmd = "python3 extract_pattern.py"
	os.system(cmd)
		
	dump_processed_data()
