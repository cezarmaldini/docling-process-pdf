from docling.document_converter import DocumentConverter

source = 'scratch/2025.07 - RelatorioMensal-1.png'

converter = DocumentConverter()
doc = converter.convert(source).document

print(doc.export_to_markdown())