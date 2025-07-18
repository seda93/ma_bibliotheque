import streamlit as st
import pandas as pd
from PIL import Image
import os
from backend.database import get_sqlalchemy_engine

st.title("📚 Ma bibliothèque")

def charger_donnees():
    try:
        engine = get_sqlalchemy_engine()
        return pd.read_sql("SELECT * FROM livres", engine)
    except Exception as e:
        st.error(f"Erreur : {e}")
        return pd.DataFrame()

def supprimer_livre(livre_id):
    try:
        engine = get_sqlalchemy_engine()
        with engine.begin() as conn:
            conn.execute("DELETE FROM livres WHERE id = %s", (livre_id,))
    except Exception as e:
        st.error(f"Suppression impossible : {e}")

df_livres = charger_donnees()

if df_livres.empty:
    st.info("Aucun livre trouvé.")
else:
    tri = st.selectbox("Trier par :", ["titre", "auteurs", "genre", "langue", "annee"])
    ordre = st.radio("Ordre :", ["Croissant", "Décroissant"], horizontal=True)
    df_livres = df_livres.sort_values(by=tri, ascending=(ordre == "Croissant"))

    for _, livre in df_livres.iterrows():
        with st.container():
            cols = st.columns([1, 3])
            if livre["image"]:
                try:
                    if livre["image"].startswith("http"):
                        cols[0].image(livre["image"], width=120)
                    else:
                        img = Image.open(os.path.join("data", "images", os.path.basename(livre["image"])))
                        cols[0].image(img, width=120)
                except:
                    cols[0].markdown("⚠️ Image non trouvée")

            with cols[1]:
                st.markdown(f"### {livre['titre']}")
                st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
                st.markdown(f"**Série** : {livre['serie'] or '—'}")
                st.markdown(f"**Genre** : {livre['genre'] or '—'}")
                st.markdown(f"**Langue** : {livre['langue'] or '—'}")
                st.markdown(f"**Année** : {livre['annee'] or '—'}")
                st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
                st.markdown(f"**Collection** : {livre['collection'] or '—'}")
                st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
                if livre['resume']:
                    with st.expander("📖 Résumé"):
                        st.markdown(livre["resume"])

                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("📝 Modifier", key=f"modif_{livre['id']}"):
                        st.session_state["livre_a_modifier"] = livre["id"]
                        st.switch_page("pages/4_Modifier_supprimer.py")
                with col2:
                    if st.button("🗑️ Supprimer", key=f"suppr_{livre['id']}"):
                        st.session_state["livre_a_supprimer"] = livre["id"]
                    if st.session_state.get("livre_a_supprimer") == livre["id"]:
                        st.warning(f"Supprimer « {livre['titre']} » ?")
                        col_ok, col_cancel = st.columns([1, 1])
                        if col_ok.button("✅ Oui", key=f"ok_{livre['id']}"):
                            supprimer_livre(livre["id"])
                            st.success("Livre supprimé.")
                            del st.session_state["livre_a_supprimer"]
                            st.rerun()
                        if col_cancel.button("❌ Non", key=f"no_{livre['id']}"):
                            del st.session_state["livre_a_supprimer"]
                            st.info("Annulé.")
        st.markdown("---")
