# Funcotate multi-sample MAF


The workflow / tool aims to reannotate a MAF with the following columns -- the calls are aggregated from different samples of several cohorts. We'd like to keep `called_by` and `cohort` information, and keep sample information in `Tumor_Sample_Barcode` (with `sample_id` + `"_T"`) in the final aggregated MAF.

```
contig  startpos        endpos  altbase cohort  sample_id       called_by       refbase n_ref_count     n_alt_count     t_ref_count     t_alt_count
chr1    13511   13511   A       COAD    11CO007 washu   C       502     1       219     35
chr1    13620   13620   A       COAD    11CO059 washu   G       444     1       422     26
chr1    69439   69439   G       LUAD    C3N-02089       washu   A       418     0       283     126
chr1    69601   69601   C       LSCC    C3N-03875       washu   T       470     0       480     45
chr1    69706   69706   A       UCEC    C3N-00328       washu   C       69      0       28      14
chr1    69709   69709   T       LUAD    C3N-00169       washu   C       129     0       77      7
chr1    494348  494348  T       COAD    11CO018 washu   G       88      0       61      58
chr1    494541  494541  A       BRCA    01BR043 washu   G       784     4       394     177
chr1    729140  729140  G       CCRCC   C3N-00244       washu   A       54      0       64      22
```

The workflow first split the aggregated MAF to submafs with only calls from a sample, while keeping the caller/cohort information in VCF INFO fields. Funcotator runs on VCF for each sample and finally merged to a single union MAF removing whatever columns specified with `RCOL`. Check out `workflow.py` for more details.

## Be cautious!

This is not a production workflow! e.g. there's VCF header for reference checks -- so it would become user's responsibility to make sure the correct ref.fasta file is used.
