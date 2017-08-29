#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

word_pattern = r"\b[A-Za-z]+\b"
unicode_pattern = r"\\u[0-9a-fA-F]{4}" # to be verified

patterns = {
	## parenthesis
	"figure_parenthesis": r"\([Ff]ig(?:ure)?\.? ?(?:\w+, )*(?:\w+ and )?\w+\)", # (fig 1), (fig. 1), (Fig. 1), (Figure 1), (Figure. 1), (Figure. 1A)
	"table_parenthesis": r"\([Tt]ables? (?:\w+, )*(?:\w+ and )?\w+\)", # (Table 1), (Table S2)
	"order_number_parenthesis": r"(?<= )\((?:\d+, )*(?:\d+ and )?\d{1,3}\)", # (1), (1, 2), (2, 5, 10)
	"order_number_range_parenthesis": r"\(\d+\-\d+\)", # (2-5), (10-200)
	"order_alpha_parenthesis": r"\((?:[A-HJ-Za-hj-z], )*[A-HJ-Za-hj-z]\)", # (A), (B), (a)
	"order_roman_parenthesis": r"\((?:[ivxIVX]+, )*[ivxIVX]+\)", # (i), (iv), (XII), (i, ii)
	"cite_year_parenthesis": r"\(\d{4}\)", # (1999), (2002)
	"cite_name_year_parenthesis": r"\([^)]+, \d{4}[a-z]?\)", # (Youngs et al., 2011), (Slade et al., 2011; Doros et al., 2012)
	"url_http_parenthesis": r"\(https?.+?\)", # (http://www.hgmd.cf.ac.uk/ac/index.php)
	"patient_parenthesis": r"\(patients? (?:\d and )?\d\)", # (patients 3), (patients 4 and 5)
	"version_parenthesis": r"\([Vv]ersion (?:\d+\.)*\d+\)", # (version 1.0.2)
	"equation_parenthesis": r"\([Eq]uation\.? ?\d+\)", # (Equation 9)
	"box_parenthesis": r"\([Bb]ox (?:\d+, )*(?:\d+ and )?\d+\)", # (Box 1)
	"see_parenthesis": r"\([Ss]ee (?:\w+, )*(?:\w+ and )?\w+\)", # (see text), (see Materials and Methods)
	## square brackets
	"figure_square_brackets": r"\[[Ff]ig(?:ure)?\.? \w+\]", # [fig 1], [fig. 1], [Fig. 1], [Figure 1], [Figure. 1], [Figure. 1A]
	"table_square_brackets": r"\[[Tt]able \w+\]", # [Table 1], [Table S2]
	"cite_index_square_brackets": r"\[(?:\d+, )*\d{1,3}\]", # [1], [1, 2], [2, 5, 10]
	"cite_index_range_square_brackets": r"\[\d+\-\d+\]", # [2-5], [10-200]
	"cite_year_brackets": r"\[\d{4}\]", # [1999], [2002]
	"cite_name_year_square_brackets": r"\[[^\]]+, \d{4}\]", # [Arkenbout et al., 2002], [Fernandez et al., 2000; Murphy et al., 2001]
	"url_http_square_brackets": r"\[https?.+?\]", # [http://projects.tcag.ca/variation/]
	## curly brackets
	# to be added...
	## others
	"variation": r"(?<=\W)[A-Z]\d{2,3}[A-Z*](?=\W)", # E452K, P90K, R358*
	"ph_value": r"[Pp][Hh] \d+(?:\.\d{1,2})?", # ph 8, pH 8, PH 8, pH 8.0, pH 8.23, pH 10
	"gene_seq": r"5[′']?\-[^′'a-z]*[AGCTU]+[^′'a-z]*\-3[′']?", # 5′-CCGGGATGACCGGAGCACCTG-3′, 5′-M13-GGCCGATTCGACCTCTCT-3′
	"url_http_plain": r"(?<![\(\[]])https?.+?(?=[ ,;\)])" # http://pymol.org, http://www.olympusfluoview.com/java/colocalization/index.html
}

other_patterns = {
	"other_parenthesis_pattern": r"\([^)]+\)", # (...)
	"other_brackets_pattern": r"\[[^\]]+\]", # [...]
	"other_curly_brackets_pattern": r"\{[^}]+\}" # {...}
}
