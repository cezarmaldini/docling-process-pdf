from docling.document_converter import DocumentConverter

source = "file:///C:/Users/viva_/workspace/cezarmaldini/docling-process-pdf/files/proposta.pdf"
converter = DocumentConverter()
result = converter.convert(source)
print(result.document.export_to_markdown())