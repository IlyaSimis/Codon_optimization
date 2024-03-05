from Usage_tables import *


class CodonSelector:
    def __init__(self, organism):
        if organism.lower() == "ecoli":
            self.tables = Tables(ecoli_usage().strip().split("\n"))
        elif organism.lower() == "hsapiens":
            self.tables = Tables(hsapiens_usage().strip().split("\n"))
        else:
           raise ValueError("Invalid organism specified. Please specify 'ecoli' or 'human'.")

        self.tables.create_table()

    def translate_sequence(self, sequence):

        if sequence[:3] != 'AUG':
            raise ValueError("Sequence must start with start codon")
        if len(sequence) % 3 != 0:
            raise ValueError("Длина последовательности должна быть кратна 3")
        codons = [sequence[i:i+3] for i in range(0, len(sequence), 3)]
        amino_acids = [genetic_code()[codon] for codon in codons]

        return ''.join(amino_acids)

    def select_codon(self, sequence):

        if set(sequence) <= {'A', 'U', 'C', 'G'}:
            amino_acid_sequence = self.translate_sequence(sequence)
        else:
            amino_acid_sequence = sequence
            if amino_acid_sequence[0] != 'M':
                raise ValueError("Sequence must start with start codon")

        selected_codons = []

        for amino_acid in amino_acid_sequence:
            codons_info = self.tables.get_codons_info(amino_acid)
            if codons_info:
                most_frequent_codon = max(codons_info, key=lambda x: x['relative_frequency'])
                selected_codons.append(most_frequent_codon['codon'])

        stop_codon_info = self.tables.get_codons_info('*')
        if stop_codon_info:
            stop_codon = max(stop_codon_info, key=lambda x: x['relative_frequency'])
            selected_codons.append(stop_codon['codon'])

        return selected_codons


class CAICalculator:
    def __init__(self, codons, codon_table):
        self.codons = codons
        self.codon_table = codon_table

    def calculate_cai(self):
        reference_values = [codon_data['relative_frequency'] for codon, codon_data in self.codon_table.items() if codon in self.codons]
        target_values = [codon_data['relative_frequency'] for codon, codon_data in self.codon_table.items() if codon in self.codons]

        cai = 1
        for ref_val, target_val in zip(reference_values, target_values):
            cai *= (target_val / ref_val) ** (1 / len(reference_values))

        return cai
