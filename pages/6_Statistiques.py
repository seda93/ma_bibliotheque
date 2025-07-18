import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend.database import get_sqlalchemy_engine

engine = get_sqlalchemy_engine()
df = pd.read_sql("SELECT * FROM livres", engine)

st.title("📊 Statistiques de la bibliothèque")

if df.empty:
    st.warning("Aucune donnée à afficher.")
else:
    st.subheader("📘 Livres par langue")
    langue_count = df["langue"].fillna("Inconnue").value_counts()
    fig1, ax1 = plt.subplots()
    langue_count.plot.pie(autopct="%1.1f%%", ax=ax1)
    ax1.set_ylabel("")
    st.pyplot(fig1)

    st.subheader("📆 Livres par année")
    annee_count = df["annee"].fillna("Inconnue").value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    annee_count.plot(kind="bar", ax=ax2)
    st.pyplot(fig2)

    st.subheader("🏷️ Livres par genre")
    genre_count = df["genre"].fillna("Inconnu").value_counts()
    fig3, ax3 = plt.subplots()
    genre_count.plot(kind="barh", ax=ax3)
    st.pyplot(fig3)
