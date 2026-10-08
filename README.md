# 🗺️ Projet Kayak — Où partir ? Où dormir ?

Projet de certification RNCP (Jedha Fullstack) — **Carelle Nouko**

## 1. À quoi sert ce projet ?

Kayak veut conseiller ses clients : **quelles sont les meilleures destinations en France ces prochains jours (selon la météo)**, et **quels sont les meilleurs hôtels** à cet endroit ?

Pour répondre, j'ai construit un petit « tuyau de données » (on dit un *pipeline*) en 5 étapes :

1. je trouve **où sont** 35 villes (leurs coordonnées GPS) ;
2. je récupère **la météo** de chaque ville ;
3. je choisis **les 5 villes avec la meilleure météo** ;
4. je récupère **les hôtels** de ces villes sur Booking.com ;
5. je range le résultat dans un fichier, je l'envoie dans le cloud (Amazon AWS) et je l'affiche sur **deux cartes**.

## 2. Ce que j'ai fait, étape par étape

| # | Étape | Outil utilisé | Résultat |
|---|---|---|---|
| 1 | Trouver les coordonnées GPS des 35 villes imposées | Nominatim (service gratuit d'OpenStreetMap) | latitude + longitude de chaque ville |
| 2 | Récupérer la météo des 5 prochains jours | OpenWeather (fournit une prévision toutes les 3 heures) | température moyenne et probabilité de pluie moyenne |
| 3 | Calculer un **score météo** et garder le Top 5 | pandas | `kayak_weather_dataset.csv` et `top_5_destinations.csv` |
| 4 | Récupérer les hôtels (nom, note, lien) | Selenium (un robot qui ouvre Chrome et lit les pages Booking) | `hotels_raw.json` |
| 5 | Nettoyer les notes et fusionner hôtels + météo | pandas | `kayak_final_dataset.csv` |
| 6 | Dessiner deux cartes | Plotly | Top 5 des destinations, Top 20 des hôtels |
| 7 | Envoyer le fichier sur le cloud AWS (S3, puis RDS) | boto3, SQLAlchemy | voir la section 5 |

### Mon score météo
`score = température moyenne − (probabilité de pluie × 10)`

Plus le score est **élevé**, plus la météo est agréable : on aime la chaleur et on enlève des points quand il risque de pleuvoir. La probabilité de pluie va de 0 à 1, je la multiplie par 10 pour qu'elle pèse vraiment dans le calcul. C'est **mon choix de départ** (une hypothèse simple), pas une vérité absolue : un autre score donnerait un autre classement.

### Nettoyage des notes
Booking écrit « Avec une note de 8,4 ». Je garde seulement le nombre, je remplace la virgule par un point, et je le transforme en vrai nombre : `8.4`. Sans ça, on ne pourrait pas trier les hôtels du mieux noté au moins bien noté.

## 3. Résultats (photo prise le 8 octobre 2026)

La météo change tous les jours. J'ai donc **figé une photo** (les fichiers CSV du dossier `src/`), prise le 8 octobre 2026.

**Top 5 des destinations :**

| Rang | Ville | Température moyenne | Score météo |
|---|---|---|---|
| 1 | Bayonne | 18,0 °C | 17,34 |
| 2 | Collioure | 17,3 °C | 17,28 |
| 3 | Biarritz | 18,0 °C | 17,27 |
| 4 | Bormes-les-Mimosas | 16,8 °C | 16,44 |
| 5 | Saintes-Maries-de-la-Mer | 16,0 °C | 15,77 |

**Hôtels :** mon robot a collecté **125 hôtels le 26 août** (25 hôtels pour chacune de 5 villes). Après fusion avec le Top 5, il me reste **100 hôtels** : 25 pour Bayonne, 25 pour Biarritz, 25 pour Collioure et 25 pour Saintes-Maries-de-la-Mer.

⚠️ **Bormes-les-Mimosas n'a aucun hôtel** : c'est une ville du Top 5 d'aujourd'hui, mais ma collecte du mois d'août ne la contenait pas, et Booking a bloqué mon robot quand j'ai voulu le relancer (voir les limites).

## 4. Les deux cartes
- **Carte 1** : les 5 meilleures destinations selon la météo.
- **Carte 2** : les 20 hôtels les mieux notés parmi mes 100 hôtels.

Les hôtels n'ont pas leur vraie adresse GPS dans mes données, seulement celle de leur **ville**. Pour les voir séparément, je les décale très légèrement autour du centre-ville : **leur position sur la carte est donc approximative.**

## 5. Le cloud AWS

| Élément | Rôle | État |
|---|---|---|
| **S3** (bucket `kayak-datalake-jedha-carelle-2026`, région `eu-west-3`) | « Garage » du projet : on y dépose le fichier final tel quel | ✅ bucket créé |
| **RDS PostgreSQL** (table `destinations_hotels`) | Base de données où l'on pose des questions en SQL | ⚠️ à créer le 24 octobre, pour limiter les frais, puis supprimée après le jury |

*(Cette section sera complétée avec mes captures d'écran et mes requêtes SQL une fois la base RDS créée.)*

## 6. Lancer le projet

```bash
git clone https://github.com/Carelle777/kayak_project.git
cd kayak_project
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Ouvrir ensuite le fichier `.env` et écrire ma clé OpenWeather après `OPENWEATHER_API_KEY=` (les clés AWS ne sont nécessaires que pour l'étape cloud). Puis ouvrir `src/kayak_data_pipeline.ipynb` dans VS Code.

> ⚠️ La météo est « en direct » : si on relance la partie météo, le Top 5 change. Les fichiers CSV fournis sont la photo du 8 octobre 2026, ils servent de référence.

**Les clés secrètes ne sont jamais dans le code** : elles sont dans le fichier `.env`, que Git ignore.

## 7. Contenu du dossier

```
kayak_project/
├── README.md                    ← ce fichier
├── requirements.txt             ← la liste des outils Python à installer
├── .env.example                 ← modèle du fichier de clés (sans aucune clé)
├── .gitignore                   ← fichiers que Git ne doit jamais envoyer
└── src/
    ├── kayak_data_pipeline.ipynb  ← le notebook principal (toutes les étapes)
    ├── booking_selenium.py        ← le robot qui collecte les hôtels
    ├── hotels_raw.json            ← hôtels bruts collectés le 26 août (125)
    ├── kayak_weather_dataset.csv  ← météo des 35 villes (photo du 8 octobre)
    ├── top_5_destinations.csv     ← les 5 meilleures villes
    └── kayak_final_dataset.csv    ← fichier final : hôtels + météo (100 hôtels)
```

## 8. Limites (ce que je sais que le projet ne fait pas bien)

- **Booking bloque les robots.** Après ma collecte réussie du 26 août, il a bloqué mes essais suivants. J'ai donc gardé les données de la collecte réussie. `booking_selenium.py` montre la méthode utilisée ; il pourrait ne plus fonctionner aujourd'hui.
- **Pas d'hôtel pour Bormes-les-Mimosas** (voir section 3).
- **Position des hôtels approximative** (voir section 4).
- **La météo est une prévision à 5 jours**, pas une moyenne sur plusieurs années.
- **Le score météo est un choix personnel**, il pourrait être amélioré (ajouter le vent, l'ensoleillement…).

## 9. Lexique (mots techniques expliqués simplement)

| Mot | Pour un enfant | En vrai |
|---|---|---|
| **Pipeline** | Une chaîne de montage : les données entrent d'un côté, ressortent propres de l'autre | Suite d'étapes automatiques de collecte → nettoyage → stockage |
| **API** | Un guichet : on pose une question précise, on reçoit une réponse | Service qui répond à des requêtes envoyées par un programme |
| **Scraping** | Un robot qui lit une page web et recopie les infos | Extraction automatique de données d'une page web |
| **Selenium** | Le robot qui pilote Chrome à ma place | Outil qui automatise un navigateur |
| **Data Lake (S3)** | Un grand garage où l'on range les fichiers tels quels | Stockage cloud de fichiers bruts |
| **Data Warehouse (RDS)** | Une bibliothèque bien rangée où l'on retrouve vite une réponse | Base de données relationnelle interrogeable en SQL |
| **SQL** | La langue pour poser des questions à une base de données | Langage de requêtes |
| **`.env`** | Un coffre-fort pour mes mots de passe | Fichier de variables secrètes, ignoré par Git |
| **Photo (snapshot)** | Une image de la météo à un jour précis | Jeu de données figé à une date |
