import csv
import re
from pathlib import Path
from typing import Final, Optional

SEQUENCE_LENGTH = 10000
INPUT_FILE: Final[Path] = Path("output.txt")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|X+|Y+)")
CHR_LABELS = [str(i) for i in range(1, 23)] + ['X', 'Y', 'unplaced']

def parse_genome_data(input_file):
    chromosomes = {label: "" for label in CHR_LABELS}
    #print("1")
    with input_file.open("r") as rf:
        current_chromosome: Optional[str] = None
        #print("2")
        line: str = rf.readline()
        while line:
            line = line.strip()  # remove the \n at the end of a line
            #print("22")
            if line.startswith(">"):
                res: Optional[re.Match] = CHR_NUM_PATTERN.search(line)
                current_chromosome = "unplaced" if not res else res.group(1)
                #print("3")
            else:
                if current_chromosome:
                    chromosomes[current_chromosome] += line.upper()
                    #print("4")
            line = rf.readline()

    return chromosomes

def process_chromosome(sequence, chromosome_id):
    sequence = re.sub(r'\s+', '', sequence)  # Remove any whitespace or newline characters in the sequence
    rows = []
    id_count = 1
    
    for i in range(0, len(sequence), SEQUENCE_LENGTH):
        segment = sequence[i:i+SEQUENCE_LENGTH]
        length = len(segment)
        ambiguous_count = sum(1 for base in segment if base not in 'ACTG')
        row = [id_count, length, ambiguous_count, segment]
        rows.append(row)
        # Print progress
        print(f'Processing row {id_count} in chromosome {chromosome_id}')
        id_count += 1
    
    return rows

def write_to_csv(chromosome_id, rows):
    output_file = f'chromosome_{chromosome_id}.csv'
    with open(output_file, 'w') as txtfile:
        txtfile.write(f'Chromosome {chromosome_id}\n')
        txtfile.write(f'{"ID":<5} | {"Length":<6} | {"Ambiguous Base Count":<20} | {"Sequence"}\n')
        txtfile.write('-' * 60 + '\n')
        for row in rows:
            txtfile.write(f'{row[0]:<5} | {row[1]:<6} | {row[2]:<20} | {row[3]}\n')
    
    print(f'Table written to {output_file}')

def main():
    chromosomes = parse_genome_data(INPUT_FILE)
    
    for chromosome_id, sequence in chromosomes.items():
        #print("10")
        if sequence:  # Only process if there is a sequence for this chromosome
            rows = process_chromosome(sequence, chromosome_id)
            #print("11")
            write_to_csv(chromosome_id, rows)
            #print("12")

if __name__ == '__main__':
    main()

