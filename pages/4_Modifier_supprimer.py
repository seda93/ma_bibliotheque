import streamlit as st
from backend.supabase_client import upload_image_to_bucket
from backend.database import get_sqlalchemy_engine
from sqlalchemy import text
from PIL import Image
import os

# --- STYLE PASTEL ---
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
    engine = get_sqlalchemy_engine()
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM livres WHERE id = :id"), {"id": livre_id})
        conn.commit()

# --- CHOIX DU LIVRE ---
livres = get_livres_options()
if not livres:
    st.info("Aucun livre disponible.")
    st.stop()

selected_label = st.selectbox("Choisissez un livre à modifier :", [l["label"] for l in livres])
livre_id = [l["id"] for l in livres if l["label"] == selected_label][0]
livre = get_livre_par_id(livre_id)

# --- MODIFICATION ---
if livre:
    with st.form("modifier_livre"):
        titre = st.text_input("Titre", livre["titre"])
        auteurs = st.text_input("Auteur(s)", livre["auteurs"] or "")
        annee = st.text_input("Année", livre["annee"] or "")
        editeur = st.text_input("Éditeur", livre["editeur"] or "")
        genre = st.text_input("Genre", livre["genre"] or "")
        langue = st.text_input("Langue", livre["langue"] or "")
        collection = st.text_input("Collection", livre["collection"] or "")
        emplacement = st.text_input("Emplacement", livre["emplacement"] or "")
        resume = st.text_area("Résumé", livre["resume"] or "")
        serie = st.text_input("Série", livre["serie"] or "")
        isbn = st.text_input("ISBN", livre["isbn"] or "")

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

        submitted = st.form_submit_button("💾 Enregistrer les modifications")
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

# --- SUPPRESSION ---
st.markdown("---")
if st.button("🗑️ Supprimer ce livre"):
    st.session_state["livre_a_supprimer"] = livre_id

if st.session_state.get("livre_a_supprimer") == int(livre["id"]):
    st.warning(f"⚠️ Confirmer la suppression de « {livre['titre']} » ?")
    col_ok, col_cancel = st.columns([1, 1])
    with col_ok:
        if st.button("✅ Oui, supprimer définitivement"):
            supprimer_livre(int(livre["id"]))
            st.success("🗑️ Livre supprimé.")
            st.session_state.pop("livre_a_supprimer", None)
            st.rerun()
    with col_cancel:
        if st.button("❌ Annuler la suppression"):
            st.session_state.pop("livre_a_supprimer", None)
            st.info("Suppression annulée.")
