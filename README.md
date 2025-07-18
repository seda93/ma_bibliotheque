
# 📚 Ma Bibliothèque – Application Streamlit

Cette application vous permet de gérer votre bibliothèque personnelle de manière élégante et interactive.

---

## 🚀 Fonctionnalités principales

- 🔎 Rechercher des livres (par titre, auteur, genre, langue…)
- 📋 Visualiser tous les livres de la base
- ➕ Ajouter des livres manuellement ou via ISBN
- 🛠️ Modifier ou supprimer un livre
- 📁 Importer ou exporter la base de données en CSV (`5_Importer_Export.py`)
- 📊 Visualiser des statistiques (par langue, genre, année, etc.)

---

## 📁 Structure du projet

```
ma_bibliotheque/
├── backend/
│   ├── database.py
│   └── fetch_book_info.py
├── data/
│   ├── livres.db           # base active (non suivie par Git)
│   └── livres_base.db      # base initiale (commitable)
├── pages/
│   ├── 1_Liste_des_livres.py
│   ├── 2_Recherche.py
│   ├── 3_Ajout_livre.py
│   ├── 4_Importer.py
│   ├── 5_Importer_Export.py
│   └── 6_Statistiques.py
├── Home.py
└── README.md
```

---

## ☁️ Déploiement Streamlit Cloud

L’application recrée la base `livres.db` à partir de `livres_base.db` si elle n’existe pas.  
Cela garantit la persistance du projet même après déploiement cloud.

---

## 📦 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/<ton_utilisateur>/ma_bibliotheque.git
```

2. Créez un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate sous Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Lancez l’application :
```bash
streamlit run Home.py
```

---

## ✨ Crédits

Développé avec ❤️ par Seda.
