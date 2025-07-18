from supabase import create_client
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def upload_image_to_bucket(file, image_name):
    if file is None:
        return None

    try:
        # Supprimer l'image si elle existe déjà
        try:
            supabase.storage.from_("livres").remove(image_name)
        except Exception as e:
            print("Aucune image à supprimer ou erreur ignorée :", e)

        # Upload image
        response = supabase.storage.from_("livres").upload(
            path=image_name,
            file=file,
            file_options={"content-type": "image/jpeg"}
        )

        if isinstance(response, dict) and response.get("error"):
            st.error(f"❌ Erreur Supabase (upload): {response['error']}")
            return None

        # Obtenir l’URL publique de l’image
        public_url = supabase.storage.from_("livres").get_public_url(image_name)
        if hasattr(public_url, 'get'):
            return public_url.get('publicURL')
        return public_url  # au cas où c’est une string directement

    except Exception as e:
        st.error(f"❌ Erreur Supabase upload : {e}")
        return None
