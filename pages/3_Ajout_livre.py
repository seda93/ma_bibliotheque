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

IMG_DIR = "data/images"
os.makedirs(IMG_DIR, exist_ok=True)

engine = get_sqlalchemy_engine()

isbn = st.text_input("📖 ISBN (optionnel)", "")
if isbn and st.button("🔍 Chercher infos ISBN"):
    infos = fetch_book_info(isbn)
    if infos:
        st.success("✅ Informations trouvées.")
        st.session_state["infos"] = infos
    else:
        st.warning("❌ Aucune information trouvée.")
        st.session_state["infos"] = {}
elif "infos" not in st.session_state:
    st.session_state["infos"] = {}

infos = st.session_state["infos"]

with st.form("form_ajout"):
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
    image = st.file_uploader("📷 Image de couverture", type=["jpg", "jpeg", "png"])

    submit = st.form_submit_button("💾 Ajouter")

    if submit:
        if not titre:
            st.error("❌ Le titre est obligatoire.")
        else:
            image_url = infos.get("image", "")
            if image:
                try:
                    image_bytes = image.read()
                    image_url_uploaded = upload_image_to_bucket(image_bytes, image.name)
                    if image_url_uploaded:
                        image_url = image_url_uploaded
                        st.success("✅ Image envoyée sur Supabase.")
                    else:
                        st.warning("⚠️ L’image n’a pas pu être uploadée.")
                except Exception as e:
                    st.error(f"Erreur lors de l’upload : {e}")

            # Insertion dans la base PostgreSQL
            insert_query = text("""
                INSERT INTO livres (
                    titre, auteurs, serie, annee, genre, langue, isbn, editeur,
                    collection, emplacement, resume, image
                ) VALUES (
                    :titre, :auteurs, :serie, :annee, :genre, :langue, :isbn,
                    :editeur, :collection, :emplacement, :resume, :image
                )
            """)

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
                "emplacement": emplacement,
                "resume": resume,
                "image": image_url
            }

            try:
                with engine.begin() as conn:
                    conn.execute(insert_query, params)
                st.success("✅ Livre ajouté avec succès.")
                st.session_state["infos"] = {}
            except Exception as e:
                st.error(f"❌ Erreur lors de l'ajout : {e}")
