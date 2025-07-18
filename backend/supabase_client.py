import requests
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
BUCKET = "images"

def upload_image_to_bucket(image_file, image_name):
    url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET}/{image_name}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/octet-stream"
    }

    response = requests.put(url, headers=headers, data=image_file.read())
    
    if response.status_code == 200:
        return f"{SUPABASE_URL}/storage/v1/object/public/{BUCKET}/{image_name}"
    else:
        print("Erreur upload :", response.status_code, response.text)
        return None
