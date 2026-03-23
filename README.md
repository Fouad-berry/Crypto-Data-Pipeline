# Crypto Data Pipeline

Ce projet automatise la collecte, le stockage et l’analyse de données de marché crypto en temps réel via l’API CoinGecko.

## Structure
- `scripts/fetch_crypto.py` : Script ETL (Extraction, Transformation, Chargement SQL)
- `database/crypto.db` : Base de données SQLite
- `notebooks/analysis.ipynb` : Analyses et visualisations
- `dashboard/` : Tableau de bord (à venir)

## Lancement rapide
1. Exécute `python scripts/fetch_crypto.py`
2. Explore les données dans le notebook `notebooks/analysis.ipynb`

## À venir
- Automatisation (cron ou boucle Python)
- Dashboard interactif
