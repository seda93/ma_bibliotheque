import requests

def fetch_from_openlibrary(isbn):
    try:
        res = requests.get(f"https://openlibrary.org/isbn/{isbn}.json")
        if res.status_code != 200:
            return None
        data = res.json()

        # Titre
        titre = data.get("title", "")

        # Année
        annee = data.get("publish_date", "")

        # Auteurs (besoin de fetch par ID)
        auteurs = []
        for a in data.get("authors", []):
            auth_id = a.get("key", "").split("/")[-1]
            auth_res = requests.get(f"https://openlibrary.org/authors/{auth_id}.json")
            if auth_res.status_code == 200:
                auteurs.append(auth_res.json().get("name", ""))

        return {
            "titre": titre,
            "auteurs": ", ".join(auteurs),
            "annee": annee,
            "isbn": isbn,
            "langue": "",  # pas toujours présent
            "editeur": "",
            "genre": "",
            "serie": "",
            "collection": "",
            "resume": data.get("description", {}).get("value") if isinstance(data.get("description"), dict) else data.get("description", ""),
            "emplacement": "",
            "image": f"https://covers.openlibrary.org/b/isbn/{isbn}-L.jpg"
        }
    except:
        return None

def fetch_from_googlebooks(isbn):
    try:
        res = requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}")
        if res.status_code != 200:
            return None
        items = res.json().get("items")
        if not items:
            return None
        data = items[0]["volumeInfo"]

        return {
            "titre": data.get("title", ""),
            "auteurs": ", ".join(data.get("authors", [])) if "authors" in data else "",
            "annee": data.get("publishedDate", ""),
            "isbn": isbn,
            "langue": data.get("language", ""),
            "editeur": data.get("publisher", ""),
            "genre": ", ".join(data.get("categories", [])) if "categories" in data else "",
            "serie": "",
            "collection": "",
            "resume": data.get("description", ""),
            "emplacement": "",
            "image": data.get("imageLinks", {}).get("thumbnail", "")
        }
    except:
        return None

def fetch_book_info(isbn):
    # 1. OpenLibrary d’abord
    info = fetch_from_openlibrary(isbn)
    
    # 2. Google Books en complément
    supplement = fetch_from_googlebooks(isbn)

    if not info and not supplement:
        return None

    # Fusion : priorité à OpenLibrary, complété par Google
    combined = info or {}
    for key, val in (supplement or {}).items():
        if not combined.get(key):
            combined[key] = val

    return combined
