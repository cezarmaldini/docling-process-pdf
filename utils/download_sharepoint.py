import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_access_token():
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
    response.raise_for_status()  # Levanta erro se falhar
    access_token = response.json().get('access_token')
    return access_token

def download_files_from_sharepoint(site_name, folder_path, local_folder):
    access_token = get_access_token()
    
    # Obter site ID
    site_resp = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/taticogestao.sharepoint.com:/sites/{site_name}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    site_resp.raise_for_status()
    site_id = site_resp.json().get("id")

    # Obter drive ID
    drive_resp = requests.get(
        f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    drive_resp.raise_for_status()
    drive_id = drive_resp.json().get("id")

    # Obter arquivos na pasta
    files_resp = requests.get(
        f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root:/{folder_path}:/children",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    files_resp.raise_for_status()
    files = files_resp.json()

    os.makedirs(local_folder, exist_ok=True)

    for file in files.get('value', []):
        file_name = file['name']
        download_url = file.get('@microsoft.graph.downloadUrl')
        if not download_url:
            print(f"Sem link de download para {file_name}")
            continue

        print(f"Baixando {file_name}...")
        file_resp = requests.get(download_url)
        if file_resp.status_code == 200:
            local_path = os.path.join(local_folder, file_name)
            with open(local_path, 'wb') as f:
                f.write(file_resp.content)
            print(f"Salvo em: {local_path}")
        else:
            print(f"Erro ao baixar {file_name}: {file_resp.status_code}")

    return local_folder
