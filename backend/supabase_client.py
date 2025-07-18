from supabase import create_client
import streamlit as st

# Utilisation directe de st.secrets (pour Streamlit Cloud ou secrets.toml local)
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image_to_bucket(image_file, image_name, bucket="images"):
    try:
        supabase.storage.from_(bucket).upload(
            path=image_name,
            file=image_file,
            file_options={"content-type": "image/jpeg"}
        )
        public_url = supabase.storage.from_(bucket).get_public_url(image_name)
        return public_url
    except Exception as e:
        print(f"Erreur d'upload : {e}")
        return None
