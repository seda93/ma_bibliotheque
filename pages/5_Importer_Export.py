import streamlit as st
import pandas as pd
from backend.database import get_connection

st.set_page_config(page_title="📥 Importer/Exporter des livres", page_icon="📥")
st.title("📥 Importer / Exporter des livres depuis ou vers un fichier CSV")

# --- Exportation CSV intégrée ---
st.subheader("📤 Exporter la base actuelle en CSV")
if st.button("📤 Exporter la base"):
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM livres", conn)
        conn.close()
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Télécharger le fichier CSV", csv, "livres_export.csv", "text/csv")
    except Exception as e:
        st.error(f"Erreur : {e}")

# --- Importation CSV ---
st.subheader("📥 Importer un fichier CSV")
uploaded_file = st.file_uploader("Sélectionnez un fichier CSV", type="csv")

if uploaded_file:
    try:
        df_new = pd.read_csv(uploaded_file)
        conn = get_connection()
        cursor = conn.cursor()

        livres_ajoutes = 0
        livres_ignores = 0

        for _, row in df_new.iterrows():
            isbn = row.get("isbn")
            if isbn:
                cursor.execute("SELECT COUNT(*) FROM livres WHERE isbn = %s", (isbn,))
                if cursor.fetchone()[0]:
                    livres_ignores += 1
                    continue

            cursor.execute("""
                INSERT INTO livres (titre, auteurs, serie, annee, genre, langue, isbn, editeur, collection, resume, emplacement, image)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                row.get("titre"), row.get("auteurs"), row.get("serie"),
                row.get("annee"), row.get("genre"), row.get("langue"),
                row.get("isbn"), row.get("editeur"), row.get("collection"),
                row.get("resume"), row.get("emplacement"), row.get("image")
            ))
            livres_ajoutes += 1

        conn.commit()
        conn.close()

        st.success(f"✅ {livres_ajoutes} livre(s) importé(s), {livres_ignores} ignoré(s) (doublons ISBN).")
    except Exception as e:
        st.error(f"Erreur lors de l'importation : {e}")
