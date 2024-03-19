import re
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.lines import Line2D
import numpy as np


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
    def __init__(self, plasmid_data, protein_fasta):
        """
        Initializes the PlasmidModel with plasmid and protein data.

        :param plasmid_data: A dictionary containing 'fasta' and 'features' keys.
        :param protein_fasta: A string in FASTA format containing the protein sequence.
        """
        self.plasmid_sequence = self.parse_fasta(plasmid_data['fasta'])
        self.protein_sequence = self.parse_fasta(protein_fasta)
        self.features = plasmid_data['features']
        self.combined_sequence = ""

    def parse_fasta(self, fasta_string):
        """
        Parses a FASTA string and extracts the sequence.

        :param fasta_string: A string in FASTA format.
        :return: A string representing the nucleotide or amino acid sequence.
        """
        fasta_body = re.sub(r'>.*\n', '', fasta_string)
        sequence = re.sub(r'\n', '', fasta_body)
        return sequence

    def combine_sequences(self):
        """
        Combines the plasmid sequence with the protein sequence.

        :return: A string representing the combined nucleotide sequence.
        """
        self.combined_sequence = self.plasmid_sequence + self.protein_sequence
        return self.combined_sequence

    def extract_feature_sequence(self, feature_name):
        """
        Extracts the sequence of a given feature from the plasmid based on its coordinates and direction.

        :param feature_name: The name of the feature to be extracted.
        :return: A string representing the nucleotide sequence of the feature.
        """
        if feature_name in self.features:
            start, end, direction = self.features[feature_name]
            if direction == 'cw':
                return self.plasmid_sequence[start-1:end]
            elif direction == 'ccw':
                # Extract and reverse-complement the sequence for features in the 'ccw' direction.
                return self._reverse_complement(self.plasmid_sequence[end-1:start])
            else:
                raise ValueError("Direction should be either 'cw' or 'ccw'.")
        else:
            raise ValueError(f"Feature '{feature_name}' not found in plasmid data.")

    def _reverse_complement(self, sequence):
        """
        Generates the reverse complement of a nucleotide sequence.

        :param sequence: The nucleotide sequence to reverse-complement.
        :return: The reverse complement sequence.
        """
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        return ''.join(complement.get(base, base) for base in reversed(sequence))

    def extract_feature_sequence(self, feature_name):
        """
        Extracts the sequence of a given feature from the plasmid based on its coordinates and direction.
        """
        if feature_name in self.features:
            start, end, direction = self.features[feature_name]
            if direction == 'cw':
                sequence = self.plasmid_sequence[start-1:end]
            elif direction == 'ccw':
                sequence = self.plasmid_sequence[end-1:start]
                sequence = self._reverse_complement(sequence)
            return sequence
        else:
            raise ValueError(f"Feature '{feature_name}' not found in plasmid data.")

    def plasmid_len(self):
        """
        Returns the length of the plasmid sequence.

        This method is useful for verifying the completeness of the inputted plasmid sequence
        and can be used to ensure that the feature coordinates correspond to the actual length
        of the plasmid sequence.

        :return: An integer value representing the number of nucleotides in the plasmid sequence.
        """
        return len(self.plasmid_sequence)

    def plot_plasmid(self):
        """
        Plots a circular diagram of the plasmid with marked features.
        Features are drawn on different levels to avoid overlapping, and closer to the main circle if possible.
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_aspect('equal')
        feature_width = 0.1

        base_radius = 0.9
        step = 0.05

        main_circle = plt.Circle((0, 0), base_radius, fill=False, color='black', linewidth=3)
        ax.add_artist(main_circle)

        levels = {}

        for feature_name, (start, end, direction) in sorted(self.features.items(), key=lambda x: x[1][0]):
            level = 0
            while any((start < levels.get(l, (0, 0))[1] and end > levels.get(l, (0, 0))[0]) for l in levels):
                level += step
            levels[level] = (start, end)

            start_angle, end_angle = self.get_angles(start, end, direction)
            color = next(ax._get_lines.prop_cycler)['color']
            wedge = Wedge((0, 0), base_radius - level, start_angle, end_angle, width=feature_width,
                          facecolor=color, edgecolor='black', label=feature_name)
            ax.add_patch(wedge)

            self.draw_boundary_line(ax, start_angle, feature_width)
            self.draw_boundary_line(ax, end_angle, feature_width)

        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        plt.axis('off')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

    def get_angles(self, start, end, direction):
        start_angle = (start / self.plasmid_len()) * 360
        end_angle = (end / self.plasmid_len()) * 360
        if direction == 'ccw':
            start_angle, end_angle = end_angle, start_angle
        return start_angle % 360, end_angle % 360

    def draw_boundary_line(self, ax, angle, feature_width):
        angle_rad = np.radians(angle)
        inner_radius = 0.9
        outer_radius = 1.05
        line = Line2D(
            [inner_radius * np.cos(angle_rad), outer_radius * np.cos(angle_rad)],
            [inner_radius * np.sin(angle_rad), outer_radius * np.sin(angle_rad)],
            color='black', linestyle='-', linewidth=1.5
        )
        ax.add_line(line)


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
