import streamlit as st
from PIL import Image
import os

st.set_page_config(
    page_title="Ma bibliothèque pastel",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# # Charger une image/logo si tu en as une
# image_path = "data/logo.png"  # à remplacer par ton image réelle
# if os.path.exists(image_path):
#     st.image(Image.open(image_path), width=150)

st.title("📚 Bienvenue dans votre Bibliothèque personnelle")

st.markdown("""
Bienvenue dans votre espace personnel de gestion de livres.  
Cette application vous permet de **gérer facilement votre collection** à travers une interface claire et intuitive.

---

### 🔧 Fonctions principales :

- 📄 **Accueil** : cette page !
- 📚 **Liste des livres** : aperçu complet avec tri et résumé.
- 🔍 **Recherche** : trouvez un livre par titre, auteur, langue, genre...
- ➕ **Ajout** : formulaire manuel ou via ISBN (données récupérées automatiquement).
- ✏️ **Modifier / Supprimer** : gérez vos fiches existantes.
- 📥 **Importer CSV** : ajoutez plusieurs livres à la fois.
- 📤 **Exporter la base** : sauvegardez tout en CSV.
- 📊 **Statistiques** : visualisez la langue, l’année, les genres...

---

### 💡 Astuces

- Vous pouvez **ajouter une image de couverture** locale ou par lien.
- Tous les livres sont stockés dans une base SQLite (`data/livres.db`).
- Vos données vous appartiennent — vous pouvez les exporter à tout moment.

---

👨‍💻 *Développé avec amour en Python + Streamlit.*
""")