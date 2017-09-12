import pandas as pd
import sys; sys.path.append("../Utils")
from reader import load_original_variants
from param_config import config

if __name__ == "__main__":
	'''
	Dirty Variants to Clean:

	ERLIN2?FGFR1 Fusion 					# -> ERLIN2-FGFR1 Fusion, train#1389
	FGFR3 - BAIAP2L1 Fusion 				# -> FGFR3-BAIAP2L1 Fusion, train#1410
	FGFR2?PPHLN1 Fusion 					# -> FGFR2-PPHLN1 Fusion, #train1470
	FLT3 internal tandem duplications		# -> internal tandem duplication, train#1640
	PAX8-PPAR? Fusion 						# -> PAX8-PPARγ Fusion, train#2910
	M1_E165DEL								# -> M1_E165del, train#961
	EGFR-KDD 								# -> Kinase Domain Duplication, train#211
	'''

	df_train_var, df_test_var = load_original_variants()

	print("Cleaning variation of original data...")
	df_train_var["Variation"].set_value(211, "Kinase Domain Duplication")
	df_train_var["Variation"].set_value(961, "M1_E165del")
	df_train_var["Variation"].set_value(1389, "ERLIN2-FGFR1 Fusion")
	df_train_var["Variation"].set_value(1410, "FGFR3-BAIAP2L1 Fusion")
	df_train_var["Variation"].set_value(1470, "FGFR2-PPHLN1 Fusion")
	df_train_var["Variation"].set_value(1640, "internal tandem duplication")
	df_train_var["Variation"].set_value(2910, "EPAX8-PPARγ Fusion")

	print("Saving processed variants data...")
	df_train_var.to_csv(config.processed_train_variant_path, index=False)
	df_test_var.to_csv(config.processed_test_variant_path, index=False)