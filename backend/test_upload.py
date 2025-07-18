from supabase_client import upload_image_to_bucket

with open("data/images/grimm.jpg", "rb") as f:
    image_url = upload_image_to_bucket(f, "grimm.jpg")
    if image_url:
        print("✅ Upload réussi :", image_url)
    else:
        print("❌ Échec de l’envoi.")
