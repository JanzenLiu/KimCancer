import os
import sys; sys.path.append("../"); sys.path.append("../")
from reader import load_stratified_kfold
from param_config import config

### generate kfold
cmd = "python3 ./gen_kfold.py"
os.system(cmd)

from genFeat_counting_feat import extract_all
extract_all()