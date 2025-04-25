# AI Article Review

## Description

**AI Article Review** est un script d'automatisation en Python permettant d'extraire des articles publiés la veille depuis une source d'actualités, de les filtrer en fonction d'un thème (par exemple, Business , l'Intelligence Artificielle...), puis de stocker les articles pertinents dans une base de données SQLite locale. L'outil propose également une interface Streamlit pour sélectionner les articles et générer un fichier PDF.

---

## Fonctionnalités

- **Extraction des articles** : Récupère les articles publiés la veille depuis une source d'actualités.
- **Filtrage des articles** : Filtre les articles liés à un thème spécifique (par exemple, IA).
- **Stockage dans une base de données** : Sauvegarde des articles pertinents dans une base de données SQLite.
- **Interface Streamlit** : Permet à l'utilisateur de sélectionner les articles et de générer un PDF.
- **Téléchargement PDF** : Télécharge un fichier PDF contenant les articles sélectionnés.

---

## Prérequis

vant de lancer le projet, assurez-vous de disposer des éléments suivants :

- **Python 3.x** installé sur votre machine.
- **Clé API OpenAI** : Vous devez avoir une clé API valide pour interagir avec OpenAI (pour le filtrage des articles).

## Installation

### 1. Clonez le dépôt

Si vous n'avez pas encore cloné le projet, exécutez la commande suivante :

git clone https://github.com/votre-utilisateur/ai-article-review.git

#### 2. Créez un environnement virtuel

Dans le répertoire du projet, créez un environnement virtuel :

python -m venv venv

### 3. Activez l'environnement virtuel

.\venv\Scripts\activate

### 4. Installez les dépendances

pip install -r requirements.txt

##  Configuration

- **Extraction des articles**

Créez un fichier .env à la racine du projet et ajoutez-y votre clé API OpenAI :

OPENAI_API_KEY=your-openai-api-key

## Lancer l'application

### 1. Exécutez le script d'extraction et d'interface Streamlit

Pour démarrer l'application et exécuter le processus d'extraction et de filtrage des articles, utilisez la commande suivante :

streamlit run app.py

##  Structure du projet

ai-article-review/

├── app.py                # Application Streamlit pour l'interface utilisateur

├── fetcher.py            # Script pour extraire les articles depuis une source d'actualités

├── db.py                 # Script pour gérer la base de données SQLite

├── articles.db           # Base de données SQLite contenant tous les articles extraits

├── filtered_articles.db  # Base de données contenant les articles filtrés

├── .env                  # Fichier de configuration contenant la clé API OpenAI

├── .gitignore            # Fichier pour ignorer les fichiers sensibles (comme .env)

├── requirements.txt      # Liste des dépendances du projet

└── README.md             # Documentation du projet

## Licence

Ce projet est sous licence MIT

