# wrte header
from pyfaidx import Fasta
import pandas as pd
import argparse

def parse_args():
	parser = argparse.ArgumentParser(description = "Merging SNP on-cis from MuTect1 result to DNP/TNP/ONP")

	# input files
	parser.add_argument("-tsv", required = True, help = "Path to input validated maf file")
	parser.add_argument("-ref", required = True, help = "Path to ref.fasta")

	# output files	
	parser.add_argument("-o_vcf", required = True, help = "Path to output VCF file that contains SNP/INDEL/XNP")
	
	args = parser.parse_args()
	return args

def get_refbase(reffa, contig_idx, seq_idx):
	"""
	read refbase from ref.fa with contig and seq index
	"""
	return reffa[contig_idx][seq_idx].seq


if __name__ == "__main__":
	args = parse_args()
	REF_FA = Fasta(args.ref, rebuild = False)
	smaf = pd.read_csv(args.tsv, sep = '\t')


	"""
	##fileformat=VCFv4.1
	##INFO=<ID=washu,Number=0,Type=Flag,Description="Variant reported in Washu Pipeline only">
	##INFO=<ID=getz,Number=0,Type=Flag,Description="Variant reported in Getz Pipeline only">
	##INFO=<ID=COHORT,Number=1,Type=String,Description="CPTAC cohort">
	##tumor_sample=tumor
	##normal_sample=normal
	"""
	f = open(args.o_vcf, "w")
	f.writelines([
				"##fileformat=VCFv4.1\n", 
				'##INFO=<ID=COHORT,Number=1,Type=String,Description="CPTAC cohort">\n',
				'##INFO=<ID=washu,Number=0,Type=Flag,Description="Variant reported in Washu Pipeline only">\n',
				'##INFO=<ID=getz,Number=0,Type=Flag,Description="Variant reported in Getz Pipeline only">\n',
				"##tumor_sample=tumor\n",
				"##normal_sample=normal\n",
				])
	f.close()

	vcf_header = "#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  normal   tumor".split()
	temp = smaf.assign(
		ID  = '.',
		QUAL = '.',
		FILTER = 'PASS',
		FORMAT = 'AD'
	).loc[:, vcf_header].replace("-", ".")


	for i, r in temp.iterrows():
		if r["REF"] == ".":
			temp.at[i, 'REF'] = get_refbase(REF_FA, r["#CHROM"], int(r["POS"])-1).capitalize()

	temp.to_csv(args.o_vcf, sep = '\t', index = False, mode = 'a')