from utils.download_sharepoint import download_files_from_sharepoint
from utils.docling import process_pdfs_to_markdown

def main():
    site_name = "BDTeste"
    folder_path = "teste_markdown"
    downloads_folder = "downloads"
    markdown_output_folder = "output"

    print("Iniciando download dos arquivos do SharePoint...")
    download_files_from_sharepoint(site_name, folder_path, downloads_folder)

    print("Iniciando processamento dos PDFs para Markdown...")
    process_pdfs_to_markdown(downloads_folder, markdown_output_folder)

    print("Processo finalizado.")

if __name__ == "__main__":
    main()