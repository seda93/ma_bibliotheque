import streamlit as st
import sqlite3

DB_PATH = "data/livres.db"

def get_livre_par_id(livre_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM livres WHERE id = ?", (livre_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def update_livre(livre_id, donnees):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE livres SET
            titre = ?, auteurs = ?, serie = ?, annee = ?, genre = ?, langue = ?,
            isbn = ?, editeur = ?, collection = ?, resume = ?, emplacement = ?, image = ?
        WHERE id = ?
    """, (
        donnees["titre"], donnees["auteurs"], donnees["serie"], donnees["annee"], donnees["genre"],
        donnees["langue"], donnees["isbn"], donnees["editeur"], donnees["collection"],
        donnees["resume"], donnees["emplacement"], donnees["image"], livre_id
    ))
    conn.commit()
    conn.close()

st.title("✏️ Modifier un livre")

# Vérifier qu'un livre est sélectionné
if "livre_a_modifier" not in st.session_state:
    st.warning("Aucun livre sélectionné pour la modification.")
    st.stop()

livre_id = st.session_state["livre_a_modifier"]
row = get_livre_par_id(livre_id)

if not row:
    st.error("Livre introuvable.")
    st.stop()

# Colonnes de la base (ordre doit correspondre à SELECT *)
(
    id, titre, auteurs, serie, annee, genre, langue, isbn,
    editeur, collection, resume, emplacement, image
) = row

infos = {
    "titre": titre,
    "auteurs": auteurs,
    "serie": serie,
    "annee": annee,
    "genre": genre,
    "langue": langue,
    "isbn": isbn,
    "editeur": editeur,
    "collection": collection,
    "resume": resume,
    "emplacement": emplacement,
    "image": image
}

# Formulaire de modification
with st.form("form_modif"):
    st.text_input("Titre *", value=infos["titre"], key="modif_titre")
    st.text_input("Auteur(s)", value=infos["auteurs"], key="modif_auteurs")
    st.text_input("Série", value=infos["serie"], key="modif_serie")
    st.text_input("Année", value=infos["annee"], key="modif_annee")
    st.text_input("Genre", value=infos["genre"], key="modif_genre")
    st.text_input("Langue", value=infos["langue"], key="modif_langue")
    st.text_input("ISBN", value=infos["isbn"], key="modif_isbn")
    st.text_input("Éditeur", value=infos["editeur"], key="modif_editeur")
    st.text_input("Collection", value=infos["collection"], key="modif_collection")
    st.text_area("Résumé", value=infos["resume"], key="modif_resume")
    st.text_input("Emplacement", value=infos["emplacement"], key="modif_emplacement")
    st.text_input("Image (URL)", value=infos["image"], key="modif_image")

    submit = st.form_submit_button("✅ Enregistrer les modifications")

    if submit:
        updated = {
            "titre": st.session_state["modif_titre"],
            "auteurs": st.session_state["modif_auteurs"],
            "serie": st.session_state["modif_serie"],
            "annee": st.session_state["modif_annee"],
            "genre": st.session_state["modif_genre"],
            "langue": st.session_state["modif_langue"],
            "isbn": st.session_state["modif_isbn"],
            "editeur": st.session_state["modif_editeur"],
            "collection": st.session_state["modif_collection"],
            "resume": st.session_state["modif_resume"],
            "emplacement": st.session_state["modif_emplacement"],
            "image": st.session_state["modif_image"]
        }
        update_livre(livre_id, updated)
        st.success("✅ Livre mis à jour avec succès !")
        # Nettoyer l’ID pour éviter une nouvelle édition automatique
        del st.session_state["livre_a_modifier"]
