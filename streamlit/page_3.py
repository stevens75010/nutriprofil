# page_3.py
import streamlit as st
import pandas as pd
import os
import openai
from datetime import datetime
import csv

# --- Langues disponibles ---
langues = {
    "Français": "fr",
    "English": "en",
    "Español": "es",
    "Nederlands": "nl",
    "Deutsch": "de"
}

# --- Traductions ---
traductions = {
    "fr": {
        "title": "🍽️ Mes recettes équilibrées",
        "meal_type": "Type de repas",
        "profile": "Profil utilisateur",
        "filters": "Filtres nutritionnels",
        "generate": "Générer une recette",
        "save": "Sauvegarder la recette",
        "your_recipe": "Votre recette",
        "saved_recipes": "📚 Recettes sauvegardées",
        "delete": "Supprimer la recette sélectionnée",
        "select_recipe": "Sélectionnez une recette à supprimer",
        "no_recipe": "Aucune recette sauvegardée.",
    },
    "en": {
        "title": "🍽️ My Balanced Recipes",
        "meal_type": "Meal Type",
        "profile": "User Profile",
        "filters": "Nutritional Filters",
        "generate": "Generate Recipe",
        "save": "Save Recipe",
        "your_recipe": "Your Recipe",
        "saved_recipes": "📚 Saved Recipes",
        "delete": "Delete Selected Recipe",
        "select_recipe": "Select a recipe to delete",
        "no_recipe": "No saved recipes.",
    }
    # Vous pouvez compléter les autres langues ici
}

# --- Paramètres repas et profils ---
types_repas = ["Entrée", "Plat", "Dessert", "Menu complet", "En-cas"]
profils = ["Sportif", "Sédentaire", "Personne âgée", "Enfant", "Autre"]

def get_translation(key, lang):
    return traductions.get(lang, traductions["fr"]).get(key, key)

def show_page():
    # --- Sélecteur de langue ---
    langue_selectionnee = st.sidebar.selectbox("🌐 Langue", list(langues.keys()))
    lang_code = langues[langue_selectionnee]
    tr = lambda k: get_translation(k, lang_code)

    st.title(tr("title"))

    # --- Choix utilisateur ---
    type_repas = st.selectbox(tr("meal_type"), types_repas)
    profil = st.selectbox(tr("profile"), profils)

    st.markdown(f"**{tr('filters')} :**")
    max_ig = st.slider("Index glycémique maximum", 10, 100, 60)
    max_lipides = st.slider("Lipides max (g)", 0, 100, 30)
    max_sodium = st.slider("Sodium max (mg)", 0, 3000, 1500)
    max_ssbs = st.slider("Boissons sucrées max (g)", 0, 100, 10)
    min_fibres = st.slider("Fibres min (g)", 0, 50, 5)
    max_procmeat = st.slider("Viandes transformées max (g)", 0, 200, 20)
    max_redmeat = st.slider("Viandes rouges max (g)", 0, 200, 30)
    min_fruits = st.slider("Fruits min (g)", 0, 200, 50)

    # --- Génération de recette par OpenAI ---
    if st.button(tr("generate")):
        openai.api_key = os.getenv("OPENAI_API_KEY")  # Assurez-vous que la clé est bien en variable d'environnement
        prompt = (
            f"Propose une recette {type_repas.lower()} équilibrée pour un profil {profil.lower()} "
            f"avec les contraintes suivantes : IG ≤ {max_ig}, lipides ≤ {max_lipides}g, sodium ≤ {max_sodium}mg, "
            f"boissons sucrées ≤ {max_ssbs}g, fibres ≥ {min_fibres}g, viandes transformées ≤ {max_procmeat}g, "
            f"viandes rouges ≤ {max_redmeat}g, fruits ≥ {min_fruits}g. "
            f"Format : nom du plat, ingrédients, instructions. Langue : {langue_selectionnee}."
        )
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            recette = response["choices"][0]["message"]["content"]
            st.session_state["recette_generee"] = recette
        except Exception as e:
            st.error(f"Erreur lors de la génération de la recette : {e}")

    # --- Affichage recette générée ---
    if "recette_generee" in st.session_state:
        st.markdown(f"### {tr('your_recipe')}")
        st.markdown(st.session_state["recette_generee"])

        if st.button(tr("save")):
            os.makedirs("recettes", exist_ok=True)
            pseudo = st.session_state.get("user", "inconnu")
            with open("recettes/recettes.csv", "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([datetime.now(), pseudo, type_repas, profil, st.session_state["recette_generee"]])
            st.success("✅ Recette sauvegardée.")

    # --- Affichage des recettes sauvegardées ---
    st.markdown(f"### {tr('saved_recipes')}")
    if os.path.exists("recettes/recettes.csv"):
        df = pd.read_csv("recettes/recettes.csv", names=["Date", "Pseudo", "Type", "Profil", "Recette"], header=None)
        pseudo = st.session_state.get("user", None)
        if pseudo:
            df = df[df["Pseudo"] == pseudo]
        if df.empty:
            st.info(tr("no_recipe"))
        else:
            st.dataframe(df[["Date", "Type", "Profil", "Recette"]], use_container_width=True)

            recipe_list = df["Recette"].tolist()
            selected = st.selectbox(tr("select_recipe"), recipe_list)
            if st.button(tr("delete")):
                df = df[df["Recette"] != selected]
                df.to_csv("recettes/recettes.csv", index=False, header=False)
                st.success("🗑️ Recette supprimée.")
                st.experimental_rerun()
    else:
        st.info(tr("no_recipe"))
