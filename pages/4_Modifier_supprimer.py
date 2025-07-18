import streamlit as st
from backend.database import get_sqlalchemy_engine
from backend.supabase_client import upload_image_to_bucket
from sqlalchemy import text
from PIL import Image
import os

st.title("✏️ Modifier un livre")

engine = get_sqlalchemy_engine()

def get_livres_options():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, titre, auteurs FROM livres ORDER BY titre"))
        return [dict(r) for r in result.fetchall()]

def get_livre_par_id(livre_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres WHERE id = :id"), {"id": livre_id})
        return result.mappings().fetchone()

def update_livre(livre_id, data):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE livres SET
                titre = :titre, auteurs = :auteurs, serie = :serie,
                annee = :annee, genre = :genre, langue = :langue,
                isbn = :isbn, editeur = :editeur, collection = :collection,
                emplacement = :emplacement, resume = :resume, image = :image
            WHERE id = :id
        """), {**data, "id": livre_id})

livres = get_livres_options()
if not livres:
    st.info("Aucun livre disponible.")
    st.stop()

options = [f"{l['titre']} ({l['auteurs']})" for l in livres]
selected = st.selectbox("Choisir un livre à modifier :", options)
livre_id = livres[options.index(selected)]["id"]
livre = get_livre_par_id(livre_id)

if livre:
    with st.form("modifier_livre"):
        titre = st.text_input("Titre", livre["titre"])
        auteurs = st.text_input("Auteur(s)", livre["auteurs"])
        serie = st.text_input("Série", livre["serie"])
        annee = st.text_input("Année", livre["annee"])
        genre = st.text_input("Genre", livre["genre"])
        langue = st.text_input("Langue", livre["langue"])
        isbn = st.text_input("ISBN", livre["isbn"])
        editeur = st.text_input("Éditeur", livre["editeur"])
        collection = st.text_input("Collection", livre["collection"])
        emplacement = st.text_input("Emplacement", livre["emplacement"])
        resume = st.text_area("Résumé", livre["resume"])
        ancienne_image = livre["image"]

        nouvelle_image = st.file_uploader("📷 Nouvelle image de couverture", type=["jpg", "png"])
        if nouvelle_image:
            uploaded_url = upload_image_to_bucket(nouvelle_image, nouvelle_image.name)
            if uploaded_url:
                image_url = uploaded_url
            else:
                st.error("❌ L’image n’a pas pu être envoyée.")
                image_url = ancienne_image
        else:
            image_url = ancienne_image

        if st.form_submit_button("💾 Sauvegarder"):
            update_livre(livre_id, {
                "titre": titre,
                "auteurs": auteurs,
                "serie": serie,
                "annee": annee,
                "genre": genre,
                "langue": langue,
                "isbn": isbn,
                "editeur": editeur,
                "collection": collection,
                "emplacement": emplacement,
                "resume": resume,
                "image": image_url
            })
            st.success("📚 Livre mis à jour avec succès.")
