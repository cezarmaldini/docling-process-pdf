import io
from docling.document_converter import DocumentConverter, DocumentStream

def convert_pdf_bytes_to_markdown(pdf_bytes: bytes) -> str:
    """
    Converte PDF em bytes para Markdown (sem salvar em disco).
    """
    converter = DocumentConverter()
    stream = io.BytesIO(pdf_bytes)

    # Criar DocumentStream a partir do PDF em memória
    doc_stream = DocumentStream(stream=stream, file_type="pdf", name="temp.pdf")

    result = converter.convert(doc_stream)
    return result.document.export_to_markdown()
