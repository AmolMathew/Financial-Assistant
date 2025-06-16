import os
import concurrent.futures
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict

def worker_initializer():
    global global_converter
    global_converter = PdfConverter(artifact_dict=create_model_dict())

def process_pdf(pdf_path, output_dir):
    global global_converter
    try:
        rendered = global_converter(pdf_path)
        markdown_text = rendered.markdown
        filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".md"
        output_file = os.path.join(output_dir, filename)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_text)
        return f"Processed {pdf_path} successfully."
    except Exception as e:
        return f"Error processing {pdf_path}: {e}"

def convert_pdf_to_md(pdf_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    with concurrent.futures.ProcessPoolExecutor(
            max_workers=1, initializer=worker_initializer
    ) as executor:
        future = executor.submit(process_pdf, pdf_path, output_dir)
        print(future.result())
