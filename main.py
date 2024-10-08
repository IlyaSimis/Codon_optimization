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


    def select_codon(self, amino_acid_sequence):
        selected_codons = []

        for amino_acid in amino_acid_sequence:
            codons_info = self.tables.get_codons_info(amino_acid)
            if codons_info:
                most_frequent_codon = max(codons_info, key=lambda x: x['relative_frequency'])
                selected_codons.append(most_frequent_codon['codon'])

        return selected_codons

