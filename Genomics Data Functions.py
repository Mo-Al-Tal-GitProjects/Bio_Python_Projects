import pandas as pd

class GenomicsData:
    def __init__(self, gene: str, sequence: str, length: int):
        self.gene = gene
        self.sequence = sequence
        self.length = length

    @classmethod
    def from_csv(cls, filepath: str) -> list:
        """
        Loads genomics data from a CSV file.

        Args:
            filepath (str): Path to the CSV file.

        Returns:
            list: List of GenomicsData objects.
        """
        try:
            df = pd.read_csv(filepath)
            genomics_data = []
            for _, row in df.iterrows():
                genomics_data.append(cls(row['Gene'], row['Sequence'], row['Length']))
            return genomics_data
        except Exception as e:
            print(f"Error loading genomics data from CSV: {e}")
            return []

    def filter_by_gene(self, gene_name: str) -> list:
        """
        Filters genomics data by gene name.

        Args:
            gene_name (str): Name of the gene to filter by.

        Returns:
            list: List of GenomicsData objects filtered by the gene name.
        """
        filtered_data = [data for data in self if data.gene == gene_name]
        return filtered_data

    def filter_by_sequence_length(self, min_length: int, max_length: int) -> list:
        """
        Filters genomics data by sequence length.

        Args:
            min_length (int): Minimum length of the sequence.
            max_length (int): Maximum length of the sequence.

        Returns:
            list: List of GenomicsData objects filtered by sequence length.
        """
        filtered_data = [data for data in self if min_length <= data.length <= max_length]
        return filtered_data

    def get_gene_names(self) -> list:
        """
        Retrieves a list of unique gene names from the genomics data.

        Returns:
            list: List of unique gene names.
        """
        gene_names = set(data.gene for data in self)
        return list(gene_names)
