import streamlit as st
import pandas as pd
import psycopg2
import os
from PIL import Image
from backend.database import get_connection
from backend.supabase_client import upload_image_to_bucket

IMG_DIR = "data/images"
os.makedirs(IMG_DIR, exist_ok=True)

def get_liste_livres():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, titre, auteurs FROM livres ORDER BY titre")
        livres = cursor.fetchall()
        conn.close()
        return livres
    except Exception as e:
        st.error(f"Erreur : {e}")
        return []

def get_livre_par_id(livre_id):
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM livres WHERE id = %s", conn, params=(livre_id,))
        conn.close()
        return df.iloc[0] if not df.empty else None
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None

def modifier_livre(livre_id, donnees):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE livres SET
                titre=%s, auteurs=%s, serie=%s, collection=%s, annee=%s,
                genre=%s, langue=%s, editeur=%s, emplacement=%s,
                resume=%s, image=%s
            WHERE id=%s
        """, (
            donnees["titre"], donnees["auteurs"], donnees["serie"], donnees["collection"],
            donnees["annee"], donnees["genre"], donnees["langue"], donnees["editeur"],
            donnees["emplacement"], donnees["resume"], donnees["image"], livre_id
        ))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Erreur lors de la mise à jour : {e}")
        return False

# --- Interface Streamlit ---

st.title("📝 Modifier un livre")

livres = get_liste_livres()
if not livres:
    st.info("Aucun livre à modifier.")
    st.stop()

option_map = {f"{titre} – {auteurs or 'Auteur inconnu'}": id for id, titre, auteurs in livres}
selected_label = st.selectbox("Choisir un livre à modifier :", list(option_map.keys()))
livre_id = option_map[selected_label]
livre = get_livre_par_id(livre_id)

if not livre.empty:
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

        nouvelle_image = st.file_uploader("📷 Nouvelle image de couverture (facultatif)", type=["jpg", "jpeg", "png"])
        image_url = st.text_input("ou coller une URL d’image", livre["image"])

        if nouvelle_image is not None:
            uploaded_url = upload_image_to_bucket(nouvelle_image, nouvelle_image.name)
            if uploaded_url:
                image_a_sauver = uploaded_url
            else:
                st.error("❌ L’image n’a pas pu être envoyée.")
                image_a_sauver = livre["image"]
        else:
            image_a_sauver = image_url

        submitted = st.form_submit_button("✅ Enregistrer les modifications")
        if submitted:
            donnees = {
                "titre": titre,
                "auteurs": auteurs,
                "serie": serie,
                "collection": collection,
                "annee": annee,
                "genre": genre,
                "langue": langue,
                "editeur": editeur,
                "emplacement": emplacement,
                "resume": resume,
                "image": image_a_sauver
            }
            success = modifier_livre(livre_id, donnees)
            if success:
                st.success("✅ Livre modifié avec succès.")
                st.rerun()
