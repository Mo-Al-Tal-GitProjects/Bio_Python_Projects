# Import necessary libraries
import matplotlib.pyplot as plt
from Bio import SeqIO
from Bio.SeqUtils import GC
from Bio.Seq import Seq
from Bio.Align import PairwiseAligner

# Function to input a DNA sequence from the user
def input_dna_sequence():
  return input("Enter a DNA sequence: ").upper()
  
# Function to read DNA sequence from a file
def read_sequence_from_file(file_path):
  for record in SeqIO.parse(file_path, "fasta"):
    return str(record.seq).upper()
    
# Function to calculate the length of a DNA sequence
def calculate_sequence_length(dna_sequence):
  return len(dna_sequence)
  
# Function to calculate the GC content of a DNA sequence
  def calculate_gc_content(dna_sequence):
    return GC(dna_sequence)
    
# Function to plot GC content
def plot_gc_content(dna_sequence):
# Adjust the window size if the sequence is shorter than 100 bases
  window_size = min(50, len(dna_sequence) // 2)
  gc_values = [GC(dna_sequence[i:i+window_size]) for i in
  range(len(dna_sequence) - window_size + 1)]
  plt.plot(gc_values)
  plt.title("GC Content over Sequence")
  plt.xlabel("Position")
  plt.ylabel("GC%")
  plt.show()
  
def plot_nucleotide_frequency(dna_sequence):
  nucleotides = ['A', 'T', 'C', 'G']
  frequencies = {nucleotide: dna_sequence.count(nucleotide) for nucleotide in
  nucleotides}
  plt.bar(frequencies.keys(), frequencies.values())
  plt.title("Nucleotide Frequency")
  plt.xlabel("Nucleotide")
  plt.ylabel("Frequency")
  plt.show()
  
def plot_gc_per_position(dna_sequence):
  gc_flags = [1 if nucleotide in ['G', 'C'] else 0 for nucleotide in
  dna_sequence]
  plt.plot(gc_flags, 'ro-') # 'ro-' means red color, circle marker, and solid
  line
  plt.title("GC Presence per Position")
  plt.xlabel("Position")
  plt.ylabel("GC Present")
  plt.ylim(-0.5, 1.5) # Set y-axis limits to show binary flags clearly
  plt.show()
  
# Function to predict protein from DNA sequence
def predict_protein(dna_sequence):
  dna_seq = Seq(dna_sequence)
  protein = dna_seq.translate()
  return str(protein)
  
# Function to compare two DNA sequences
def compare_sequences(seq1, seq2):
  aligner = PairwiseAligner()
  alignments = aligner.align(seq1, seq2)
  for alignment in alignments:
  print(alignment)
  
# Main function
def main():
  print("DNA Sequence Analyzer - Enhanced")
# User choice for input method
choice = input("Enter 1 to input DNA sequence manually, 2 to read from file:")
  if choice == '1':
    dna_sequence = input_dna_sequence()
  elif choice == '2':
    file_path = input("Enter the file path: ")
    dna_sequence = read_sequence_from_file(file_path)
  else:
    print("Invalid choice")
    return
    
if dna_sequence:
  sequence_length = calculate_sequence_length(dna_sequence)
  print(f"Sequence Length: {sequence_length} base pairs")
  gc_content = calculate_gc_content(dna_sequence)
  print(f"GC Content: {gc_content:.2f}%")
  plot_gc_content(dna_sequence)
  plot_nucleotide_frequency(dna_sequence)
  plot_gc_per_position(dna_sequence)
  protein = predict_protein(dna_sequence)
  print(f"Predicted Protein: {protein}")
  # Optional: Sequence comparison
  # ...
else:
  print("No DNA sequence provided.")
  
# Entry point of the script
if __name__ == "__main__":
main()
