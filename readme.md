🧠 Nutriprofil


🇫🇷 Nutriprofil – Votre allié nutrition santé
Nutriprofil est une application d’analyse et de recommandation alimentaire conçue pour :

mieux comprendre les habitudes nutritionnelles des Français,

évaluer les risques sanitaires associés à certains types de consommation,

et proposer des recommandations alimentaires personnalisées via l’intelligence artificielle.

🚀 Objectifs du projet
L'application Nutriprofil repose sur trois volets complémentaires :

1. 📊 Analyse de la consommation alimentaire en France
Répartition de la consommation par catégories (produits transformés, fruits et légumes, boissons sucrées, etc.)

Évolution des tendances alimentaires (2000–2024)

Données par région, âge, sexe, etc.

2. ⚠️ Évaluation des risques pour la santé
Détection des excès : trop gras, trop sucré, trop salé

Risques de maladies : diabète, maladies cardiovasculaires, obésité, hypertension, cancer colorectal…

Prédiction par modèles de machine learning (Random Forest)

3. 🧬 Recommandations personnalisées
Analyse des apports alimentaires

Comparaison avec les recommandations officielles (PNNS, OMS…)

Suggestions de régimes équilibrés selon les objectifs santé

Debby, chatbot IA pour recommander des alternatives plus saines

🍽️ Nouveauté – Section Mes Recettes
La section "Mes Recettes" introduit une génération intelligente de recettes équilibrées, avec :

✅ Choix du type de repas : entrée, plat, dessert, menu complet, en-cas
✅ Choix du profil utilisateur : sportif, sédentaire, senior, enfant, etc.
✅ Définition de seuils nutritionnels personnalisés :

Index glycémique

Lipides

Sodium

Boissons sucrées (SSBs)

Fibres

Viandes transformées

Viandes rouges

Fruits

✅ Génération automatique de recettes avec GPT-4 (OpenAI)
✅ Sauvegarde et suppression des recettes personnalisées
✅ Traduction possible de l’interface :
🇫🇷 Français (par défaut), 🇬🇧 Anglais, 🇪🇸 Espagnol, 🇳🇱 Néerlandais, 🇩🇪 Allemand

Les recettes sont stockées dans recettes/recettes.csv
L’historique est rattaché à chaque utilisateur connecté

🛠️ Technologies utilisées
Python : Pandas, NumPy, Scikit-learn, Joblib

Streamlit : pour l’interface web interactive

SQLite : base de données utilisateurs

Plotly / Matplotlib / Seaborn : visualisations

OpenAI GPT-4 : génération de recettes intelligentes

API & Données : INSEE, CIQUAL, Santé Publique France

🇬🇧 Nutriprofil – Your Smart Nutrition Assistant
Nutriprofil is a food analysis and recommendation app built to:

understand French food consumption trends,

assess health risks,

and generate personalized diet suggestions using AI.

🚀 Project Goals
The application includes three main modules:

1. 📊 Food Consumption Analysis in France
Category breakdown: processed foods, fruits, vegetables, sugary drinks...

Evolution of trends over time (2000–2024)

Segmentation by age, gender, region, etc.

2. ⚠️ Health Risk Assessment
Detection of excess: sugar, fat, salt

Risk mapping: diabetes, cardiovascular diseases, obesity, hypertension, colorectal cancer…

ML-powered risk prediction (Random Forest)

3. 🧬 Personalized Recommendations
Food diary analysis

Comparison with official guidelines (WHO, PNNS…)

Smart recommendations based on user profile and goals

Debby, the AI nutrition chatbot for smart food alternatives

🍽️ New – My Recipes Section
This section introduces AI-powered recipe generation with:

✅ Meal type selection: starter, main dish, dessert, full menu, snack
✅ User profile: athlete, sedentary, senior, child...
✅ Nutritional constraints:

Glycemic index

Fat

Sodium

Sweetened beverages (SSBs)

Fiber

Processed meat

Red meat

Fruit

✅ Recipes generated using GPT-4 (OpenAI)
✅ Save or delete suggested recipes
✅ Interface available in:
🇫🇷 French (default), 🇬🇧 English, 🇪🇸 Spanish, 🇳🇱 Dutch, 🇩🇪 German

Recipes are saved in recettes/recettes.csv
Each user’s history is saved under their session

🛠️ Tech Stack
Python: Pandas, NumPy, Scikit-learn, Joblib

Streamlit: web UI

SQLite: database

Plotly / Matplotlib / Seaborn: visualization

OpenAI GPT-4: smart recipe generator

Public data: INSEE, CIQUAL, Santé Publique France