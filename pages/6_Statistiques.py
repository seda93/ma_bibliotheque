import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend.database import get_connection

st.title("📊 Statistiques de votre bibliothèque")

def charger_data():
    try:
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM livres", conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()

df = charger_data()

if df.empty:
    st.info("La base est vide.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Livres par langue")
        lang_counts = df["langue"].value_counts()
        st.bar_chart(lang_counts)

    with col2:
        st.subheader("📅 Livres par année")
        annee_counts = df["annee"].value_counts().sort_index()
        st.line_chart(annee_counts)

    st.subheader("📖 Livres par genre")
    genre_counts = df["genre"].value_counts().head(10)
    fig, ax = plt.subplots()
    genre_counts.plot(kind="barh", ax=ax)
    st.pyplot(fig)
