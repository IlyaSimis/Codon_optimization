from ecoli import ecoli_usage
from hsapiens import hsapiens_usage


class Tables:
    def __init__(self, data):
        self.data = data
        self.result = {}

    def create_table(self):
        for line in self.data:
            parts = line.split(",")
            amino_acid = parts[0]
            codon = parts[1]
            relative_frequency = float(parts[2])

            if amino_acid not in self.result:
                self.result[amino_acid] = []

            self.result[amino_acid].append({"codon": codon, "relative_frequency": relative_frequency})

    def get_codons_info(self, amino_acid):
        return self.result.get(amino_acid)
