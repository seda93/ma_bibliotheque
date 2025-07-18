from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image_to_bucket(file, image_name):
    if file is None:
        return None

    try:
        response = supabase.storage.from_("livres").upload(
            path=image_name,
            file=file,
            file_options={"content-type": "image/jpeg"},
            upsert=True,
        )
        if response.get("error"):
            return None
        
        url = supabase.storage.from_("livres").get_public_url(image_name)
        return url
    except Exception as e:
        print("Erreur Supabase upload:", e)
        return None
