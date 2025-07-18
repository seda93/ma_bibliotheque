import streamlit as st
import pandas as pd
from PIL import Image
from sqlalchemy import text
from backend.database import get_sqlalchemy_engine

st.markdown("""
<style>
body {
    background-color: #fdf6f0;
}
section.main > div {
    background-color: #ffffffdd;
    border-radius: 1rem;
    padding: 1rem;
    box-shadow: 0px 0px 10px rgba(200, 200, 200, 0.3);
}
h1, h2, h3 {
    color: #6a5acd;
}
</style>
""", unsafe_allow_html=True)

engine = get_sqlalchemy_engine()

st.title("📚 Ma bibliothèque")

def charger_donnees():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres"))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

def supprimer_livre(livre_id):
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM livres WHERE id = :id"), {"id": livre_id})

df_livres = charger_donnees()

if df_livres.empty:
    st.info("Aucun livre trouvé dans la base de données.")
else:
    tri = st.selectbox("Trier par :", ["titre", "auteurs", "genre", "langue", "annee"])
    ordre = st.radio("Ordre :", ["Croissant", "Décroissant"], horizontal=True)
    df_sorted = df_livres.sort_values(by=tri, ascending=(ordre == "Croissant"))

    for _, livre in df_sorted.iterrows():
        with st.container():
            cols = st.columns([1, 3])
            if livre["image"]:
                cols[0].image(livre["image"], width=120)
            with cols[1]:
                st.markdown(f"### {livre['titre']}")
                st.markdown(f"**Auteur(s)** : {livre['auteurs'] or 'Inconnu'}")
                st.markdown(f"**Année** : {livre['annee'] or '—'}")
                st.markdown(f"**Éditeur** : {livre['editeur'] or '—'}")
                st.markdown(f"**Genre** : {livre['genre'] or '—'}")
                st.markdown(f"**Langue** : {livre['langue'] or '—'}")
                st.markdown(f"**Collection** : {livre['collection'] or '—'}")
                st.markdown(f"**Série** : {livre['serie'] or '—'}")
                st.markdown(f"**Emplacement** : {livre['emplacement'] or '—'}")
                if livre['resume']:
                    with st.expander("📖 Résumé"):
                        st.markdown(livre["resume"])

                col_modif, col_suppr = st.columns([1, 1])
                with col_modif:
                    if st.button("✏️ Modifier", key=f"modif_{livre['id']}"):
                        st.session_state["livre_a_modifier"] = livre["id"]
                        st.switch_page("pages/4_Modifier_supprimer.py")
                with col_suppr:
                    if st.button("🗑️ Supprimer", key=f"suppr_{livre['id']}"):
                        st.session_state["livre_a_supprimer"] = livre["id"]

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
