
# 📚 Ma Bibliothèque Personnelle

Une application web simple et élégante pour gérer tous vos livres, développée avec Python et [Streamlit](https://streamlit.io/).  
Elle fonctionne en local, sans besoin de serveur externe ni d’internet une fois installée.

---

## ✨ Fonctionnalités principales

- 📋 Ajouter des livres manuellement ou via ISBN
- 🔎 Rechercher dans votre collection (titre, auteur, genre, langue…)
- 🖼️ Gérer les images de couverture (URL ou fichiers uploadés)
- ✏️ Modifier ou supprimer des livres existants
- 📥 Importer un ensemble de livres via un fichier CSV
- 📤 Exporter toute votre base (CSV complet)
- 📊 Visualiser des statistiques : langue, année, genre, etc.
- 🗃️ Base de données locale persistante (SQLite)

---

## 🖼️ Aperçu visuel

*(Ajoutez ici une ou plusieurs captures d’écran si vous le souhaitez)*

---

## 📁 Structure du projet

```
ma_bibliotheque/
├── Home.py                        # Page d'accueil principale
├── app.py (facultatif)
├── data/
│   ├── livres.db                  # Base de données SQLite
│   ├── livres_base.db             # base initiale (commitable)
│   └── images/                    # Images uploadées (couvertures)
├── backend/
│   ├── database.py                # Connexion à SQLite
│   ├── isbn_lookup.py             # Récupération de données par ISBN
│   └── utils.py                   # Fonctions utilitaires diverses
├── pages/                         # Pages Streamlit
│   ├── 1_Liste_des_livres.py
│   ├── 2_Recherche.py
│   ├── 3_Ajout_livre.py
│   ├── 4_Modifier_supprimer.py
│   ├── 5_Importer_Export.py
│   └── 6_Statistiques.py
├── requirements.txt              # Dépendances Python
└── README.md                     # Ce fichier
```

---

## ☁️ Déploiement Streamlit Cloud

L’application recrée la base `livres.db` à partir de `livres_base.db` si elle n’existe pas.  
Cela garantit la persistance du projet même après déploiement cloud.

---

## ⚙️ Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/ma_bibliotheque.git
cd ma_bibliotheque
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate         # Mac/Linux
venv\Scripts\activate          # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

> Sinon, installe-les manuellement :
```bash
pip install streamlit pandas matplotlib pillow requests
```

---

## 🚀 Lancer l'application

Depuis la racine du projet :

```bash
streamlit run Home.py
```

Puis ouvre automatiquement dans ton navigateur : [http://localhost:8501](http://localhost:8501)

---

## 📄 Format CSV attendu pour l'import

Tu peux importer plusieurs livres via un fichier `.csv` avec les colonnes suivantes :

```
titre, auteurs, serie, annee, genre, langue, isbn, editeur, collection, resume, emplacement, image
```

Un bouton dans l’app permet de télécharger un fichier modèle.

---

## 💾 Sauvegarde des données

Tous les livres sont stockés dans :

```
data/livres.db
```

Les images de couverture uploadées localement sont dans :

```
data/images/
```

---

## 👨‍💻 Auteur

Projet développé par **seda93**  
Contact : [seda.ozturk39@gmail.com]  
Licence : usage personnel ou éducatif libre.

---

## ✅ Idées d'améliorations futures

- 📱 Adaptation mobile responsive
- 🔒 Authentification multi-utilisateur
- 🧾 Export PDF par fiche livre
- 📆 Gestion d’historique de lectures / emprunts
