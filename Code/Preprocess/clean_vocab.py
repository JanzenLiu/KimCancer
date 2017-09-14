import re

'^[\d\.\-+=\:,\/]*$'
"^5['′]-[UACTG]+-3['′]?+$" # case insensitive
'^p=\d+\.\d+(?:e-\d+)?$'
'^\d*[pq][\d\.\-]*$'
'^[UACTG]+$'
"^5['′]-[UACTG]+$" # case insensitive
"^[UACTG]+-3['′]?+$"
'^p\d+\/p\d+$'
'^5′[ACTUG]+3′$'
'^(?:https?|ftp)?(?:\/{1,2})?(?:www\.)?[\w+\.\-]+\.(com|org|fr|jp|us|hk|cn|net|ch|gov|edu|ca|uk|de|info|dk|tw|il)(?:\:\d+)?(?:\/.+)*\/?$'
'^\d+[a-z]-[a-z]$'
'^[A-Z\d]*\d+[A-Z\d]*$'
'^5-[ACUTG]+$'
'^[ACUTG-]+$' # -> genseq
'^\d+p\d+-p\d+$'
'^p=\d(?:\.\d+)?×10−?\d+$'
'^[\w\.]+\.jpg$'
'^[a-z]+=[\d\.\-—−∶:–+=,\/]+$'
'^5-[ACUTG]+-3$'
# add reference pattern
'^58-[ACUTG]+-38$'
'^\d+\.\d+(?:e[+- ]{0,3}\d+)?$'
'^\d+–\d+del[A-Z]+$'
'^\d*ins\d*$'
'[AUTCG]{5,}'
'^p\.[A-Z]\d+(?:\-[A-Z]\d+)?$'
'^v(?:er(?:sion)?)?[\.\d ]+$'
"^[3589S'´′ \-]{1,4}[ACTUG]{5,}[3589'´′ \-]{1,4}$"
'^doi:[\w\.\/\- ]+$'
'\d{1,3}(?:,\d{3})+' # to replace

# typo
'Referencec'
# '^fig(?:ure)?s?[\w ,\.]+$' # notice, no consecutive english letter, try to resolve it.

r"^[A-Z]\d+_[A-Z]\d+del$" # 65 rows filtered out
r"^[A-Z]\d+del$" # 32 rows filtered out
r"^\d+_\d+del$" # 4 rows filtered out
r"^[A-Z]\d+_[A-Z]\d+DEL$" # 1 rows filtered out


r"^[A-Z]\d+ins[A-Z]+$" # 3 rows filtered out
r"^[A-Z]\d+_[A-Z]\d+ins[A-Z]+$" # 40 rows filtered out
r"^\d+_\d+ins[A-Z]+$" # 1 rows filtered out
r"^[A-Z]\d+_[A-Z]\d+ins$" # 1 rows filtered out


r"^[A-Z]\d+_[A-Z]\d+delins[A-Z]+$" # 33 rows filtered out
r"^[A-Z]\d+delins[A-Z]+$" # 4 rows filtered out
r"^[A-Z]\d+[A-Z\*]$" # 8206 rows filtered out

r"^[A-Z]\d+_[A-Z]\d+dup$" # 10 rows filtered out
r"^[A-Z]\d+dup$" # 5 rows filtered out
r"^[A-Z]\d+_[A-Z]\d+trunc$" # 1 rows filtered out
r"^\d+_\d+trunc$" # 4 rows filtered out
r"^[A-Z]\d+fs" # 14 rows filtered out
r"^[A-Z]\d+[A-Z]fs\*\d+$" # 6 rows filtered out
r"^[A-Z]\d+[A-Z]fs\*$" # 2 rows filtered out
r"^[A-Z]\d+_splice$" # 9 rows filtered out
r"^\d+_\d+splice$" # 2 rows filtered out
r"^\d+_[A-Z]\d+splice$" # 1 rows filtered out
r"^Exon \d+ \w+$" # 10 rows filtered out
r"^Exon \d+ \w+/\w+$" # 2 rows filtered out
r"^Promoter Mutations$" # 1 rows filtered out
r"^Promoter Hypermethylation$" # 2 rows filtered out
r"^[A-Z0-9]+v[VIX]+$" # 4 rows filtered out
r"^DNA binding domain (\w+ )*\w+$" # 3 rows filtered out
r"^Truncating Mutations$" # 113 rows filtered out
r"^[A-Z0-9]-[A-Z0-9]+-\d+ Fusion$" # 2 rows filtered out
r"^[A-Z0-9]+-[A-Z0-9]+ Fusion$" # 153 rows filtered out
r"^Deletion$" # 88 rows filtered out
r"^Epigenetic Silencing$" # 1 rows filtered out
r"^Hypermethylation$" # 1 rows filtered out
r"^Amplification$" # 79 rows filtered out
r"^Overexpression$" # 6 rows filtered out
r"^null\d+[A-Z]$" # 19 rows filtered out