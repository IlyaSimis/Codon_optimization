from main import *

selector_instance = CodonSelector(organism="ecoli")
amino_acid_sequence = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"
selected_codons = selector_instance.select_codon(amino_acid_sequence)
print(selected_codons)

selector_instance = CodonSelector(organism="hsapiens")
selected_codons = selector_instance.select_codon(amino_acid_sequence)
print(selected_codons)
