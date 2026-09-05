# 🗺️ Projet Kayak : Data Pipeline & Moteur de Recommandation 🚀

Bienvenue dans mon projet final de Data Engineering ! Ce projet a été réalisé dans le cadre de ma certification RNCP pour simuler la construction d'une infrastructure de données complète pour l'équipe produit de Kayak.

## 🎯 Contexte Business
L'équipe produit de Kayak souhaite proposer une nouvelle fonctionnalité : recommander de manière intelligente **les meilleures destinations** et **les meilleurs hôtels**.
L'objectif est de construire un pipeline **ETL (Extract, Transform, Load)** automatisé qui récupère les données de météo et d'hôtels, les nettoie, les stocke de manière sécurisée dans le Cloud (AWS), et permet de visualiser les résultats finaux sur des cartes interactives.

## 🏗️ Architecture du Pipeline ETL
1. **Scraping & Ingestion (Extract) :** Récupération des données météo via l'API OpenWeather, et scraping des hôtels sur Booking.com à l'aide de Scrapy/Selenium.
2. **Data Lake S3 (Storage) :** Sauvegarde des données brutes au format `.csv` sur un bucket sécurisé **AWS S3** via `boto3`.
3. **Data Warehouse RDS (Load) :** Envoi des données nettoyées et structurées dans une base de données **PostgreSQL** (Free Tier) hébergée sur **AWS RDS** via `SQLAlchemy`.
4. **Data Visualization :** Génération de cartes de recommandations interactives avec **Plotly** directement depuis nos données.

## 🛠️ Installation & Exécution par le Jury
```bash
git clone https://github.com/Carelle777/kayak_project.git
cd kayak_project
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt