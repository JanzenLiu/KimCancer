import numpy as np
import pandas as pd
import sys
sys.path.append("../")
from param_config import config

df_train_txt = pd.read_csv(config.original_train_text_path, sep="\|\|", header=None, skiprows=1, names=["ID", "Text"])
df_train_var = pd.read_csv(config.original_train_variant_path)
df_test_txt = pd.read_csv(config.original_test_text_path, sep="\|\|", header=None, skiprows=1, names=["ID", "Text"])
df_test_var = pd.read_csv(config.original_test_variant_path)