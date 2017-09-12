import pandas as pd
import re

################################################################################
#####################
### To Preprocess ###
#####################
ERLIN2?FGFR1 Fusion 					# -> ERLIN2-FGFR1 Fusion, train#1389
FGFR3 - BAIAP2L1 Fusion 				# -> FGFR3-BAIAP2L1, train#1410
FGFR2?PPHLN1 Fusion 					# -> FGFR2-PPHLN1 Fusion, #train1470
FLT3 internal tandem duplications		# -> internal tandem duplication, train#1640


################################################################################
##########################
### AA-level Variation ###
##########################
### deletion ###
var_regex_1 = r"^[A-Z]\d+_[A-Z]\d+del$" # 65 rows filtered out
var_regex_2 = r"^[A-Z]\d+del$" # 32 rows filtered out
var_regex_3 = r"^\d+_\d+del$" # 4 rows filtered out
var_regex_4 = r"^[A-Z]\d+_[A-Z]\d+DEL$" # 1 rows filtered out

### insertion ###
var_regex_5 = r"^[A-Z]\d+ins[A-Z]+$" # 3 rows filtered out
var_regex_6 = r"^[A-Z]\d+_[A-Z]\d+ins[A-Z]+$" # 40 rows filtered out
var_regex_7 = r"^\d+_\d+ins[A-Z]+$" # 1 rows filtered out
var_regex_8 = r"^[A-Z]\d+_[A-Z]\d+ins$" # 1 rows filtered out

### deletion and insertion ###
var_regex_9 = r"^[A-Z]\d+_[A-Z]\d+delins[A-Z]+$" # 33 rows filtered out
var_regex_10 = r"^[A-Z]\d+delins[A-Z]+$" # 4 rows filtered out
var_regex_11 = r"^[A-Z]\d+[A-Z\*]$" # 8206 rows filtered out

### duplication ###
var_regex_12 = r"^[A-Z]\d+_[A-Z]\d+dup$" # 10 rows filtered out
var_regex_13 = r"^[A-Z]\d+dup$" # 5 rows filtered out

### truncation ###
var_regex_14 = r"^[A-Z]\d+_[A-Z]\d+trunc$" # 1 rows filtered out
var_regex_15 = r"^\d+_\d+trunc$" # 4 rows filtered out

### frame shift ###
var_regex_16 = r"^[A-Z]\d+fs" # 14 rows filtered out
var_regex_17 = r"^[A-Z]\d+[A-Z]fs\*\d+$" # 6 rows filtered out
var_regex_18 = r"^[A-Z]\d+[A-Z]fs\*$" # 2 rows filtered out

### splice ###
var_regex_19 = r"^[A-Z]\d+_splice$" # 9 rows filtered out
var_regex_20 = r"^\d+_\d+splice$" # 2 rows filtered out
var_regex_21 = r"^\d+_[A-Z]\d+splice$" # 1 rows filtered out

### Unknown ###
var_regex_22 = r"^null\d+[A-Z]$" # 19 rows filtered out


####################################
### Gene-Segment-level Variation ###
####################################
### Exon Variation ###
var_regex_23 = r"^Exon \d+ \w+$" # 10 rows filtered out
var_regex_24 = r"^Exon \d+ \w+/\w+$" # 2 rows filtered out
'''3221               TRKAIII Splice Variant'''	# two Exon splicing

### Promotor Variation ###
var_regex_25 = r"^Promoter Mutations$" # 1 rows filtered out
var_regex_26 = r"^Promoter Hypermethylation$" # 2 rows filtered out

### typical variation for that gene ###
var_regex_27 = r"^[A-Z0-9]+v[VIX]+$" # 4 rows filtered out
'''2054                             MYC-nick''' # a variant form
'''3109                              DNMT3B7''' # a truncated DNMT3B

### mutation on specific region ###
var_regex_28 = r"^DNA binding domain (\w+ )*\w+$" # 3 rows filtered out
'''351                           3' Deletion''' # deletion and unknown

### mutation on specific composition ###
'''4439       Single Nucleotide Polymorphism''' #
'''1640    FLT3 internal tandem duplications''' # duplication
'''211                              EGFR-KDD''' # Kinase Domain Duplication

### truncation ###
var_regex_29 = r"^Truncating Mutations$" # 113 rows filtered out
'''Truncating Mutations in the PEST Domain'''
'''Truncating Mutations Upstream of Transactivation Domain'''


############################
### Gene-level Variation ###
############################
### Fusion ###
var_regex_30 = r"^Fusions$" # 37 rows filtered out
var_regex_31 = r"^[A-Z0-9]-[A-Z0-9]+-\d+ Fusion$" # 2 rows filtered out
var_regex_32 = r"^[A-Z0-9]+-[A-Z0-9]+ Fusion$" # 153 rows filtered out
'''3223                   Delta-NTRK1 Fusion''' # unknown + Fusion

### Structural variant ###
var_regex_33 = r"^Deletion$" # 88 rows filtered out

### Functional variant ###
var_regex_34 = r"^Epigenetic Silencing$" # 1 rows filtered out
var_regex_35 = r"^Hypermethylation$" # 1 rows filtered out
var_regex_36 = r"^Amplification$" # 79 rows filtered out
var_regex_37 = r"^Overexpression$" # 6 rows filtered out
'''631                      Copy Number Loss''' # unknown

### Wild Type ###
'''3135                             Wildtype''' # a very special type of variant

### Typical Variant ###
'''96                              TGFBR1*6A''' # a common polymorphism of the type I transforming growth factor beta receptor
'''1786                             ARv567es'''
'''1801                                AR-V7'''
'''1938                               L232LI''' # typical variant
'''1941                               L225LI''' # typical variant
'''2718                              p61BRAF''' # typical variant
'''3254                               CASP8L''' # unknown

###############
### Unknown ###
###############
'''
354                                 R1627
355                                 C1385
'''
################################################################################


def filter_var(df, regex):
	inds = df[df["Variation"].map(lambda x: re.match(regex, x)!=None)].index
	df.drop(inds, inplace=True)
	print("%d rows filtered out" % inds.shape[0])