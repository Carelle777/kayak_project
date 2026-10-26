"""Pose à la base RDS les requêtes du fichier sql/requetes_rds.sql et affiche les résultats."""

import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Les secrets viennent du fichier .env, jamais écrits dans le code
load_dotenv("../.env")
mot_de_passe = os.getenv("RDS_PASSWORD")
adresse = os.getenv("RDS_ENDPOINT")
engine = create_engine(f"postgresql://postgres:{mot_de_passe}@{adresse}:5432/postgres")

# Chaque requête est séparée de la suivante par un point-virgule
with open("../sql/requetes_rds.sql", encoding="utf-8") as fichier:
    requetes = fichier.read().split(";")

for requete in requetes:
    requete = requete.strip()
    if not requete:
        continue
    titre = requete.splitlines()[0].lstrip("- ")
    print("\n---", titre, "---")
    print(pd.read_sql(requete, engine).to_string(index=False))
