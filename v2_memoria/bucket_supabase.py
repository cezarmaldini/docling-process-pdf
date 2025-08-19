import re
import unicodedata
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_API_KEY = os.getenv('SUPABASE_API_KEY')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

def sanitize_filename(filename: str) -> str:
    # Remove acentos
    nfkd = unicodedata.normalize("NFKD", filename)
    no_accent = "".join([c for c in nfkd if not unicodedata.combining(c)])

    # Substitui caracteres inválidos por "_"
    sanitized = re.sub(r'[^a-zA-Z0-9._\- ()]', "_", no_accent)

    return sanitized

def upload_markdown_to_bucket(bucket_name: str, file_name: str, markdown_content: str) -> str:
    try:
        file = sanitize_filename(file_name)

        today = datetime.today().strftime("%Y%m%d")

        folder = f"propostas_{today}"

        path = f"{folder}/{file}"

        supabase.storage.from_(bucket_name).upload(
            path, 
            markdown_content.encode("utf-8")
        )
        
        public_url = supabase.storage.from_(bucket_name).get_public_url(file)
        print(f"✅ Upload concluído: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return None