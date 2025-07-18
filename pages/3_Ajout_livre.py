import streamlit as st
from backend.isbn_lookup import fetch_book_info
from backend.database import get_sqlalchemy_engine
from backend.supabase_client import upload_image_to_bucket
from sqlalchemy import text
import os

# --- STYLES PASTEL ---
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

st.title("➕ Ajouter un livre")

engine = get_sqlalchemy_engine()

with st.form("ajout_livre"):
    isbn = st.text_input("ISBN")
    fetch = st.form_submit_button("🔍 Chercher les infos")

infos = fetch_book_info(isbn) if fetch and isbn else {}

with st.form("form_ajout"):
    titre = st.text_input("Titre", infos.get("titre", ""))
    auteurs = st.text_input("Auteur(s)", infos.get("auteurs", ""))
    annee = st.text_input("Année", infos.get("annee", ""))
    editeur = st.text_input("Éditeur", infos.get("editeur", ""))
    genre = st.text_input("Genre", infos.get("genre", ""))
    langue = st.text_input("Langue", infos.get("langue", ""))
    collection = st.text_input("Collection", infos.get("collection", ""))
    emplacement = st.text_input("Emplacement", infos.get("emplacement", ""))
    resume = st.text_area("Résumé", infos.get("resume", ""))
    serie = st.text_input("Série", infos.get("serie", ""))
    isbn_final = st.text_input("ISBN", infos.get("isbn", isbn), key="isbn_final")

    image_file = st.file_uploader("📷 Image de couverture", type=["jpg", "jpeg", "png"])
    image_url = None

    if image_file:
        try:
            image_bytes = image_file.read()
            uploaded_url = upload_image_to_bucket(image_bytes, image_file.name)
            if uploaded_url:
                image_url = uploaded_url
                st.success("✅ Image téléchargée avec succès.")
            else:
                st.error("❌ L’image n’a pas pu être envoyée.")
        except Exception as e:
            st.error(f"Erreur envoi image : {e}")

    submitted = st.form_submit_button("💾 Ajouter le livre")

    if submitted:
        try:
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO livres 
                    (titre, auteurs, annee, editeur, genre, langue, collection, emplacement, resume, isbn, image, serie)
                    VALUES 
                    (:titre, :auteurs, :annee, :editeur, :genre, :langue, :collection, :emplacement, :resume, :isbn, :image, :serie)
                """), {
                    "titre": titre or None,
                    "auteurs": auteurs or None,
                    "annee": annee or None,
                    "editeur": editeur or None,
                    "genre": genre or None,
                    "langue": langue or None,
                    "collection": collection or None,
                    "emplacement": emplacement or None,
                    "resume": resume or None,
                    "isbn": isbn_final or None,
                    "image": image_url or None,
                    "serie": serie or None,
                })
            st.success("📚 Livre ajouté avec succès !")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erreur lors de l’ajout : {e}")
