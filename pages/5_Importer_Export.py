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

import streamlit as st
import pandas as pd
from sqlalchemy import text
from backend.database import get_sqlalchemy_engine

engine = get_sqlalchemy_engine()

st.title("📥 Importer / Exporter la base au format CSV")

# ➕ Import CSV
st.header("📁 Importer un fichier CSV")
fichier = st.file_uploader("Sélectionner un fichier CSV", type="csv")

if fichier:
    df = pd.read_csv(fichier)
    ajoutés, ignorés = 0, 0
    with engine.begin() as conn:
        for _, row in df.iterrows():
            result = conn.execute(text("SELECT COUNT(*) FROM livres WHERE isbn = :isbn"), {"isbn": row["isbn"]})
            if result.scalar() == 0:
                conn.execute(text("""
                    INSERT INTO livres 
                    (titre, auteurs, serie, annee, genre, langue, isbn, editeur, collection, emplacement, resume, image)
                    VALUES (:titre, :auteurs, :serie, :annee, :genre, :langue, :isbn, :editeur, :collection, :emplacement, :resume, :image)
                """), row.to_dict())
                ajoutés += 1
            else:
                ignorés += 1
    st.success(f"✅ {ajoutés} livres ajoutés — {ignorés} ignorés (déjà présents).")

# ⬇ Export CSV
st.header("📤 Exporter la base actuelle")
if st.button("📄 Télécharger la base au format CSV"):
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM livres", conn)
        st.download_button("📥 Télécharger CSV", df.to_csv(index=False), file_name="livres.csv", mime="text/csv")
