import streamlit as st
import pandas as pd
from backend.database import get_sqlalchemy_engine

engine = get_sqlalchemy_engine()

st.title("📥 Importer / Exporter la base de livres")

# Export
if st.button("📤 Exporter au format CSV"):
    df = pd.read_sql("SELECT * FROM livres", engine)
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("📄 Télécharger CSV", data=csv, file_name="livres_export.csv", mime="text/csv")

# Import
uploaded = st.file_uploader("📥 Importer un fichier CSV", type=["csv"])
if uploaded:
    new_df = pd.read_csv(uploaded)
    ajoutés, ignorés = 0, 0
    existants = pd.read_sql("SELECT isbn FROM livres", engine)["isbn"].tolist()

    with engine.begin() as conn:
        for _, row in new_df.iterrows():
            if row["isbn"] in existants:
                ignorés += 1
                continue
            try:
                conn.execute(
                    """
                    INSERT INTO livres (titre, auteurs, serie, annee, genre, langue, isbn, editeur, collection, resume, emplacement, image)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    tuple(row.fillna("").values)
                )
                ajoutés += 1
            except Exception as e:
                st.error(f"Erreur avec le livre : {row['titre']} – {e}")

    st.success(f"{ajoutés} livre(s) ajouté(s), {ignorés} ignoré(s).")
