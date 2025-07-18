import streamlit as st
import pandas as pd
from PIL import Image
import os
from backend.database import get_sqlalchemy_engine

st.title("🔍 Rechercher un livre")

engine = get_sqlalchemy_engine()
df = pd.read_sql("SELECT * FROM livres", engine)

recherche = st.text_input("🔎 Recherche par titre, auteur ou genre")

if recherche:
    filtre = df.apply(lambda x: recherche.lower() in str(x).lower(), axis=1)
    resultats = df[filtre]

    if resultats.empty:
        st.warning("Aucun résultat trouvé.")
    else:
        for _, livre in resultats.iterrows():
            with st.container():
                cols = st.columns([1, 3])
                if livre["image"]:
                    try:
                        if livre["image"].startswith("http"):
                            cols[0].image(livre["image"], width=120)
                        else:
                            img = Image.open(os.path.join("data", "images", os.path.basename(livre["image"])))
                            cols[0].image(img, width=120)
                    except:
                        cols[0].markdown("⚠️ Image non trouvée")

                with cols[1]:
                    st.markdown(f"### {livre['titre']}")
                    st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
                    st.markdown(f"**Genre** : {livre['genre'] or '—'}")
                    st.markdown(f"**Langue** : {livre['langue'] or '—'}")
                    st.markdown(f"**Année** : {livre['annee'] or '—'}")
