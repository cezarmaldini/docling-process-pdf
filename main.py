import os
from docling.document_converter import DocumentConverter

os.environ["HF_HOME"] = "C:/meus_modelos/huggingface"

# 📄 Caminho relativo ao arquivo PDF
source = 'files/proposta_02.pdf'

# 🔄 Converte o documento
converter = DocumentConverter()
result = converter.convert(source)

# 📝 Exporta para Markdown
print(result.document.export_to_markdown())