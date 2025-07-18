import streamlit as st
import pandas as pd
from PIL import Image
from backend.database import get_sqlalchemy_engine
from sqlalchemy import text

st.markdown("""
<style>
    .stButton>button {
        border-radius: 8px;
        padding: 6px 16px;
        margin: 3px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📚 Ma bibliothèque")

def charger_donnees():
    engine = get_sqlalchemy_engine()
    with engine.connect() as conn:
        df = pd.read_sql_query("SELECT * FROM livres", conn)
    return df

def supprimer_livre(livre_id):
    engine = get_sqlalchemy_engine()
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM livres WHERE id = :id"), {"id": livre_id})
        conn.commit()

df_livres = charger_donnees()

if df_livres.empty:
    st.info("Aucun livre trouvé dans la base de données.")
else:
    df_livres["id"] = df_livres["id"].astype(int)  # Force int pour comparaison

    colonnes_triables = ["titre", "auteurs", "genre", "langue", "annee"]
    tri = st.selectbox("Trier par :", colonnes_triables)
    ordre = st.radio("Ordre :", ["Croissant", "Décroissant"], horizontal=True)
    df_livres_sorted = df_livres.sort_values(by=tri, ascending=(ordre == "Croissant"))

    for _, livre in df_livres_sorted.iterrows():
        with st.container():
            cols = st.columns([1, 3])
            if livre["image"]:
                if livre["image"].startswith("http"):
                    cols[0].image(livre["image"], width=120)
                else:
                    try:
                        img = Image.open(livre["image"])
                        cols[0].image(img, width=120)
                    except:
                        cols[0].markdown("⚠️ Image non trouvée")
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
                    if st.button("📝 Modifier", key=f"modif_{livre['id']}"):
                        st.session_state["livre_a_modifier"] = livre["id"]
                        st.switch_page("pages/4_Modifier_supprimer.py")

                with col_suppr:
                    if st.button("🗑️ Supprimer", key=f"suppr_{livre['id']}"):
                        st.session_state["livre_a_supprimer"] = int(livre["id"])

            # CONFIRMATION SUPPRESSION
            if st.session_state.get("livre_a_supprimer") == int(livre["id"]):
                st.warning(f"⚠️ Confirmer la suppression de « {livre['titre']} » ?")
                col_ok, col_cancel = st.columns([1, 1])
                with col_ok:
                    if st.button("✅ Oui, supprimer", key=f"confirm_{livre['id']}"):
                        supprimer_livre(int(livre["id"]))
                        st.success("Livre supprimé.")
                        st.session_state.pop("livre_a_supprimer", None)
                        st.rerun()
                with col_cancel:
                    if st.button("❌ Annuler", key=f"cancel_{livre['id']}"):
                        st.session_state.pop("livre_a_supprimer", None)
                        st.info("Suppression annulée.")

            st.markdown("---")
