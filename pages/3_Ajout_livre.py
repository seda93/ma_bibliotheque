st.markdown("""
<style>
body {
    background-color: #fdf6f0;
}
section.main > div {
    background-color: #ffffffdd;
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0px 0px 10px rgba(200, 200, 200, 0.3);
}
h1, h2, h3 {
    color: #6a5acd;
}
</style>
""", unsafe_allow_html=True)

import streamlit as st
from backend.isbn_lookup import fetch_book_info
from backend.database import get_sqlalchemy_engine
from backend.supabase_client import upload_image_to_bucket
import os
from sqlalchemy import text
from PIL import Image

IMG_DIR = "data/images"

st.title("➕ Ajouter un livre")

engine = get_sqlalchemy_engine()

# Créer dossier image si absent
os.makedirs(IMG_DIR, exist_ok=True)

with st.form("ajout_form"):
    isbn = st.text_input("ISBN")
    if isbn and st.form_submit_button("🔍 Chercher infos ISBN"):
        infos = fetch_book_info(isbn)
        if infos:
            st.session_state["infos"] = infos
        else:
            st.warning("Aucune information trouvée.")
    else:
        st.session_state["infos"] = {}

    infos = st.session_state.get("infos", {})

    titre = st.text_input("Titre", infos.get("titre", ""))
    auteurs = st.text_input("Auteur(s)", infos.get("auteurs", ""))
    serie = st.text_input("Série", infos.get("serie", ""))
    annee = st.text_input("Année", infos.get("annee", ""))
    genre = st.text_input("Genre", infos.get("genre", ""))
    langue = st.text_input("Langue", infos.get("langue", ""))
    editeur = st.text_input("Éditeur", infos.get("editeur", ""))
    collection = st.text_input("Collection", infos.get("collection", ""))
    emplacement = st.text_input("Emplacement", infos.get("emplacement", ""))
    resume = st.text_area("Résumé", infos.get("resume", ""))
    isbn_final = st.text_input("ISBN", infos.get("isbn", isbn), key="isbn_final")
    image_url = infos.get("image", "")
    image = st.file_uploader("📷 Image de couverture", type=["jpg", "jpeg", "png"])

    if st.form_submit_button("💾 Ajouter le livre"):
        if not titre:
            st.error("Le titre est obligatoire.")
        else:
            image_path_or_url = image_url

            if image:
                image_bytes = image.read()
                image_path_or_url = upload_image_to_bucket(image.name, image_bytes)
                st.success("Image envoyée dans Supabase Storage.")

            insert_sql = """
                INSERT INTO livres (titre, auteurs, serie, annee, genre, langue, isbn, editeur, collection, resume, emplacement, image)
                VALUES (:titre, :auteurs, :serie, :annee, :genre, :langue, :isbn, :editeur, :collection, :resume, :emplacement, :image)
            """
            params = {
                "titre": titre,
                "auteurs": auteurs,
                "serie": serie,
                "annee": annee,
                "genre": genre,
                "langue": langue,
                "isbn": isbn_final,
                "editeur": editeur,
                "collection": collection,
                "resume": resume,
                "emplacement": emplacement,
                "image": image_path_or_url
            }

            try:
                with engine.begin() as conn:
                    conn.execute(text(insert_sql), params)
                st.success("✅ Livre ajouté avec succès.")
                st.session_state["infos"] = {}
            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
                