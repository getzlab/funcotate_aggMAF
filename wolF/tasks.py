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


def funcotate(vcf, ref, output_format):
    # preprocessing logic can go here
    return Task(
        name="funcotate_{}".format(output_format),
        inputs={
            "ref": ref,
            "vcf": vcf,
            "output_format": output_format,
            "suffix": output_format.lower(),
        },
        script=[
            """
        pairname=$(basename ${vcf} .fixed.vcf)
        echo ${pairname}
        gatk Funcotator \
    -R ${ref} \
    -V ${vcf} \
    -O ${pairname}.${suffix} \
    --output-file-format ${output_format} \
    --data-sources-path /mnt/nfs/wgs_ref/funcotator_dataSources.v1.6.20190124s \
    --annotation-default normal_barcode:${pairname}_N \
    --annotation-default tumor_barcode:${pairname}_T \
    --ref-version hg38
        """,
        ],
        outputs={output_format: "*.{}".format(output_format.lower())},
        docker="gcr.io/broad-getzlab-workflows/gatk4_wolf:v6",
        resources={"mem": "6G"},
    )


def merge_maf(mafs_in, rcols):
    return Task(
        name="merge_funcotated_maf",
        inputs={"mafs": mafs_in, "rcols": rcols},
        script=[
            """
skiplines=$(grep '##' $(head -n1 ${mafs}) | wc -l)
echo $skiplines
python /app/merge.py -i <(head -c-1 ${mafs} | tr '\n' ',') -o merged_final.maf -r ${rcols} -skip $(( $skiplines + 1 ))
      """
        ],
        outputs={"final": "merged_final.maf"},
        docker=img,
        resources={"mem": "10G"},
    )

