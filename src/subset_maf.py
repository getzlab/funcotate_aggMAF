import pandas as pd
import sys

MAF = pd.read_csv(sys.argv[1], sep = '\t')
chrseq = ["chr"+ str(i) for i in list(range(1, 23))+ ["X", "Y"]]
MAF['called_by'] = MAF['called_by'].str.replace(',',';')

MAF = MAF.drop(columns = ["callers", "vclass", "Protein_Change",  "gene"])\
.assign(
    tumor = MAF.apply(lambda x: "{},{}".format(
        x['t_ref_count'], 
        x['t_alt_count']), axis=1), 
    normal = MAF.apply(lambda x: "{},{}".format(
        x['n_ref_count'], 
        x['n_alt_count']), axis=1), 
    contig_id = MAF['contig'].map(lambda x: chrseq.index(x)),
    info = MAF.apply(lambda x: "COHORT={};{}".format(
        x['cohort'], 
        x['called_by']), axis=1), 
).sort_values(['sample_id', 'contig_id', 'startpos'])\
.rename(columns = {
    'contig': "#CHROM",
    'startpos': "POS",
    'refbase':'REF',
    'altbase':'ALT',
    'info': 'INFO'
})
# split to separate files
grouped = MAF.groupby("sample_id")
for name, group in grouped:
    group.to_csv("{}.submaf".format(name), sep = '\t',  index = False)
