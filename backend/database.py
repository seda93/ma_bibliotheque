from sqlalchemy import create_engine
import os
import streamlit as st

# 🔐 Fonction pour obtenir une connexion SQLAlchemy à Supabase (PostgreSQL)
def get_sqlalchemy_engine():
    return create_engine(
        f"postgresql://{st.secrets['user']}:{st.secrets['password']}@{st.secrets['host']}:{st.secrets['port']}/{st.secrets['dbname']}",
        connect_args={"sslmode": "require"}
    )
