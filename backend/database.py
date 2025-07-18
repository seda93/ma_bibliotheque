from sqlalchemy import create_engine
import streamlit as st

def get_sqlalchemy_engine():
    return create_engine(
        f"postgresql+psycopg2://{st.secrets['user']}:{st.secrets['password']}@{st.secrets['host']}:{st.secrets['port']}/{st.secrets['dbname']}"
    )
