import os
from docling.document_converter import DocumentConverter

PDF_PATH = "ingestion/teste.pdf"

def convert_pdf_to_document(pdf_path):
    """
    Convert a PDF file to a structured document format.
    """
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()


document = convert_pdf_to_document(PDF_PATH)

print(document)

with open("document.md", "w", encoding="utf-8") as arquivo:
    arquivo.write(document)

print("Arquivo Markdown salvo com sucesso!")