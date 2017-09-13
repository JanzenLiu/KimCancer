import re

'^[\d\.\-—−–∶:–+=,\/]*$'
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
'^figs?(?:ure)?[\w ,\.]+$' # notice, no consecutive english letter, try to resolve it.

