import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import text
from backend.database import get_sqlalchemy_engine

# --- STYLES GLOBAUX PASTEL ---
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Arial', sans-serif;
            background-color: #fdf6f0;
            color: #333;
        }
        h1, h2 {
            color: #6c5b7b;
        }
        .block-container {
            padding: 2rem;
        }
        .stMarkdown > div {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Statistiques sur la bibliothèque")

engine = get_sqlalchemy_engine()
df = pd.read_sql("SELECT * FROM livres", engine)

if df.empty:
    st.info("Aucun livre dans la base.")
    st.stop()

# Palette pastel
pastel_colors = plt.cm.Pastel1.colors + plt.cm.Pastel2.colors

# Répartition par langue
st.subheader("🗣 Répartition par langue")
langue_counts = df["langue"].value_counts().head(10)
fig1, ax1 = plt.subplots(figsize=(3.5, 2))
ax1.pie(langue_counts.values, labels=langue_counts.index, autopct="%1.1f%%", startangle=140, colors=pastel_colors)
ax1.axis("equal")
st.pyplot(fig1)

# Répartition par genre
st.subheader("📚 Répartition par genre")
genre_counts = df["genre"].value_counts().head(10)
fig2, ax2 = plt.subplots(figsize=(4, 2))
ax2.bar(genre_counts.index, genre_counts.values, color=pastel_colors[:len(genre_counts)])
ax2.tick_params(axis="x", labelrotation=45, labelsize=7)
ax2.tick_params(axis="y", labelsize=7)
plt.tight_layout()
st.pyplot(fig2)

# Répartition par année
st.subheader("📅 Répartition par année")
df["annee"] = pd.to_numeric(df["annee"], errors="coerce")
year_counts = df["annee"].dropna().astype(int).value_counts().sort_index()
fig3, ax3 = plt.subplots(figsize=(4, 2))
ax3.plot(year_counts.index, year_counts.values, marker='o', linestyle='-', color="#a3c9a8")
ax3.set_xlabel("Année", fontsize=7)
ax3.set_ylabel("Nombre de livres", fontsize=7)
ax3.tick_params(axis="x", labelsize=7)
ax3.tick_params(axis="y", labelsize=7)
plt.tight_layout()
st.pyplot(fig3)