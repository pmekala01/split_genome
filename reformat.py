"""
This program reformats a fasta file to place the entirety of a contig onto
a singular line, split by definition lines, primary assemblies only.

For example,

>chromosome 1 Primary Assembly
AGCT
TCGA
>chromosome 2 Primary Assembly
AAAA
TTTT
>chromosome 1 random contig
GGCC
TTAA
>chromosome 2 random contig
GGGG
CCCC

becomes:

>chromosome 1 Primary Assembly
AGCTTCGA
>chromosome 2 Primary Assembly
AAAATTTT

"""
import re
from pathlib import Path
from typing import Final

# OLD_FNA_PATH: Final[Path] = Path(r"fna_files/GCF.fna")
OLD_FNA_PATH: Final[Path] = Path(r"GCF.fna")
# NEW_FNA_PATH: Final[Path] = Path(r"fna_files/GCF_formatted.fna")
NEW_FNA_PATH: Final[Path] = Path(r"output.txt")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")


def main() -> None:
    # chromosome: str = ""
    # with OLD_FNA_PATH.open("r") as rf:
        # for line in rf:
            # if line.startswith(">"):
                # res: list = CHR_NUM_PATTERN.findall(line)
                # chromosome = "unplaced" if not res else res[0]
                # new_file: Path = NEW_FNA_PATH / f"{chromosome}.fna"
                # with new_file.open("a"):
                    # pass  # TODO: do this later lol
    with OLD_FNA_PATH.open("r") as rf, NEW_FNA_PATH.open("w") as wf:
        line: str = rf.readline()
        is_good: bool = True
        wf.write(line)
        while line:
            line = rf.readline()
            if not line.startswith(">"):
                line = line[:-1]
            else:
                line = line.lower()
                is_good = "primary" in line and "unplaced" not in line and "unlocalized" not in line
                if is_good:
                    wf.write("\n")
            if is_good:
                wf.write(line)

    return

if __name__ == "__main__":
    main()