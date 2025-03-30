# Dataset Management API

Une application complète pour gérer, analyser et visualiser des datasets CSV.

## À propos du projet

Ce projet est composé de deux parties principales :
- Une **API REST** construite avec FastAPI pour le traitement et l'analyse des datasets
- Un **client CLI** développé avec Typer pour interagir facilement avec l'API

L'application permet de télécharger des datasets CSV, de les manipuler, d'extraire des statistiques, d'exporter en Excel et de générer des visualisations sous forme d'histogrammes.

## Prérequis

- Un environnement virtuel (recommandé)

## Installation

1. Clonez le dépôt et naviguez dans le répertoire du projet :

```bash
git clone <url-du-repo>
cd API-Hiring
```

2. Créez et activez un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## API Server

### Démarrage du serveur

Pour lancer l'API en mode développement avec rechargement automatique :

```bash
uvicorn app.main:app --reload
```

Le serveur démarrera par défaut sur `http://127.0.0.1:8000`.

### Documentation API

Une fois le serveur démarré, vous pouvez accéder à la documentation interactive :
- Swagger UI : `http://127.0.0.1:8000/docs`
- ReDoc : `http://127.0.0.1:8000/redoc`

### Endpoints

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/datasets/` | Liste tous les datasets disponibles |
| POST | `/datasets/` | Crée un nouveau dataset à partir d'un fichier CSV |
| GET | `/datasets/{dataset_id}` | Récupère les informations d'un dataset spécifique |
| DELETE | `/datasets/{dataset_id}` | Supprime un dataset |
| GET | `/datasets/{dataset_id}/excel/` | Exporte le dataset au format Excel |
| GET | `/datasets/{dataset_id}/stats/` | Récupère les statistiques du dataset |
| GET | `/datasets/{dataset_id}/plot/` | Génère un PDF avec des histogrammes du dataset |

## Client CLI

Le client CLI offre une interface en ligne de commande pour interagir avec l'API.

### Commandes disponibles

#### Commande test

```bash
# Affiche un message de bienvenue
python client/main.py hello --name "World"
# Version courte
python client/main.py hello -n "World"
```

#### Gestion des datasets

```bash
# Création d'un dataset (upload CSV)
python client/main.py create --file-path "sample_data.csv"
# Version courte
python client/main.py create -f "sample_data.csv"

# Liste de tous les datasets
python client/main.py list

# Affichage des informations d'un dataset
python client/main.py info --dataset-id "ID_DU_DATASET"
# Version courte
python client/main.py info -d "ID_DU_DATASET"

# Suppression d'un dataset
python client/main.py delete --dataset-id "ID_DU_DATASET"
# Version courte
python client/main.py delete -d "ID_DU_DATASET"
```

#### Analyse et exportation

```bash
# Export Excel du dataset
python client/main.py export_excel --dataset-id "ID_DU_DATASET" --output-path "mon_dataset.xlsx"
# Version courte
python client/main.py export_excel -d "ID_DU_DATASET" -o "mon_dataset.xlsx"

# Affichage des statistiques du dataset
python client/main.py stats --dataset-id "ID_DU_DATASET"
# Version courte
python client/main.py stats -d "ID_DU_DATASET"

# Téléchargement du PDF des histogrammes
python client/main.py plot --dataset-id "ID_DU_DATASET" --output-path "histos.pdf"
# Version courte
python client/main.py plot -d "ID_DU_DATASET" -o "histos.pdf"
```

### Aide intégrée

Chaque commande dispose d'une aide détaillée accessible via :

```bash
python client/main.py --help
python client/main.py <commande> --help
```

## Dépendances principales

- FastAPI : Framework API REST haut niveau
- Typer : Bibliothèque CLI basée sur Click
- Pandas : Manipulation et analyse de données
- Matplotlib : Génération de graphiques
- Openpyxl : Export Excel
- Uvicorn : Serveur ASGI pour FastAPI
