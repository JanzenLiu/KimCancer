import re

patterns = {
	## parenthesis
	"figure_parenthesis": r"\([Ff]ig(ure)?\.? \w+\)", # (fig 1), (fig. 1), (Fig. 1), (Figure 1), (Figure. 1), (Figure. 1A)
	"table_parenthesis": r"\([Tt]able \w+\)", # (Table 1), (Table S2)
	"order_number_parenthesis": r"(?<= )\((\d+, )*\d+\)", # (1), (1, 2), (2, 5, 10)
	"order_number_range_parenthesis": r"(?<= )\(\d+\-\d+\)", # (2-5), (10-200)
	"order_alpha_parenthesis": r"(?<= )\([A-Za-z]\)", # (A), (B), (a)
	"cite_name_year_parenthesis": r"\([^)]+, \d{4}\)", # (Youngs et al., 2011), (Slade et al., 2011; Doros et al., 2012)
	"http(s)_parenthesis": r"\(https?.+?\)", # (http://www.hgmd.cf.ac.uk/ac/index.php)
	"other_parenthesis": r"\([^)]+\)", # (...)
	## square brackets
	"figure_square_brackets": r"\[[Ff]ig(ure)?\.? \w+\]", # [fig 1], [fig. 1], [Fig. 1], [Figure 1], [Figure. 1], [Figure. 1A]
	"table_square_brackets": r"\[[Tt]able \w+\]", # [Table 1], [Table S2]
	"cite_index_square_brackets": r"\[(\d+, )*\d+\]", # [1], [1, 2], [2, 5, 10]
	"cite_index_range_square_brackets": r"\[\d+\-\d+\]", # [2-5], [10-200]
	"cite_name_year_square_brackets": r"\[[^\]]+, \d{4}\]", # [Arkenbout et al., 2002], [Fernandez et al., 2000; Murphy et al., 2001]
	"http(s)_square_brackets": r"\[https?.+?\]", # [http://projects.tcag.ca/variation/]
	"other_square_brackets": r"\[[^\]]+\]", # [...]
	## curly brackets
	"other_curly_brackets": r"\{[^}]+\}", # {...}
	## others
	"variation": r"(?<=\W)[A-Z]\d{2,3}[A-Z*](?=\W)", # E452K, P90K, R358*
	"ph_value": r"[Pp][Hh] \d+(\.\d{1,2})?", # ph 8, pH 8, PH 8, pH 8.0, pH 8.23, pH 10
	"gene_seq": r"5(.?)\-[^′'a-z]*[AGCTU]+[^′'a-z]*\-3\1", # 5′-CCGGGATGACCGGAGCACCTG-3′, 5′-M13-GGCCGATTCGACCTCTCT-3′
	"http(s)_all": r"https?.+?(?=[ ,)\]])", # http://pymol.org, http://www.olympusfluoview.com/java/colocalization/index.html
}