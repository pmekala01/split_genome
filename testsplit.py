import argparse
import csv
import re
from pathlib import Path
from typing import Final, Optional

INPUT_FILE: Final[Path] = Path("output.txt")
CHR_NUM_PATTERN: Final[re.Pattern] = re.compile(r"chromosome (\d+|x+|y+)")
CHR_LABELS = [str(i) for i in range(1, 23)] + ['x', 'y', 'unplaced']

def parse_genome_data(input_file):
    chromosomes = {label: "" for label in CHR_LABELS}
    with input_file.open("r") as rf:
        current_chromosome: Optional[str] = None
        line: str = rf.readline()
        while line:
            line = line.strip()
            if line.startswith(">"):
                res: Optional[re.Match] = CHR_NUM_PATTERN.findall(line)
                current_chromosome = "unplaced" if not res else res[0]
                print(f"{current_chromosome}\n")
            else:
                if current_chromosome:
                    chromosomes[current_chromosome] += line.upper()
            line = rf.readline()
    return chromosomes

def count_consecutive_ambiguous_bases(segment):
    max_count = 0
    current_count = 0
    
    for base in segment:
        if base not in 'ACTG':
            current_count += 1
            if current_count > max_count:
                max_count = current_count
        else:
            current_count = 0
    
    return max_count if max_count > 5000 else 0

def process_chromosome(sequence, chromosome_id, sequence_length):
    sequence = re.sub(r'\s+', '', sequence)
    rows = []
    id_count = 1
    half_length = sequence_length // 2
    
    for i in range(0, len(sequence) - half_length + 1, half_length):
        segment = sequence[i:i + sequence_length]
        length = len(segment)
        ambiguous_count = sum(1 for base in segment if base not in 'ACTG')
        continuous_n_count = count_consecutive_ambiguous_bases(segment)
        start_position = i + 1  # Position is 1-based
        row = [id_count, length, ambiguous_count, continuous_n_count, start_position, segment]
        rows.append(row)
        id_count += 1
    
    return rows

def write_to_csv(chromosome_id, rows):
    output_file = f'chromosome_{chromosome_id}.csv'
    with open(output_file, 'w') as txtfile:
        txtfile.write(f'Chromosome {chromosome_id}\n')
        txtfile.write(f'{"ID":<5} | {"Length":<6} | {"Ambiguous Base Count":<20} | {"Continuous N Count":<20} | {"Position":<8} | {"Sequence"}\n')
        txtfile.write('-' * 100 + '\n')
        for row in rows:
            txtfile.write(f'{row[0]:<5} | {row[1]:<6} | {row[2]:<20} | {row[3]:<20} | {row[4]:<8} | {row[5]}\n')
    
    print(f'Table written to {output_file}')

def main():
    parser = argparse.ArgumentParser(description='Process genome data.')
    parser.add_argument('sequence_length', type=int, help='Length of the sequence to be processed')
    args = parser.parse_args()

    sequence_length = args.sequence_length
    chromosomes = parse_genome_data(INPUT_FILE)
    
    for chromosome_id, sequence in chromosomes.items():
        if sequence:
            rows = process_chromosome(sequence, chromosome_id, sequence_length)
            write_to_csv(chromosome_id, rows)

if __name__ == '__main__':
    main()
