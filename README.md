# Crypto Data Pipeline

Ce projet automatise la collecte, le stockage et l’analyse de données de marché crypto en temps réel via l’API CoinGecko.

## Structure
- `scripts/fetch_crypto.py` : Script ETL (Extraction, Transformation, Chargement SQL)
- `database/crypto.db` : Base de données SQLite
- `notebooks/analysis.ipynb` : Analyses et visualisations
- `dashboard/` : Tableau de bord (à venir)

## Lancement rapide

### 1. Crée un environnement virtuel Python (recommandé)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Exécute le pipeline ETL
```bash
python scripts/fetch_crypto.py
```

### 3. Explore les données dans le notebook
Ouvre `notebooks/analysis.ipynb` dans Jupyter ou VS Code.

## Automatisation de la collecte (cron)

Pour automatiser la collecte toutes les 5 minutes avec cron :

1. Ouvre le crontab :
	```bash
	crontab -e
	```
2. Ajoute la ligne suivante :
	```
	*/5 * * * * cd /chemin/vers/crypto-data-pipeline && /chemin/vers/venv/bin/python scripts/fetch_crypto.py
	```
	Remplace `/chemin/vers/crypto-data-pipeline` et `/chemin/vers/venv` par tes chemins réels.

Cela exécutera le script toutes les 5 minutes automatiquement.

## À venir
- Dashboard interactif
