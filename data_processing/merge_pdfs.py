from pypdf import PdfWriter
import os

# Get the absolute path of the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

pdf_list = [
    "sample1.pdf",
    "sample2.pdf",
    "sample3.pdf",
    "sample4.pdf",
    "sample5.pdf",
]

output_filename = os.path.join(script_dir, '..', 'policy.pdf')

merger = PdfWriter()
print("Starting PDF merge...")

# Iterate through all the PDFs
for pdf_file in pdf_list:
    # Create the full path to the sample PDF
    full_pdf_path = os.path.join(script_dir, pdf_file)
    if os.path.exists(full_pdf_path):
        print(f"  -> Adding {pdf_file}...")
        merger.append(full_pdf_path)
    else:
        print(f"  -> WARNING: {pdf_file} not found. Skipping.")

# Write out the merged PDF to the main project folder
with open(output_filename, "wb") as fout:
    merger.write(fout)

merger.close()
print(f"\n✅ Successfully merged files into '{os.path.abspath(output_filename)}'!")