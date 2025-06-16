A modular Python toolkit for financial data extraction, document conversion, and Retrieval-Augmented Generation (RAG) analysis.

This project enables:

Automated downloading of BSE annual reports

Extraction of structured data (text, tables, charts) from PDFs to Markdown

Advanced financial Q&A using RAG (vector search + LLM) with a Gradio web UI






Table of Contents

Features

Project Structure

Installation

Configuration

Usage

  1. BSE Annual Report Downloader

  2. PDF Extraction to Markdown

  3. Financial RAG Assistant (UI)

Extraction Module Details



Features

BSE Annual Report Downloader: Scrapes and downloads annual reports from the BSE website.

PDF Extraction: Extracts text, tables, and chart data from PDFs, outputting clean Markdown for downstream analytics or RAG ingestion.

RAG Assistant: Combines vector search (Qdrant), LLM (Gemini), and financial APIs for context-aware Q&A, accessible via Gradio UI.

Project Structure

financial-assistant/

├── config/

│   └── settings.py                  # Centralized configuration

├── downloader/

│   ├── bse_downloader.py            # BSE annual report scraper

│   └── pdf_to_md.py                 # PDF extraction to Markdown

├── rag_core/

│   ├── genai.py                     # LLM API calls (Gemini)

│   ├── qdrant.py                    # Vector search logic

│   ├── embeddings.py                # Embedding generation

│   ├── fmp_api.py                   # Financial Modeling Prep API

│   └── pipeline.py                  # RAG workflow

├── ui/

│   └── gradio_app.py                # Gradio web interface

├── scripts/

│   ├── run_bse_downloader.py

│   ├── run_pdf_to_md.py

│   └── run_rag_assistant.py

├── requirements.txt

├── README.md

└── .gitignore



Installation

Clone the repository:

bash
git clone https://github.com/YOURUSERNAME/financial-assistant.git
cd financial-assistant
Install dependencies:

bash
pip install -r requirements.txt
Configuration
Edit config/settings.py to set your API keys, file paths, and other parameters.

Place your input files (e.g., Equity.csv, PDFs) in the appropriate folders as described below.

Usage
1. BSE Annual Report Downloader
Download annual reports from BSE:

bash
python scripts/run_bse_downloader.py
Output: PDFs saved in the downloads/ directory.

2. PDF Extraction to Markdown
Extracts text, tables, and charts from all PDFs in a folder and outputs Markdown files:

bash
python scripts/run_pdf_to_md.py
Input: Place PDFs in UNPROCESSED_2022/

Output: Markdown files in PROCESSED_2022_FINAL/

Log: Conversion log in the project root

3. Financial RAG Assistant (UI)
Launch the Gradio web interface for financial Q&A:

bash
python scripts/run_rag_assistant.py
Access the UI in your browser at the displayed local URL.

Extraction Module Details
The PDF extraction module (downloader/pdf_to_md.py) uses pdfplumber, camelot, and PyMuPDF to:

Extract and clean text from each page

Extract tables (using both lattice and stream methods)

Detect and convert chart/figure references into Markdown tables

Post-process and format the output for downstream analytics and RAG ingestion

This approach follows best practices for PDF data extraction in RAG and analytics pipelines.

