import os
from docling_teste import convert_pdf_to_markdown
from bucket_supabase import upload_markdown_to_bucket

if __name__ == "__main__":
    input_folder = "downloads"
    bucket_name = "teste"

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".pdf"):
            pdf_path = os.path.join(input_folder, filename)
            print(f"📄 Processando: {filename}")

            try:
                # Converte PDF -> Markdown (em memória)
                markdown = convert_pdf_to_markdown(pdf_path)

                # Define o nome do arquivo no bucket
                md_filename = os.path.splitext(filename)[0] + ".md"

                # Faz upload direto para o Supabase
                upload_markdown_to_bucket(bucket_name, md_filename, markdown)

            except Exception as e:
                print(f"⚠️ Erro ao processar {filename}: {e}")
