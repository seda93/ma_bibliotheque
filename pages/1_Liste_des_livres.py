import streamlit as st
import psycopg2
import pandas as pd
import os
from PIL import Image
from backend.database import get_connection  # <-- ton fichier de connexion PostgreSQL

def charger_donnees():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM livres", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erreur de connexion à la base : {e}")
        return pd.DataFrame()

def supprimer_livre(livre_id):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM livres WHERE id = %s", (livre_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        st.error(f"Erreur lors de la suppression : {e}")

st.title("📚 Ma bibliothèque")

df_livres = charger_donnees()

if df_livres.empty:
    st.info("Aucun livre trouvé dans la base de données.")
else:
    colonnes_triables = ["titre", "auteurs", "serie", "genre", "langue", "annee"]
    tri = st.selectbox("Trier par :", colonnes_triables)
    ordre = st.radio("Ordre :", ["Croissant", "Décroissant"], horizontal=True)
    df_livres_sorted = df_livres.sort_values(by=tri, ascending=(ordre == "Croissant"))

    for _, livre in df_livres_sorted.iterrows():
        with st.container():
            cols = st.columns([1, 3])
            if livre["image"]:
                try:
                    if livre["image"].startswith("http"):
                        cols[0].image(livre["image"], width=120)
                    else:
                        img_path = os.path.join("data", "images", os.path.basename(livre["image"]))
                        img = Image.open(img_path)
                        cols[0].image(img, width=120)
                except:
                    cols[0].markdown("⚠️ Image non trouvée")
            with cols[1]:
                st.markdown(f"### {livre['titre']}")
                st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
                st.markdown(f"**Série** : {livre['serie'] or '—'}")
                st.markdown(f"**Genre** : {livre['genre'] or '—'}")
                st.markdown(f"**Année** : {livre['annee'] or '—'}")
                st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
                st.markdown(f"**Collection** : {livre['collection'] or '—'}")
                st.markdown(f"**Langue** : {livre['langue'] or '—'}")
                st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
                if livre['resume']:
                    with st.expander("📖 Résumé"):
                        st.markdown(livre["resume"])

                # Boutons
                col_modif, col_suppr = st.columns([1, 1])
                with col_modif:
                    if st.button("📝 Modifier", key=f"modif_{livre['id']}"):
                        st.session_state["livre_a_modifier"] = livre["id"]
                        st.switch_page("pages/4_Modifier_supprimer.py")
                with col_suppr:
                    if st.button("🗑️ Supprimer", key=f"suppr_{livre['id']}"):
                        st.session_state["livre_a_supprimer"] = livre["id"]

                    # Confirmation juste après
                    if st.session_state.get("livre_a_supprimer") == livre["id"]:
                        st.warning(f"⚠️ Confirmer la suppression de « {livre['titre']} » ?")
                        col_ok, col_cancel = st.columns([1, 1])
                        with col_ok:
                            if st.button("✅ Oui, supprimer", key=f"confirm_{livre['id']}"):
                                supprimer_livre(livre["id"])
                                st.success("Livre supprimé.")
                                del st.session_state["livre_a_supprimer"]
                                st.rerun()
                        with col_cancel:
                            if st.button("❌ Annuler", key=f"cancel_{livre['id']}"):
                                del st.session_state["livre_a_supprimer"]
                                st.info("Suppression annulée.")
        st.markdown("---")
