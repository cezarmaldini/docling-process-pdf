from sharepoint import fetch_files_from_sharepoint
from conversor import convert_pdf_bytes_to_markdown
from bucket_supabase import upload_markdown_to_bucket

def main():
    site_name = "BDTeste"
    folder_path = "PDF"
    bucket_name = "propostas_markdown"

    # Busca PDFs no SharePoint
    pdf_files = fetch_files_from_sharepoint(site_name, folder_path)

    for pdf in pdf_files:
        file_name = pdf["file_name"].replace(".pdf", ".md")
        pdf_bytes = pdf["content"]

        # Converte para Markdown
        markdown_content = convert_pdf_bytes_to_markdown(pdf_bytes)

        # Faz upload para Supabase
        upload_markdown_to_bucket(bucket_name, file_name, markdown_content)

if __name__ == "__main__":
    main()