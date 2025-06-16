from downloader.pdf_to_md import convert_pdf_to_md
from multiprocessing import freeze_support

if __name__ == "__main__":
    freeze_support()
    pdf_path = "data/CBI_2021.pdf"
    output_dir = "processed_pdfs"
    convert_pdf_to_md(pdf_path, output_dir)
