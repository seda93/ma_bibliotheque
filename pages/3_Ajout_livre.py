import streamlit as st
from backend.isbn_lookup import fetch_book_info
from backend.supabase_client import upload_image_to_bucket
from backend.database import get_sqlalchemy_engine
from sqlalchemy import text
import os

st.title("➕ Ajouter un livre")

engine = get_sqlalchemy_engine()

isbn = st.text_input("Entrer un ISBN :")
infos = {}

if isbn and st.button("🔍 Chercher les infos"):
    infos = fetch_book_info(isbn)
    if not infos:
        st.warning("Aucune information trouvée pour cet ISBN.")

if infos or isbn:
    with st.form("form_ajout"):
        titre = st.text_input("Titre", value=infos.get("titre", ""), key="titre")
        auteurs = st.text_input("Auteur(s)", value=infos.get("auteurs", ""), key="auteurs")
        serie = st.text_input("Série", value=infos.get("serie", ""), key="serie")
        annee = st.text_input("Année", value=infos.get("annee", ""), key="annee")
        genre = st.text_input("Genre", value=infos.get("genre", ""), key="genre")
        langue = st.text_input("Langue", value=infos.get("langue", ""), key="langue")
        editeur = st.text_input("Éditeur", value=infos.get("editeur", ""), key="editeur")
        collection = st.text_input("Collection", value=infos.get("collection", ""), key="collection")
        emplacement = st.text_input("Emplacement", value=infos.get("emplacement", ""), key="emplacement")
        resume = st.text_area("Résumé", value=infos.get("resume", ""), key="resume")
        isbn_final = st.text_input("ISBN", value=infos.get("isbn", isbn), key="isbn")
        image = st.file_uploader("📷 Image de couverture", type=["jpg", "jpeg", "png"])

        submit = st.form_submit_button("📚 Ajouter")

        if submit:
            # Vérifier doublon
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM livres WHERE isbn = :isbn"), {"isbn": isbn_final})
                count = result.scalar()

            if count > 0:
                st.error("⚠️ Ce livre existe déjà dans la base de données.")
            else:
                image_url = None
                if image:
                    image_url = upload_image_to_bucket(image, image.name)
                    if not image_url:
                        st.error("❌ Erreur lors de l’envoi de l’image.")
                        image_url = ""

                with engine.begin() as conn:
                    conn.execute(text("""
                        INSERT INTO livres (titre, auteurs, serie, annee, genre, langue, isbn, editeur, collection, emplacement, resume, image)
                        VALUES (:titre, :auteurs, :serie, :annee, :genre, :langue, :isbn, :editeur, :collection, :emplacement, :resume, :image)
                    """), {
                        "titre": titre,
                        "auteurs": auteurs,
                        "serie": serie,
                        "annee": annee,
                        "genre": genre,
                        "langue": langue,
                        "isbn": isbn_final,
                        "editeur": editeur,
                        "collection": collection,
                        "emplacement": emplacement,
                        "resume": resume,
                        "image": image_url or ""
                    })
                st.success("✅ Livre ajouté avec succès.")
                st.rerun()
