import streamlit as st
import sqlite3
from backend.isbn_lookup import fetch_book_info
import os

IMG_DIR = "data/images"
os.makedirs(IMG_DIR, exist_ok=True)

DB_PATH = "data/livres.db"

def ajouter_livre(donnees):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO livres (
                titre, auteurs, serie, annee, genre, langue, isbn,
                editeur, collection, resume, emplacement, image
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            donnees["titre"], donnees["auteurs"], donnees["serie"], donnees["annee"],
            donnees["genre"], donnees["langue"], donnees["isbn"],
            donnees["editeur"], donnees["collection"], donnees["resume"],
            donnees["emplacement"], donnees["image"]
        ))
        conn.commit()
        st.success("📚 Livre ajouté avec succès !")
    except sqlite3.IntegrityError:
        st.warning("⚠️ Ce livre (ISBN) existe déjà dans la base.")
    finally:
        conn.close()

st.title("➕ Ajouter un livre")

# Bloc ISBN
st.subheader("🔎 Recherche par ISBN")

isbn_input = st.text_input("Entrer un ISBN :", max_chars=20)

infos = {
    "titre": "", "auteurs": "", "serie": "", "annee": "", "genre": "",
    "langue": "", "isbn": "", "editeur": "", "collection": "", "resume": "",
    "emplacement": "", "image": ""
}

if isbn_input:
    donnees_isbn = fetch_book_info(isbn_input)
    if donnees_isbn:
        st.success("✅ Informations trouvées ! Complétez les champs ci-dessous.")
        infos.update(donnees_isbn)
    else:
        st.warning("❌ Aucune information trouvée pour cet ISBN.")

# Formulaire manuel
st.subheader("📝 Ajouter ou modifier les informations")

with st.form("form_ajout"):
    infos["titre"] = st.text_input("Titre *", value=infos["titre"])
    infos["auteurs"] = st.text_input("Auteur(s)", value=infos["auteurs"])
    infos["serie"] = st.text_input("Série", value=infos["serie"])
    infos["annee"] = st.text_input("Année", value=infos["annee"])
    infos["genre"] = st.text_input("Genre(s)", value=infos["genre"])
    infos["langue"] = st.text_input("Langue", value=infos["langue"])
    infos["isbn"] = st.text_input("ISBN", value=infos["isbn"])
    infos["editeur"] = st.text_input("Éditeur", value=infos["editeur"])
    infos["collection"] = st.text_input("Collection", value=infos["collection"])
    infos["resume"] = st.text_area("Résumé", value=infos["resume"])
    infos["emplacement"] = st.text_input("Emplacement (bibliothèque, étagère...)", value=infos["emplacement"])
    infos["image"] = st.text_input("URL de l’image de couverture", value=infos["image"])

    submit = st.form_submit_button("📥 Ajouter le livre")
    if submit:
        if infos["titre"].strip():
            ajouter_livre(infos)
        else:
            st.error("Le champ titre est obligatoire.")

image_upload = st.file_uploader("Image de couverture (fichier ou laisser vide si URL)", type=["jpg", "png"])

# Générer un nom de fichier local
if image_upload:
    img_path = os.path.join(IMG_DIR, image_upload.name)
    with open(img_path, "wb") as f:
        f.write(image_upload.getbuffer())
    infos["image"] = img_path  # enregistre le chemin local