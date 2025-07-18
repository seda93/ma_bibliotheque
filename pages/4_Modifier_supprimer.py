import streamlit as st
from sqlalchemy import text
from PIL import Image
import os

from backend.database import get_sqlalchemy_engine
from backend.supabase_client import upload_image_to_bucket

st.title("🛠️ Modifier ou supprimer un livre")

engine = get_sqlalchemy_engine()

def get_livres_options():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, titre, auteurs FROM livres ORDER BY titre"))
        return list(result.mappings().all())

def get_livre_par_id(livre_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres WHERE id = :id"), {"id": livre_id})
        return result.mappings().first()

def update_livre(livre_id, data):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE livres SET
                titre = :titre,
                auteurs = :auteurs,
                annee = :annee,
                editeur = :editeur,
                genre = :genre,
                langue = :langue,
                collection = :collection,
                emplacement = :emplacement,
                resume = :resume,
                isbn = :isbn,
                serie = :serie,
                image = :image
            WHERE id = :id
        """), {**data, "id": livre_id})

def delete_livre(livre_id):
    with engine.begin() as conn:
        conn.execute(text("DELETE FROM livres WHERE id = :id"), {"id": livre_id})

# Liste déroulante avec recherche
livres = get_livres_options()
if not livres:
    st.info("Aucun livre disponible.")
    st.stop()

options = [f"{livre['titre']} ({livre['auteurs']})" for livre in livres]
option_map = {f"{livre['titre']} ({livre['auteurs']})": livre["id"] for livre in livres}
selected_label = st.selectbox("📚 Sélectionner un livre à modifier", options)
livre_id = option_map[selected_label]
livre = get_livre_par_id(livre_id)

if livre:
    with st.form("modifier_livre"):
        titre = st.text_input("Titre", livre["titre"])
        auteurs = st.text_input("Auteur(s)", livre["auteurs"])
        annee = st.text_input("Année", livre["annee"] or "")
        editeur = st.text_input("Éditeur", livre["editeur"] or "")
        genre = st.text_input("Genre", livre["genre"] or "")
        langue = st.text_input("Langue", livre["langue"] or "")
        collection = st.text_input("Collection", livre["collection"] or "")
        emplacement = st.text_input("Emplacement", livre["emplacement"] or "")
        resume = st.text_area("Résumé", livre["resume"] or "")
        isbn = st.text_input("ISBN", livre["isbn"] or "", key="isbn_modif")
        serie = st.text_input("Série", livre["serie"] or "")

        # Afficher image actuelle
        st.markdown("**Image actuelle :**")
        if livre["image"]:
            st.image(livre["image"], width=150)

        nouvelle_image = st.file_uploader("📷 Nouvelle image de couverture (optionnel)", type=["jpg", "jpeg", "png"])
        image_a_sauver = livre["image"]

        if nouvelle_image is not None:
            uploaded_url = upload_image_to_bucket(nouvelle_image, nouvelle_image.name)
            if uploaded_url:
                image_a_sauver = uploaded_url
            else:
                st.error("❌ L’image n’a pas pu être envoyée.")

        submit = st.form_submit_button("💾 Enregistrer les modifications")
        if submit:
            update_livre(livre_id, {
                "titre": titre,
                "auteurs": auteurs,
                "annee": annee,
                "editeur": editeur,
                "genre": genre,
                "langue": langue,
                "collection": collection,
                "emplacement": emplacement,
                "resume": resume,
                "isbn": isbn,
                "serie": serie,
                "image": image_a_sauver
            })
            st.success("✅ Livre mis à jour avec succès.")

# Suppression
st.markdown("---")
st.warning("⚠️ Cette action supprimera le livre définitivement.")
if st.button("🗑️ Supprimer ce livre"):
    delete_livre(livre_id)
    st.success("✅ Livre supprimé.")
    st.rerun()
