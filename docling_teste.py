from docling.document_converter import DocumentConverter

def convert_pdf_to_markdown(pdf_path: str) -> str:
    """
    Converte um PDF para Markdown em memória (string).
    """
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()
