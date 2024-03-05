from main import *

selector_instance = CodonSelector(organism="ecoli")
amino_acid_sequence = "AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA"
selected_codons = selector_instance.select_codon(amino_acid_sequence)

print(selected_codons)

selector_instance = CodonSelector(organism="hsapiens")
selected_codons = selector_instance.select_codon(amino_acid_sequence)
print(selected_codons)

processor = Tables(data=hsapiens_usage().strip().split("\n"))
processor.create_table()
result = processor.get_result()
print(result)

cai_calculator = CAICalculator(selected_codons, result)
cai_value = cai_calculator.calculate_cai()
print("CAI value:", cai_value)
