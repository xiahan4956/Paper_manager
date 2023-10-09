import datetime
import os

import PyPDF2
import requests
import wget


def dose_have_new_pdf(data_path, initial_files):
    "Continuously check if there are new pdf files in a directory."
    start_time = datetime.datetime.now()

    while True:
        current_files = set([f for f in os.listdir(data_path) if f.endswith('.pdf')])
        new_files = current_files - initial_files

        if new_files:
            print(f"New PDF files found: {new_files}")
            return new_files

        # Check for 20s, wait for PDF to download
        if (datetime.datetime.now() - start_time).seconds > 10:
            print("Timeout waiting, no new PDF files found.")
            return None


def read_pdf(new_files, data_path):
    for new_file in new_files:
        with open(os.path.join(data_path, new_file), "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text()

    return content


def read_pdf_by_url(url, data_path):
    try:
        print("Starting to download PDF using wget")
        
        print("Download URL:" + url)
        save_path = os.path.join(data_path, "temp.pdf")
        wget.download(url, out=save_path, bar=wget.bar_adaptive)
            
        with open(save_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            content = ""
            for page in pdf_reader.pages:
                content += page.extract_text()

        # Clear all files in data_path
        for f in os.listdir(data_path):
            os.remove(os.path.join(data_path, f))
        
    except Exception as e:
        print("Failed to download PDF using wget:", e)
        content = ""

    return content
