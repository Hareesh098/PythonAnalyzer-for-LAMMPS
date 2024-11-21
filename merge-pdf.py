import os
from PyPDF2 import PdfMerger
import glob

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    try:
        for pdf in pdf_list:
            merger.append(pdf)
        merger.write(output_path)
    finally:
        merger.close()

# Define directory and pattern to find all matching files
input_directory = "../plots"
pattern = os.path.join(input_directory, "Vx-nAtom130304-Z5.9894Fx-by-Fy-*.pdf")

# Get list of files matching the pattern
input_files = sorted(glob.glob(pattern))

# Define output file
output_file = os.path.join(input_directory, "Vx-nAtom130304-Z5.9894-AllFx-by-Fy.pdf")

# Merge the PDFs
merge_pdfs(input_files, output_file)

