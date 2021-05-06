import wolf
from wolF import *


def workflow(fullmaf, REF, RCOL, output_format):

    split_task = split_maf(fullmaf)
    maf2vcf_task = maf2vcf(ref=REF, maf=split_task["submaf"])
    left_align_task = left_align(ref=REF, vcf=maf2vcf_task["vcf"])
    funcotate_task = funcotate(
        vcf=left_align_task["fixed_vcf"], ref=REF, output_format=output_format
    )
    if output_format == "MAF": # a.k.a the union MAF we produced
        merge_task = merge_maf(
            mafs_in=[funcotate_task.get_output("MAF", unbox=False)], rcols=RCOL
        )
    elif output_format == "VCF":
        # no one asked for aggregated VCF yet, but if we ever need to, we should use `bcftools merge`
        pass


if __name__ == "__main__":
    with wolf.WolfWorkflow(
        workflow=workflow,
        # common_task_opts = { "retry" : 2 } # will retry every task up to 5 times
    ) as w:
        # dispatch workflow for every pair in the dataframe
        w.run(
            run_name="cptac_v5_vcf",
            fullmaf="/mnt/nfs/wgs_ref/merged_fixed_v5.maflite",
            REF="/mnt/nfs/wgs_ref/GRCh38.d1.vd1.fa",
            RCOL="/mnt/nfs/wgs_ref/cols2remove.txt", # a list of redundant columns that we want to omit
            output_format="VCF",
        )
        #
