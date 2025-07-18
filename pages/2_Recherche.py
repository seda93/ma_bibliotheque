import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os

DB_PATH = "data/livres.db"

def charger_donnees():
    if not os.path.exists(DB_PATH):
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM livres", conn)
    conn.close()
    return df

def afficher_livre(livre):
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
                cols[0].warning("Image non trouvée.")
        with cols[1]:
            st.markdown(f"### {livre['titre']}")
            st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
            st.markdown(f"**Année** : {livre['annee'] or '—'}")
            st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
            st.markdown(f"**Genre** : {livre['genre'] or '—'}")
            st.markdown(f"**Langue** : {livre['langue'] or '—'}")
            st.markdown(f"**Collection** : {livre['collection'] or '—'}")
            st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
            if livre['resume']:
                with st.expander("📖 Résumé"):
                    st.markdown(livre["resume"])
    st.markdown("---")

# ⬇️ Interface utilisateur
st.title("🔎 Recherche de livres")
df = charger_donnees()

if df.empty:
    st.info("Aucun livre trouvé.")
else:
    recherche = st.text_input("Rechercher par titre, auteur, éditeur ou genre")

    # Filtrage simple (tu peux l’enrichir plus tard)
    if recherche:
        df = df[df.apply(lambda row: recherche.lower() in str(row).lower(), axis=1)]

    if df.empty:
        st.warning("Aucun résultat.")
    else:
        for _, livre in df.iterrows():
            afficher_livre(livre)
