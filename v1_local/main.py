from utils.download_sharepoint import download_files_from_sharepoint
from utils.docling import process_pdfs_to_markdown

def main():
    site_name = "BDTeste"
    folder_path = "teste_markdown"
    markdown_output_folder = "output"
    download = "downloads"

    print("Iniciando download dos arquivos do SharePoint...")
    pdf_list = download_files_from_sharepoint(site_name, folder_path, download)

    print("Iniciando processamento dos PDFs para Markdown...")
    process_pdfs_to_markdown(pdf_list, markdown_output_folder)

    print("Processo finalizado.")

if __name__ == "__main__":
    main()