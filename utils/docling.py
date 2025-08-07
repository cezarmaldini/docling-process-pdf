import os
from docling.document_converter import DocumentConverter

def convert_pdf_to_markdown(pdf_path):
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()

def process_pdfs_to_markdown(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"Processando: {filename}")

            try:
                markdown = convert_pdf_to_markdown(pdf_path)
                markdown_filename = os.path.splitext(filename)[0] + ".md"
                output_path = os.path.join(output_folder, markdown_filename)
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(markdown)
                print(f"Arquivo Markdown salvo: {markdown_filename}")
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")