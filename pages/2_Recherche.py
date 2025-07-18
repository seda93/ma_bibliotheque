import streamlit as st
import pandas as pd
from sqlalchemy import text
from backend.database import get_sqlalchemy_engine

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

st.title("🔍 Recherche")

engine = get_sqlalchemy_engine()

def charger_donnees():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres"))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

df = charger_donnees()

recherche = st.text_input("Rechercher par titre, auteur, éditeur ou genre :")

if recherche:
    mask = df.apply(lambda row: recherche.lower() in str(row).lower(), axis=1)
    resultats = df[mask]

    if not resultats.empty:
        for _, livre in resultats.iterrows():
            with st.container():
                cols = st.columns([1, 3])
                if livre["image"]:
                    cols[0].image(livre["image"], width=120)
                with cols[1]:
                    st.markdown(f"### {livre['titre']}")
                    st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
                    st.markdown(f"**Année** : {livre['annee'] or '—'}")
                    st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
                    st.markdown(f"**Genre** : {livre['genre'] or '—'}")
                    st.markdown(f"**Langue** : {livre['langue'] or '—'}")
                    st.markdown(f"**Collection** : {livre['collection'] or '—'}")
                    st.markdown(f"**Série** : {livre['serie'] or '—'}")
                    st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
                    if livre['resume']:
                        with st.expander("📖 Résumé"):
                            st.markdown(livre["resume"])
                    st.markdown("---")
    else:
        st.warning("Aucun résultat trouvé.")
else:
    st.info("Veuillez entrer un mot-clé.")
