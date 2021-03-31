from wolf import Task
import os

img = "gcr.io/broad-getzlab-workflows/maf2vcflite:v7"


def split_maf(fullmaf):

    return Task(
        name="split_maf",
        inputs={"maf": fullmaf},
        outputs={"submaf": "*.submaf"},
        script=[
            """
          python /app/subset_maf.py ${maf}
          """
        ],
        docker=img,
        resources={"mem": "10G"},
    )


def maf2vcf(ref, maf):
    # preprocessing logic can go here
    return Task(
        name="maf2vcf",
        inputs={
            "ref": ref,
            "maf": maf,
        },
        script=[
            """
        pairname=$(basename ${maf} .submaf)
        python /app/write_vcf.py -tsv ${maf} -ref ${ref} -o_vcf ${pairname}.vcf
        """
        ],
        outputs={"vcf": "*.vcf"},
        docker=img,
        resources={"mem": "2G"},
    )


def left_align(vcf, ref):
    return Task(
        name="gatk_leftalign",
        inputs={"ref": ref, "vcf": vcf},
        script=[
            """
pairname=$(basename ${vcf} .vcf)
gatk LeftAlignAndTrimVariants -R ${ref} -V ${vcf} -O ${pairname}.fixed.vcf
      """
        ],
        outputs={"fixed_vcf": "*.fixed.vcf"},
        docker="gcr.io/broad-getzlab-workflows/gatk4_wolf:v7",
        resources={"mem": "2G"},
    )


def funcotate(vcf, ref):
    # preprocessing logic can go here
    return Task(
        name="funcotate",
        inputs={
            "ref": ref,
            "vcf": vcf,
        },
        script=[
            """
        pairname=$(basename ${vcf} .vcf)
        echo ${pairname}
        gatk Funcotator \
    -R ${ref} \
    -V ${vcf} \
    -O ${pairname}.maf \
    --output-file-format MAF \
    --data-sources-path /mnt/nfs/wgs_ref/funcotator_dataSources.v1.6.20190124s \
    --transcript-list /mnt/nfs/wgs_ref/transcriptList.exact_uniprot_matches.AKT1_CRLF2_FGFR1.txt \
    --annotation-default normal_barcode:${pairname}_N \
    --annotation-default tumor_barcode:${pairname}_T \
    --ref-version hg38
        """
        ],
        outputs={"maf": "*.maf"},
        docker="gcr.io/broad-getzlab-workflows/gatk4_wolf:v6",
        resources={"mem": "6G"},
    )


def merge(mafs_in, rcols):
    return Task(
        name="merge_funcotated",
        inputs={"mafs": mafs_in, "rcols": rcols},
        script=[
            """
skiplines=$(grep '##' out.maf | wc -l)
python /app/merge.py -i <(head -c-1 ${mafs} | tr '\n' ',') -o merged_final.maf -r ${rcols} -skip $(( $skiplines + 1 ))
      """
        ],
        outputs={"final": "merged_final.maf"},
        docker="gcr.io/broad-getzlab-workflows/maf2vcflite:v6",
        resources={"mem": "10G"},
    )
