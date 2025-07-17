import streamlit as st
import pandas as pd
import sqlite3

def exporter_base():
    conn = sqlite3.connect("data/livres.db")
    df = pd.read_sql_query("SELECT * FROM livres", conn)
    conn.close()
    return df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📤 Exporter toute la base de données au format CSV",
    data=exporter_base(),
    file_name="ma_bibliotheque_complete.csv",
    mime="text/csv"
)
