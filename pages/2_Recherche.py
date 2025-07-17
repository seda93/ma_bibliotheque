import streamlit as st
import pandas as pd
import sqlite3
import os

DB_PATH = "data/livres.db"

def charger_livres():
    if not os.path.exists(DB_PATH):
        st.error("Base de données non trouvée.")
        return pd.DataFrame()
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM livres", conn)
    conn.close()
    return df

def filtrer_livres(df, titre, auteur, genre, langue):
    if titre:
        df = df[df["titre"].str.contains(titre, case=False, na=False)]
    if auteur:
        df = df[df["auteurs"].str.contains(auteur, case=False, na=False)]
    if genre and genre != "Tous":
        df = df[df["genre"].str.contains(genre, case=False, na=False)]
    if langue and langue != "Toutes":
        df = df[df["langue"].str.contains(langue, case=False, na=False)]
    return df

st.title("🔎 Recherche de livres")

df_livres = charger_livres()

if df_livres.empty:
    st.info("Aucun livre trouvé dans la base.")
else:
    with st.expander("🔍 Filtres de recherche", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            titre = st.text_input("Titre contient")
            auteur = st.text_input("Auteur contient")
        with col2:
            genre = st.selectbox("Genre", options=["Tous"] + sorted(df_livres["genre"].dropna().unique().tolist()))
            langue = st.selectbox("Langue", options=["Toutes"] + sorted(df_livres["langue"].dropna().unique().tolist()))

    resultats = filtrer_livres(df_livres, titre, auteur, genre, langue)

    st.markdown(f"### 📚 Résultats : {len(resultats)} livre(s) trouvé(s)")
    st.dataframe(resultats, use_container_width=True)

    # Export CSV
    if not resultats.empty:
        csv = resultats.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Exporter les résultats en CSV",
            data=csv,
            file_name="resultats_recherche.csv",
            mime="text/csv"
        )
