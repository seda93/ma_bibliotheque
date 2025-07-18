import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
from backend.database import get_sqlalchemy_engine

engine = get_sqlalchemy_engine()
st.title("📊 Statistiques de la bibliothèque")

with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM livres", conn)

if df.empty:
    st.info("Aucun livre à afficher.")
else:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Livres par genre")
        genre_count = df['genre'].value_counts()
        fig, ax = plt.subplots()
        genre_count.plot(kind='bar', ax=ax)
        ax.set_ylabel("Nombre")
        st.pyplot(fig)

    with col2:
        st.subheader("🌍 Livres par langue")
        langue_count = df['langue'].value_counts()
        fig, ax = plt.subplots()
        langue_count.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        st.pyplot(fig)

    st.subheader("📅 Répartition par année")
    annee_count = df['annee'].value_counts().sort_index()
    fig, ax = plt.subplots()
    annee_count.plot(kind='bar', ax=ax)
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de livres")
    st.pyplot(fig)
