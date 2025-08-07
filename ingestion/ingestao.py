# ================================================================
# Importar bibliotecas
import os
import requests
from dotenv import load_dotenv

load_dotenv()


from docling.document_converter import DocumentConverter

# ================================================================
# Obter Access Token Microsoft Graph
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

token_url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

data = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://graph.microsoft.com/.default'
}

response = requests.post(token_url, data=data)
access_token = response.json().get('access_token')

print("Access token:", access_token)

# ==============================================================
# Fazer download dos arquivos do Sharepoint
site_name = "BDTeste"
folder_path = "teste_markdown"

site_resp = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/taticogestao.sharepoint.com:/sites/{site_name}",
    headers={"Authorization": f"Bearer {access_token}"}
)
site_id = site_resp.json().get("id")
print("Site ID:", site_id)

drive_resp = requests.get(
    f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive",
    headers={"Authorization": f"Bearer {access_token}"}
)
drive_id = drive_resp.json().get("id")
print("Drive ID:", drive_id)

# Obter lista de arquivos na pasta teste_markdown dentro do drive
files_resp = requests.get(
    f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder_path}:/children",
    headers={"Authorization": f"Bearer {access_token}"}
)

if files_resp.status_code == 200:
    files = files_resp.json()
    for file in files.get('value', []):
        print(f"Nome: {file['name']}")
        print(f"Link: {file['webUrl']}")
        print("-" * 40)
else:
    print(f"Erro ao listar arquivos: {files_resp.status_code} - {files_resp.text}")

# Cria a pasta downloads local (se não existir)
local_folder = "downloads"
os.makedirs(local_folder, exist_ok=True)

for file in files.get('value', []):
    file_name = file['name']
    download_url = file.get('@microsoft.graph.downloadUrl')
    if not download_url:
        print(f"Sem link de download para {file_name}")
        continue

    print(f"Baixando {file_name}...")

    # Requisição GET para baixar o arquivo
    file_resp = requests.get(download_url)
    if file_resp.status_code == 200:
        # Salvar arquivo localmente
        local_path = os.path.join(local_folder, file_name)
        with open(local_path, 'wb') as f:
            f.write(file_resp.content)
        print(f"Salvo em: {local_path}")
    else:
        print(f"Erro ao baixar {file_name}: {file_resp.status_code}")


# ========================================================================
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