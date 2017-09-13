import pandas as pd
import re

def get_pattern_pos_in_text(text, regex, ignore_case=True):
	if not ignore_case:
		flag = re.U
	else:
		flag = re.U|re.I
	pos = [match.span() for match in re.finditer(regex, text, flag)]
	return pos

