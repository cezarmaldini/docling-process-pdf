import os
from docling.document_converter import DocumentConverter

# Caminho da pasta onde estão os arquivos PDF
FILES_DIR = os.path.join("downloads")
OUTPUT_DIR = os.path.join("ingestion", "files_markdown")

# Cria a pasta de saída, se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_pdf_to_document(pdf_path):
    """
    Convert a PDF file to a structured document format.
    """
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()

# Processa todos os arquivos PDF da pasta
for filename in os.listdir(FILES_DIR):
    if filename.lower().endswith(".pdf"):
        PDF_PATH = os.path.join(FILES_DIR, filename)
        print(f"Processando: {filename}")
        
        try:
            document = convert_pdf_to_document(PDF_PATH)
            markdown_filename = os.path.splitext(filename)[0] + ".md"
            output_path = os.path.join(OUTPUT_DIR, markdown_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(document)
            
            print(f"Arquivo Markdown salvo com sucesso: {markdown_filename}")
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")