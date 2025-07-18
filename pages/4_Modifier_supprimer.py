import streamlit as st
import sqlite3
import pandas as pd
from PIL import Image
import os

DB_PATH = "data/livres.db"

def get_liste_livres():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titre, auteurs FROM livres ORDER BY titre")
    livres = cursor.fetchall()
    conn.close()
    return livres

def get_livre_par_id(livre_id):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM livres WHERE id = ?", conn, params=(livre_id,))
    conn.close()
    return df.iloc[0] if not df.empty else None

st.title("📝 Modifier un livre")

livres = get_liste_livres()
if not livres:
    st.info("Aucun livre à modifier.")
    st.stop()

# Création d'un dictionnaire pour relier titre-auteur à l'ID
option_map = {f"{titre} – {auteurs or 'Auteur inconnu'}": id for id, titre, auteurs in livres}

# Liste des titres pour l'affichage
selected_label = st.selectbox("Choisir un livre à modifier :", list(option_map.keys()))

livre_id = option_map[selected_label]
livre = get_livre_par_id(livre_id)

# Formulaire de modification
with st.form("modifier_livre"):
    titre = st.text_input("Titre", livre["titre"])
    auteurs = st.text_input("Auteur(s)", livre["auteurs"])
    serie = st.text_input("Série", livre["serie"])
    collection = st.text_input("Collection", livre["collection"])
    annee = st.text_input("Année", livre["annee"])
    genre = st.text_input("Genre", livre["genre"])
    langue = st.text_input("Langue", livre["langue"])
    editeur = st.text_input("Éditeur", livre["editeur"])
    emplacement = st.text_input("Emplacement", livre["emplacement"])
    resume = st.text_area("Résumé", livre["resume"] or "")

    # Image locale ou URL
    nouvelle_image = st.file_uploader("📷 Nouvelle image de couverture (facultatif)", type=["jpg", "jpeg", "png"])
    image_url = st.text_input("ou coller une URL d’image", livre["image"])

    if nouvelle_image is not None:
        # Enregistrement local
        chemin_image = os.path.join("images", nouvelle_image.name)
        with open(chemin_image, "wb") as f:
            f.write(nouvelle_image.read())
        image_a_sauver = chemin_image
    else:
        image_a_sauver = image_url

    submitted = st.form_submit_button("✅ Enregistrer les modifications")
    if submitted:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livres
            SET titre=?, auteurs=?, serie=?, collection=?, annee=?, genre=?, langue=?,
                editeur=?, emplacement=?, resume=?, image=?
            WHERE id=?
        """, (titre, auteurs, serie, collection, annee, genre, langue,
              editeur, emplacement, resume, image_a_sauver, livre_id))
        conn.commit()
        conn.close()
        st.success("✅ Livre modifié avec succès.")
        st.rerun()
