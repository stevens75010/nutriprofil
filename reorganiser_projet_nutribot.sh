#!/bin/bash

# 📁 Création des dossiers nécessaires
mkdir -p streamlit/models
mkdir -p streamlit/data
mkdir -p streamlit/.streamlit

# 📦 Déplacement des fichiers de modèles
mv model_charge_glycémique.pkl streamlit/models/
mv model_conso.pkl streamlit/models/
mv diabete_risque_randomforest.pkl streamlit/models/
mv obesite_risque_randomforest.pkl streamlit/models/
mv mcv_risque_randomforest.pkl streamlit/models/
mv cancercolorectal_risque_randomforest.pkl streamlit/models/

# 📊 Déplacement des CSV dans /data
mv Dataframe/conso-menages-2024.csv streamlit/data/
mv Dataframe/dataframe_complet_rempli_proteines.csv streamlit/data/

# 🔐 Création d’un fichier secrets.toml (clé OpenAI à remplacer !)
echo '[openai]' > streamlit/.streamlit/secrets.toml
echo 'openai_key = "sk-votre-clé-ici"' >> streamlit/.streamlit/secrets.toml

# 📄 Ajout du secrets.toml dans le .gitignore local
echo ".streamlit/secrets.toml" >> streamlit/.gitignore

# 🚀 Déplacement du fichier app.py (si présent dans la racine)
if [ -f app.py ]; then
  mv app.py streamlit/
fi

# ✅ Commit Git propre
git add streamlit/
git commit -m "🗂️ Réorganisation : modèles, données et clé API déplacés dans le dossier streamlit/"
git push origin main

echo "✅ Réorganisation terminée. Lance Streamlit avec :"
echo "cd streamlit && streamlit run app.py"
