import streamlit as st
from sqlalchemy import text
from backend.database import get_sqlalchemy_engine
from PIL import Image
import requests

st.title("🔍 Recherche de livres")

engine = get_sqlalchemy_engine()
recherche = st.text_input("Rechercher par titre, auteur, genre, etc.")

if recherche:
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT * FROM livres 
            WHERE LOWER(titre) LIKE :q OR LOWER(auteurs) LIKE :q 
               OR LOWER(genre) LIKE :q OR LOWER(langue) LIKE :q
               OR LOWER(serie) LIKE :q
        """), {"q": f"%{recherche.lower()}%"})
        livres = result.mappings().fetchall()

    if not livres:
        st.warning("Aucun livre trouvé.")
    else:
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
            st.markdown("---")
