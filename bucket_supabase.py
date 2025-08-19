from supabase import create_client, Client

url: str = "https://rmhwyhdjcciyckrajzmq.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJtaHd5aGRqY2NpeWNrcmFqem1xIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDcyMzE2NCwiZXhwIjoyMDY2Mjk5MTY0fQ.l7yGzZWSl7ZIVTd0DC3HWAlzplQuTm5pi0MUd5x0v4Y"

supabase: Client = create_client(url, key)

def upload_markdown_to_bucket(bucket_name: str, file_name: str, markdown_content: str) -> str:
    """
    Faz upload de conteúdo Markdown diretamente para o Supabase Storage (sem salvar local).
    
    Args:
        bucket_name (str): Nome do bucket.
        file_name (str): Nome do arquivo (ex: "documento.md").
        markdown_content (str): Conteúdo do arquivo em markdown.
    
    Returns:
        str: URL pública do arquivo no bucket.
    """
    try:
        supabase.storage.from_(bucket_name).upload(
            file_name, 
            markdown_content.encode("utf-8"),  # converte string para bytes
        )
        
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        print(f"✅ Upload concluído: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Erro no upload: {e}")
        return None