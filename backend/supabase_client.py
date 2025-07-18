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

        # Upload de l’image
        response = supabase.storage.from_("livres").upload(
            path=image_name,
            file=file,
            file_options={"content-type": "image/jpeg"}
        )

        if hasattr(response, "error") and response.error is not None:
            st.error(f"❌ Erreur Supabase (upload): {response.error.message}")
            return None

        # Obtenir l’URL publique de l’image
        public_url_response = supabase.storage.from_("livres").get_public_url(image_name)

        if hasattr(public_url_response, 'public_url'):
            return public_url_response.public_url
        elif isinstance(public_url_response, dict) and "publicURL" in public_url_response:
            return public_url_response["publicURL"]
        elif isinstance(public_url_response, str):
            return public_url_response
        else:
            st.error("❌ Erreur : URL publique non récupérée.")
            return None

    except Exception as e:
        st.error(f"❌ Erreur Supabase upload : {e}")
        return None
