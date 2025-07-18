import streamlit as st
import pandas as pd
from sqlalchemy import text
from PIL import Image
import os

from backend.database import get_sqlalchemy_engine
from backend.supabase_client import upload_image_to_bucket

IMG_DIR = "data/images"
os.makedirs(IMG_DIR, exist_ok=True)

def get_liste_livres():
    try:
        engine = get_sqlalchemy_engine()
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, titre, auteurs FROM livres ORDER BY titre"))
            return result.fetchall()
    except Exception as e:
        st.error(f"Erreur : {e}")
        return []

def get_livre_par_id(livre_id):
    try:
        engine = get_sqlalchemy_engine()
        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM livres WHERE id = %(id)s", conn, params={"id": livre_id})
        return df.iloc[0] if not df.empty else None
    except Exception as e:
        st.error(f"Erreur : {e}")
        return None

def modifier_livre(livre_id, donnees):
    try:
        engine = get_sqlalchemy_engine()
        with engine.connect() as conn:
            conn.execute(text("""
                UPDATE livres SET
                    titre=:titre, auteurs=:auteurs, serie=:serie, collection=:collection,
                    annee=:annee, genre=:genre, langue=:langue, editeur=:editeur,
                    emplacement=:emplacement, resume=:resume, image=:image
                WHERE id=:id
            """), {**donnees, "id": livre_id})
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

if livre is not None:
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
        resume = st.text_area("Résumé", livre["resume"])

        st.markdown("**Image actuelle :**")
        if livre["image"]:
            if livre["image"].startswith("http"):
                st.image(livre["image"], width=100)
            else:
                try:
                    st.image(Image.open(livre["image"]), width=100)
                except:
                    st.warning("Image non trouvée localement.")
        nouvelle_image = st.file_uploader("📷 Nouvelle image", type=["jpg", "png"], key="modif_image")

        image_url = livre["image"]
        if nouvelle_image:
            image_url = upload_image_to_bucket(nouvelle_image)

        submitted = st.form_submit_button("💾 Enregistrer les modifications")

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
                "image": image_url
            }
            if modifier_livre(livre_id, donnees):
                st.success("✅ Livre modifié avec succès !")
                st.rerun()
else:
    st.error("Livre introuvable.")
