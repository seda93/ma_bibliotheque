import streamlit as st
import pandas as pd
from PIL import Image
import os
from backend.database import get_connection  # ← ta fonction centralisée PostgreSQL

def charger_donnees():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM livres", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erreur lors du chargement : {e}")
        return pd.DataFrame()

def afficher_livre(livre):
    with st.container():
        cols = st.columns([1, 3])
        if livre["image"]:
            try:
                if livre["image"].startswith("http"):
                    cols[0].image(livre["image"], width=120)
                else:
                    img_path = os.path.join("data", "images", os.path.basename(livre["image"]))
                    img = Image.open(img_path)
                    cols[0].image(img, width=120)
            except:
                cols[0].markdown("⚠️ Image non trouvée")
        with cols[1]:
            st.markdown(f"### {livre['titre']}")
            st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
            st.markdown(f"**Série** : {livre['serie'] or '—'}")
            st.markdown(f"**Genre** : {livre['genre'] or '—'}")
            st.markdown(f"**Année** : {livre['annee'] or '—'}")
            st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
            st.markdown(f"**Collection** : {livre['collection'] or '—'}")
            st.markdown(f"**Langue** : {livre['langue'] or '—'}")
            st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
            if livre['resume']:
                with st.expander("📖 Résumé"):
                    st.markdown(livre["resume"])
    st.markdown("---")

# Interface utilisateur
st.title("🔎 Recherche de livres")
df = charger_donnees()

if df.empty:
    st.info("Aucun livre trouvé.")
else:
    recherche = st.text_input("Rechercher par titre, auteur, éditeur ou genre")

    if recherche:
        df = df[df.apply(lambda row: recherche.lower() in str(row).lower(), axis=1)]

    if df.empty:
        st.warning("Aucun résultat.")
    else:
        for _, livre in df.iterrows():
            afficher_livre(livre)
