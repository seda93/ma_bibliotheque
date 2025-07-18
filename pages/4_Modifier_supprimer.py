import streamlit as st
import sqlite3
import os
from PIL import Image

DB_PATH = "data/livres.db"
COVERS_DIR = "data/covers"

def get_liste_livres():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titre, auteurs FROM livres ORDER BY titre")
    result = cursor.fetchall()
    conn.close()
    return result

def get_livre(livre_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livres WHERE id = ?", (livre_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        colonnes = ["id", "titre", "auteurs", "collection", "annee", "genre", "langue",
                    "isbn", "editeur", "emplacement", "resume", "image"]
        return dict(zip(colonnes, row))
    return None

def update_livre(livre_id, donnees):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE livres
        SET titre = ?, auteurs = ?, collection = ?, annee = ?, genre = ?, langue = ?,
            isbn = ?, editeur = ?, emplacement = ?, resume = ?, image = ?
        WHERE id = ?
    """, (
        donnees["titre"], donnees["auteurs"], donnees["collection"], donnees["annee"],
        donnees["genre"], donnees["langue"], donnees["isbn"], donnees["editeur"],
        donnees["emplacement"], donnees["resume"], donnees["image"], livre_id
    ))
    conn.commit()
    conn.close()

st.title("📝 Modifier un livre par sélection")

# Étape 1 : choisir le livre à modifier
livres = get_liste_livres()
options = {f"{titre} – {auteurs or 'Auteur inconnu'} (ID {id})": id for id, titre, auteurs in livres}
selection = st.selectbox("📖 Choisir un livre à modifier :", list(options.keys()))

if selection:
    livre_id = options[selection]
    livre = get_livre(livre_id)

    if not livre:
        st.error("Livre introuvable.")
        st.stop()

    with st.form("modifier_livre"):
        titre = st.text_input("Titre", value=livre["titre"])
        auteurs = st.text_input("Auteur(s)", value=livre["auteurs"])
        collection = st.text_input("Collection", value=livre["collection"])
        annee = st.text_input("Année", value=livre["annee"])
        genre = st.text_input("Genre", value=livre["genre"])
        langue = st.text_input("Langue", value=livre["langue"])
        isbn = st.text_input("ISBN", value=livre["isbn"])
        editeur = st.text_input("Éditeur", value=livre["editeur"])
        emplacement = st.text_input("Emplacement", value=livre["emplacement"])
        resume = st.text_area("Résumé", value=livre["resume"])

        if livre["image"]:
            try:
                if livre["image"].startswith("http"):
                    st.image(livre["image"], width=150)
                else:
                    st.image(Image.open(livre["image"]), width=150)
            except:
                st.warning("Image actuelle introuvable.")

        uploaded_image = st.file_uploader("📷 Nouvelle image de couverture (facultatif)", type=["png", "jpg", "jpeg"])

        submitted = st.form_submit_button("💾 Enregistrer les modifications")

    if submitted:
        nouvelle_image_path = livre["image"]

        if uploaded_image:
            os.makedirs(COVERS_DIR, exist_ok=True)
            nouvelle_image_path = os.path.join(COVERS_DIR, uploaded_image.name)
            with open(nouvelle_image_path, "wb") as f:
                f.write(uploaded_image.getbuffer())

        nouvelles_donnees = {
            "titre": titre,
            "auteurs": auteurs,
            "collection": collection,
            "annee": annee,
            "genre": genre,
            "langue": langue,
            "isbn": isbn,
            "editeur": editeur,
            "emplacement": emplacement,
            "resume": resume,
            "image": nouvelle_image_path
        }

        update_livre(livre_id, nouvelles_donnees)
        st.success("✅ Livre mis à jour avec succès.")
