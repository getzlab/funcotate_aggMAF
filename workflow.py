import  wolf
from wolF import *

def workflow(fullmaf, REF, RCOL):

    split_task = split_maf(fullmaf)
    maf2vcf_task = maf2vcf(
        ref = REF, 
        maf = split_task["submaf"]
        )
    funcotate_task = funcotate(
        vcf = maf2vcf_task["vcf"],
        ref = REF, 
        )
    merge_task = merge(
        mafs_in = funcotate_task.get_output("maf", lambda x : ",".join(x)),
        rcols = RCOL
    )

if __name__ == "__main__":
    with wolf.WolfWorkflow(
        workflow = workflow,
        # common_task_opts = { "retry" : 2 } # will retry every task up to 5 times
        ) as w:
            # dispatch workflow for every pair in the dataframe
            w.run(run_name="funcotate_maf", 
                  fullmaf = "/mnt/nfs/wgs_ref/merged_fixed.maflite",
                  REF = "/mnt/nfs/wgs_ref/GRCh38.d1.vd1.fa",
                  RCOL = "/mnt/nfs/wgs_ref/cols2remove.txt"
            )