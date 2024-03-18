class OrganismSelector:
    def __init__(self, amino_acid_sequence):
        self.amino_acid_sequence = amino_acid_sequence
        self.organism_data = None

    def organism_data_parse(self, organism_info):
        """
        Parses organism information and returns a dictionary with organism data.

        :param organism_info: Information about the organism.
        :return: Dictionary with organism data.
        """
        organism_data = dict()

        if isinstance(organism_info, str):
            data_pairs = organism_info.split(',')
            for pair in data_pairs:
                key, value = pair.split(':')
                organism_data[key.strip()] = value.strip()

        elif isinstance(organism_info, dict):
            organism_data = organism_info

        self.organism_data = organism_data
        return organism_data

    def organism_selector(self):
        """
        Selects an organism based on the amino acid sequence.

        :return: Variable organism with selected organism data.
        """

        organism_info = "name:E.coli,complexity:simple"
        organism_data = self.organism_data_parse(organism_info)

        organism = organism_data
        return organism

    def print_organism_data_parse(self, organism_info):
        pass


class PlasmidModel:
    def __init__(self, amino_acid_sequence):
        self.amino_acid_sequence = amino_acid_sequence
        self.nucleotide_sequence = ""
        self.plasmid_data = ""
        self.tag_sequence = ""

    def sequence_parser(self, amino_acid_sequence, plasmid_sequence):
        """
        Translates an amino acid sequence to a nucleotide sequence and appends it to the plasmid sequence.

        :param amino_acid_sequence: A string of amino acids.
        :param plasmid_sequence: A string representing the sequence of the plasmid.
        :return: A string representing the nucleotide sequence.
        """
        return plasmid_sequence + amino_acid_sequence

    def plasmid_parser(self, sequence):
        """
        Converts sequence data into another format.

        :param sequence: A string representing the nucleotide sequence.
        :return: The formatted sequence data.
        """

        return sequence

    def plasmid_init(self, plasmid_sequence):
        """
        Initializes the plasmid by translating the amino acid sequence and integrating it.

        :param plasmid_sequence: A string representing the sequence of the plasmid.
        :return: Initialized plasmid data.
        """

        nucleotide_sequence = self.sequence_parser(self.amino_acid_sequence, plasmid_sequence)

        self.plasmid_data = self.plasmid_parser(nucleotide_sequence)

        self.nucleotide_sequence = nucleotide_sequence
        return self.plasmid_data

    def plasmid_mod(self, plasmid_sequence, tag_sequnce):
        """
        Modyfied plasmid with tags
        :param plasmid_sequence: Initialized plasmid data.
        :return: modyfied plasmid with tags
        """

        return plasmid_sequence


class Cultivation:
    """
    The Cultivation class orchestrates the cultivation process of organisms that have been transformed
    with a plasmid containing a specific gene sequence. It collaborates with the OrganismSelector
    to choose a suitable host organism and the PlasmidModel to construct the plasmid required for
    gene expression.
    """

    def __init__(self, amino_acid_sequence, plasmid_sequence, environment):
        """
        Initializes the Cultivation process with the amino acid sequence of the target protein
        and the sequence of the plasmid vector.

        :param amino_acid_sequence: String representing the sequence of amino acids.
        :param plasmid_sequence: String representing the initial sequence of the plasmid.
        """
        self.amino_acid_sequence = amino_acid_sequence
        self.plasmid_sequence = plasmid_sequence
        self.environment = environment

    def perform_cultivation(self):
        """
        Carries out the cultivation process. It selects an appropriate organism for the expression
        of the target protein and prepares the plasmid for transformation.

        :return: Information about the cultivation environment.
        """
        organism_selector = OrganismSelector(self.amino_acid_sequence)
        organism = organism_selector.organism_selector()

        plasmid_model = PlasmidModel(self.amino_acid_sequence)
        plasmid = plasmid_model.plasmid_init(self.plasmid_sequence)

        environment = {
            'organism': organism,
            'plasmid': plasmid,
            'enviroment': self.environment
        }

        return environment


class ProteinPurificationOptimizer:
    """
        This class provides functionality to determine the optimal purification method
        for a protein based on the tag used.

        Attributes:
            tags_methods (dict): A dictionary mapping tags to their optimal purification methods.
    """

    def __init__(self, purification_methods):
        """
        :param purification_methods: Dictionary with tags as keys and purification methods as values.
        """
        self.purification_methods = purification_methods

    def find_optimal_purification_method(self, tag):
        """
        Find the optimal protein purification method based on the tag.

        :param tag: The tag for which to find the purification method.
        :return: The optimal purification method for the given tag.
        """
        return self.purification_methods.get(tag, "No method found for this tag")