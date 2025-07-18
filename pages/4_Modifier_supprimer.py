import streamlit as st
from backend.supabase_client import upload_image_to_bucket
from backend.database import get_sqlalchemy_engine
from sqlalchemy import text
from PIL import Image
import os

# --- STYLES GLOBAUX PASTEL ---
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

st.title("✏️ Modifier ou supprimer un livre")

engine = get_sqlalchemy_engine()

def get_livres_options():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, titre, auteurs FROM livres"))
        return [{"id": r[0], "label": f"{r[1]} – {r[2] or 'Auteur inconnu'}"} for r in result]

def get_livre_par_id(livre_id):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres WHERE id = :id"), {"id": livre_id})
        row = result.fetchone()
        return dict(row._mapping) if row else None

def update_livre(livre_id, data):
    with engine.connect() as conn:
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
                image = :image,
                serie = :serie
            WHERE id = :id
        """), {**data, "id": livre_id})

def supprimer_livre(livre_id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM livres WHERE id = :id"), {"id": livre_id})

# --- SÉLECTION DU LIVRE ---
livres = get_livres_options()
if not livres:
    st.info("Aucun livre disponible.")
    st.stop()

selected_label = st.selectbox("Choisissez un livre à modifier :", [l["label"] for l in livres])
livre_id = [l["id"] for l in livres if l["label"] == selected_label][0]
livre = get_livre_par_id(livre_id)

# --- ÉTAT DE SUPPRESSION ---
if "supprimer_en_cours" not in st.session_state:
    st.session_state.supprimer_en_cours = None

if livre:
    with st.form("modifier_livre"):
        titre = st.text_input("Titre", livre["titre"], key="titre")
        auteurs = st.text_input("Auteur(s)", livre["auteurs"] or "", key="auteurs")
        annee = st.text_input("Année", livre["annee"] or "", key="annee")
        editeur = st.text_input("Éditeur", livre["editeur"] or "", key="editeur")
        genre = st.text_input("Genre", livre["genre"] or "", key="genre")
        langue = st.text_input("Langue", livre["langue"] or "", key="langue")
        collection = st.text_input("Collection", livre["collection"] or "", key="collection")
        emplacement = st.text_input("Emplacement", livre["emplacement"] or "", key="emplacement")
        resume = st.text_area("Résumé", livre["resume"] or "", key="resume")
        serie = st.text_input("Série", livre["serie"] or "", key="serie")
        isbn = st.text_input("ISBN", livre["isbn"] or "", key="isbn")

        st.markdown("**Image actuelle :**")
        if livre["image"]:
            try:
                if livre["image"].startswith("http"):
                    st.image(livre["image"], width=150)
                else:
                    with open(livre["image"], "rb") as img_file:
                        st.image(img_file.read(), width=150)
            except FileNotFoundError:
                st.warning("📁 Image introuvable sur le serveur.")

        nouvelle_image = st.file_uploader("📷 Nouvelle image de couverture", type=["jpg", "jpeg", "png"])
        image_a_sauver = livre["image"]

        if nouvelle_image:
            try:
                image_bytes = nouvelle_image.read()
                uploaded_url = upload_image_to_bucket(image_bytes, nouvelle_image.name)
                if uploaded_url:
                    image_a_sauver = uploaded_url
                    st.success("✅ Image mise à jour sur Supabase.")
                else:
                    st.error("❌ L’image n’a pas pu être envoyée.")
            except Exception as e:
                st.error(f"Erreur envoi image : {e}")

        col1, col2 = st.columns(2)
        with col1:
            submitted = st.form_submit_button("💾 Enregistrer les modifications")
        with col2:
            demande_suppression = st.form_submit_button("🗑️ Supprimer ce livre")

        if submitted:
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
                "image": image_a_sauver,
                "serie": serie,
            })
            st.success("✅ Livre modifié avec succès.")
            st.rerun()

        if demande_suppression:
            st.session_state.supprimer_en_cours = livre_id
            st.warning(f"⚠️ Voulez-vous vraiment supprimer **{livre['titre']}** ?")
            col_conf, col_annul = st.columns(2)
            with col_conf:
                if st.button("✅ Oui, supprimer définitivement"):
                    supprimer_livre(livre_id)
                    st.success("🗑️ Livre supprimé.")
                    st.session_state.supprimer_en_cours = None
                    st.rerun()
            with col_annul:
                if st.button("❌ Annuler"):
                    st.session_state.supprimer_en_cours = None
                    st.info("Suppression annulée.")
