import streamlit as st
import pandas as pd
import sqlite3
import io

@st.cache_data
def generer_modele_csv():
    df = pd.DataFrame(columns=[
        "titre", "auteurs", "serie", "annee", "genre", "langue", "isbn",
        "editeur", "collection", "resume", "emplacement", "image"
    ])
    return df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📄 Télécharger un modèle de fichier CSV",
    data=generer_modele_csv(),
    file_name="modele_bibliotheque.csv",
    mime="text/csv"
)

DB_PATH = "data/livres.db"

def ajouter_livre_csv(row):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO livres (
                titre, auteurs, serie, annee, genre, langue, isbn,
                editeur, collection, resume, emplacement, image
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row.get("titre", ""),
            row.get("auteurs", ""),
            row.get("serie", ""),
            row.get("annee", ""),
            row.get("genre", ""),
            row.get("langue", ""),
            row.get("isbn", ""),
            row.get("editeur", ""),
            row.get("collection", ""),
            row.get("resume", ""),
            row.get("emplacement", ""),
            row.get("image", "")
        ))
        conn.commit()
        return True  # succès
    except sqlite3.IntegrityError:
        return False  # doublon ISBN
    finally:
        conn.close()

st.title("📥 Importer des livres via un fichier CSV")

fichier = st.file_uploader("Sélectionnez un fichier CSV", type=["csv"])

if fichier is not None:
    try:
        df = pd.read_csv(fichier)

        # Vérifier colonnes minimales
        colonnes_attendues = [
            "titre", "auteurs", "serie", "annee", "genre", "langue", "isbn",
            "editeur", "collection", "resume", "emplacement", "image"
        ]
        colonnes_manquantes = [col for col in colonnes_attendues if col not in df.columns]

        if colonnes_manquantes:
            st.error(f"Colonnes manquantes dans le CSV : {', '.join(colonnes_manquantes)}")
        else:
            st.success("✅ Fichier valide")
            st.write("Aperçu des données :")
            st.dataframe(df.head(), use_container_width=True)

            if st.button("📚 Importer tous les livres"):
                nb_ajoutes = 0
                nb_doublons = 0
                for _, row in df.iterrows():
                    success = ajouter_livre_csv(row)
                    if success:
                        nb_ajoutes += 1
                    else:
                        nb_doublons += 1

                if nb_ajoutes > 0:
                    st.success(f"✅ {nb_ajoutes} livre(s) importé(s) avec succès.")
                if nb_doublons > 0:
                    st.warning(f"⚠️ {nb_doublons} livre(s) ignoré(s) car déjà présent(s) (ISBN identique).")

                st.rerun()

    except Exception as e:
        st.error(f"Erreur de lecture du fichier : {e}")
