import streamlit as st
import pandas as pd
from PIL import Image
from backend.database import get_sqlalchemy_engine
from sqlalchemy import text

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

st.title("📚 Ma bibliothèque")

engine = get_sqlalchemy_engine()

def charger_donnees():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres"))
        return result.mappings().fetchall()

livres = charger_donnees()

if not livres:
    st.info("Aucun livre trouvé.")
else:
    colonnes_triables = ["titre", "auteurs", "genre", "langue", "annee"]
    tri = st.selectbox("Trier par :", colonnes_triables)
    ordre = st.radio("Ordre :", ["Croissant", "Décroissant"], horizontal=True)
    livres = sorted(livres, key=lambda x: x[tri] or "", reverse=(ordre == "Décroissant"))

    for livre in livres:
        with st.container():
            cols = st.columns([1, 3])
            if livre["image"]:
                try:
                    if livre["image"].startswith("http"):
                        cols[0].image(livre["image"], width=120)
                    else:
                        img = Image.open(livre["image"])
                        cols[0].image(img, width=120)
                except:
                    cols[0].warning("Image non disponible")
            with cols[1]:
                st.markdown(f"### {livre['titre']}")
                st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
                st.markdown(f"**Série** : {livre['serie'] or '—'}")
                st.markdown(f"**Genre** : {livre['genre'] or '—'}")
                st.markdown(f"**Langue** : {livre['langue'] or '—'}")
                st.markdown(f"**Année** : {livre['annee'] or '—'}")
                st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
                st.markdown(f"**Collection** : {livre['collection'] or '—'}")
                st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
                if livre["resume"]:
                    with st.expander("📖 Résumé"):
                        st.markdown(livre["resume"])
                # Boutons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📝 Modifier", key=f"modif_{livre['id']}"):
                        st.session_state["livre_a_modifier"] = livre["id"]
                        st.switch_page("pages/4_Modifier_supprimer.py")
                with col2:
                    if st.button("🗑️ Supprimer", key=f"suppr_{livre['id']}"):
                        st.session_state["livre_a_supprimer"] = livre["id"]
                        st.rerun()
        st.markdown("---")
