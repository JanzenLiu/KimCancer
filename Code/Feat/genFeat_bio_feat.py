import pandas as pd
import re

'''
@TODO
to determine how many kind of general mutations(e.g. deletion, splice) are there to one hot, 
which should make sense to combine with other one-hot feature, like AA_mutation, function_segment_mutation
'''

##########################
### AA-level Variation ###
##########################
### deletion ###
# start_AA, start_AA_known(bool) start_pos, 
# end_AA, end_AA_known(bool), end_pos, 
# AA_mutation(bool), AA_mutation_type(one-hot), AA_deletion_length
var_regex_1 = r"^[A-Z]\d+_[A-Z]\d+del$" # 65 rows filtered out
var_regex_2 = r"^[A-Z]\d+del$" # 32 rows filtered out
var_regex_3 = r"^\d+_\d+del$" # 4 rows filtered out
var_regex_4 = r"^[A-Z]\d+_[A-Z]\d+DEL$" # 1 rows filtered out

### insertion ###
# ..., AA_insertion_length, AA_insertion_sequence(1st, 2nd...), AA_insertion_known(bool)
var_regex_5 = r"^[A-Z]\d+ins[A-Z]+$" # 3 rows filtered out
var_regex_6 = r"^[A-Z]\d+_[A-Z]\d+ins[A-Z]+$" # 40 rows filtered out
var_regex_7 = r"^\d+_\d+ins[A-Z]+$" # 1 rows filtered out
var_regex_8 = r"^[A-Z]\d+_[A-Z]\d+ins$" # 1 rows filtered out

### deletion and insertion ###
# ..., gross_AA_increase_length, single_mutation(bool)
# origina_AA, new_AA, new_AA_terminator(bool, * stands for terminator) 
var_regex_9 = r"^[A-Z]\d+_[A-Z]\d+delins[A-Z]+$" # 33 rows filtered out
var_regex_10 = r"^[A-Z]\d+delins[A-Z]+$" # 4 rows filtered out
var_regex_11 = r"^[A-Z]\d+[A-Z\*]$" # 8206 rows filtered out

### duplication ###
# ..., duplication_length
var_regex_12 = r"^[A-Z]\d+_[A-Z]\d+dup$" # 10 rows filtered out
var_regex_13 = r"^[A-Z]\d+dup$" # 5 rows filtered out

### truncation ###
# ..., truncation length
var_regex_14 = r"^[A-Z]\d+_[A-Z]\d+trunc$" # 1 rows filtered out
var_regex_15 = r"^\d+_\d+trunc$" # 4 rows filtered out

### frame shift ###
# ..., original_AA_before_shift, new_AA_after_shift, shift_length(the last number indicates length)
var_regex_16 = r"^[A-Z]\d+fs" # 14 rows filtered out
var_regex_17 = r"^[A-Z]\d+[A-Z]fs\*\d+$" # 6 rows filtered out
var_regex_18 = r"^[A-Z]\d+[A-Z]fs\*$" # 2 rows filtered out

### splice ###
var_regex_19 = r"^[A-Z]\d+_splice$" # 9 rows filtered out
var_regex_20 = r"^\d+_\d+splice$" # 2 rows filtered out
var_regex_21 = r"^\d+_[A-Z]\d+splice$" # 1 rows filtered out


####################################
### Gene-Segment-level Variation ###
####################################
### Exon Variation ###
# ..., gene_segment_variation(bool), Exon variation(bool), splicing(bool, could be combined with other)
# functional_structure_variation(bool, maybe onehot?)
# Exon number, mutation(e.g. deletion, insertion, to be onehot-encoded)
var_regex_22 = r"^Exon \d+ \w+$" # 10 rows filtered out
var_regex_23 = r"^Exon \d+ \w+/\w+$" # 2 rows filtered out
'''3221               TRKAIII Splice Variant'''	# two Exon splicing

### Promotor Variation ###
# ..., promotor_variation(bool), mutation(i.e., hypermethylation, one hot)
var_regex_24 = r"^Promoter Mutations$" # 1 rows filtered out
var_regex_25 = r"^Promoter Hypermethylation$" # 2 rows filtered out

### typical variation for that gene ###
# ..., variation_version(split gene name out, one hot)
var_regex_26 = r"^[A-Z0-9]+v[VIX]+$" # 4 rows filtered out
'''2054                             MYC-nick''' # a variant form
'''3109                              DNMT3B7''' # a truncated DNMT3B

### mutation on specific region ###
# ..., dna_binding_domain_variation(bool, maybe one hot 'funcional_structure'?)
# mutation(i.e. deletion)
var_regex_27 = r"^DNA binding domain (\w+ )*\w+$" # 3 rows filtered out
'''351                           3' Deletion''' # deletion and unknown

### mutation on specific composition ###
# ... polymorphism(bool), variated_composition(e.g. nucleotide, tandem, kinase_domain..., then one hot),
# num_composition_affected..., num_known(bool), typical_for_gene(bool)
'''4439       					   Single Nucleotide Polymorphism''' # polymorphism
'''1640    						FLT3 internal tandem duplications''' # duplication
'''211   EGFR-KDD(original), Kinase Domain Duplication(processed)'''

### truncation ###
# ... truncation(bool), truncated_domain(one-hot)
var_regex_28 = r"^Truncating Mutations$" # 113 rows filtered out
'''Truncating Mutations in the PEST Domain'''
'''Truncating Mutations Upstream of Transactivation Domain'''


############################
### Gene-level Variation ###
############################
### Fusion ###
# origin_gene, other_gene, funsion(one-hot)
var_regex_29 = r"^Fusions$" # 37 rows filtered out
var_regex_30 = r"^[A-Z0-9]-[A-Z0-9]+-\d+ Fusion$" # 2 rows filtered out
var_regex_31 = r"^[A-Z0-9]+-[A-Z0-9]+ Fusion$" # 153 rows filtered out
'''3223                   Delta-NTRK1 Fusion''' # unknown + Fusion

### Structural variant ###
# deletion(bool), structural_variant(bool)
var_regex_32 = r"^Deletion$" # 88 rows filtered out

### Functional variant ###
# functional variant(bool), variant(one hot)
var_regex_33 = r"^Epigenetic Silencing$" # 1 rows filtered out
var_regex_34 = r"^Hypermethylation$" # 1 rows filtered out
var_regex_35 = r"^Amplification$" # 79 rows filtered out
var_regex_36 = r"^Overexpression$" # 6 rows filtered out
'''631                      Copy Number Loss''' # unknown

### Wild Type ###
# wildtype variant(bool)
'''3135                             Wildtype''' # a very special type of variant

### Typical Variant ###
# to encode manually
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
# null(bool), unknown(bool), null_no, null_letter
var_regex_37 = r"^null\d+[A-Z]$" # 19 rows filtered out
'''
354                                 R1627
355                                 C1385
'''
################################################################################


def filter_var(df, regex):
	inds = df[df["Variation"].map(lambda x: re.match(regex, x)!=None)].index
	df.drop(inds, inplace=True)
	print("%d rows filtered out" % inds.shape[0])