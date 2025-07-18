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

engine = get_sqlalchemy_engine()

st.title("📊 Statistiques de la bibliothèque")

def fetch_data():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM livres"))
        return pd.DataFrame(result.fetchall(), columns=result.keys())

df = fetch_data()

if df.empty:
    st.warning("Aucune donnée disponible.")
    st.stop()

# --- LANGUE ---
st.subheader("🌍 Répartition par langue")
langue_counts = df['langue'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(langue_counts, labels=langue_counts.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Pastel1.colors)
ax1.axis('equal')
st.pyplot(fig1)

# --- GENRE ---
st.subheader("📚 Répartition par genre")
genre_counts = df['genre'].value_counts()
fig2, ax2 = plt.subplots()
ax2.bar(genre_counts.index, genre_counts.values, color=plt.cm.Pastel2.colors)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
st.pyplot(fig2)

# --- ANNÉE ---
st.subheader("📅 Répartition par année")
df["annee"] = pd.to_numeric(df["annee"], errors="coerce")
year_counts = df["annee"].dropna().astype(int).value_counts().sort_index()
fig3, ax3 = plt.subplots()
ax3.plot(year_counts.index, year_counts.values, marker='o', linestyle='-', color='#a3c9a8')
ax3.set_xlabel("Année")
ax3.set_ylabel("Nombre de livres")
st.pyplot(fig3)
