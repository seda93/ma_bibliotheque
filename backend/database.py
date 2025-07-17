import sqlite3

def create_connection():
    return sqlite3.connect("data/livres.db")

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS livres (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT,
        auteurs TEXT,
        serie TEXT,
        annee TEXT,
        genre TEXT,
        langue TEXT,
        isbn TEXT UNIQUE,
        editeur TEXT,
        collection TEXT,
        resume TEXT,
        emplacement TEXT,
        image TEXT
    );
    """)
    conn.commit()
    conn.close()
