import argparse
import pandas as pd

# parse inputs
def parse_args():
    parser = argparse.ArgumentParser(description="merge funcotated MAF")

    # files IO
    parser.add_argument(
        "-i", required=True, help="Paths to input mafs concatenated by comma"
    )
    parser.add_argument(
        "-o",
        required=True,
        help="Path to output maf file (with a minimal set of columns)",
    )
    parser.add_argument("-r", help="Path to columns to remove", default=None)
    parser.add_argument(
        "-skip", help="Number of noninformative rows", default=None, type=int
    )
    args = parser.parse_args()
    return args


args = parse_args()

with open(args.i) as f:
    inputs = f.read()


l = []

# read file of removed columns
with open(args.r) as f:
    cols_to_remove = [line.rstrip() for line in f]

for maf in inputs.split(","):
    l.append(
        pd.read_csv(
            maf,
            sep="\t",
            usecols=lambda x: x not in cols_to_remove,
            skiprows=lambda x: x in list(range(args.skip)),
            low_memory=False,
        )
    )

pd.concat(l).to_csv(args.o, index=False, sep="\t")
