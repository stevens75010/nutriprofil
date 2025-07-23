import streamlit as st
import openai
import joblib
import os
import pandas as pd
from dotenv import load_dotenv
from fpdf import FPDF
from io import BytesIO

# --- Chargement OpenAI ---
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

# --- Mapping des familles (formulaire -> modèle) ---
FAMILLE_MAPPING = {
    "Légume": "Fruits et légumes",
    "Fruit": "Fruits et légumes", 
    "Viande": "Viandes et poissons",
    "Laitier": "Produits laitiers",
    "Transformé": "Plats préparés",
    "Céréale": "Céréales",
    "Boisson": "Boissons",
    "Autre": "Autres",
    "Sucré": "Produits sucrés"
}

# Familles reconnues par le modèle (basées sur l'erreur)
FAMILLES_MODELE = [
    "Produits animaux",
    "Fruits et légumes",
    "Viandes et poissons", 
    "Produits laitiers",
    "Plats préparés",
    "Céréales",
    "Boissons",
    "Autres",
    "Produits sucrés"
]

# --- Fonction pour diagnostiquer les colonnes du modèle ---
def get_model_features():
    """Récupère les noms de colonnes attendues par le modèle"""
    try:
        if hasattr(model_cg, 'feature_names_in_'):
            return list(model_cg.feature_names_in_)
        elif hasattr(model_cg, 'feature_names_'):
            return list(model_cg.feature_names_)
        else:
            return None
    except:
        return None

# --- Chargement des modèles ---
@st.cache_resource
def load_models():
    base_path = "../streamlit/"
    try:
        model_cg = joblib.load(base_path + "model_charge_glycémique.pkl")
        model_diabete = joblib.load(base_path + "diabete_risque_randomforest.pkl")
        model_obesite = joblib.load(base_path + "obesite_risque_randomforest.pkl")
        model_mcv = joblib.load(base_path + "mcv_risque_randomforest.pkl")
        model_cancer = joblib.load(base_path + "cancercolorectal_risque_randomforest.pkl")
        return model_cg, model_diabete, model_obesite, model_mcv, model_cancer
    except FileNotFoundError as e:
        st.error(f"Erreur lors du chargement des modèles : {e}")
        return None, None, None, None, None

model_cg, model_diabete, model_obesite, model_mcv, model_cancer = load_models()

# --- Initialisation des variables de session ---
def init_session_state():
    if "historique_utilisateurs" not in st.session_state:
        st.session_state.historique_utilisateurs = {}
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

# --- Questions posées par Debby ---
questions = [
    ("nom", "Comment s'appelle le produit que vous souhaitez analyser ?"),
    ("calories", "Combien de **calories** contient une portion (en kcal) ?"),
    ("glucides", "Combien de **glucides** (en grammes) par portion ?"),
    ("fibres", "Combien de **fibres** (en grammes) ?"),
    ("graisses", "Combien de **graisses** totales (en grammes) ?"),
    ("proteines", "Combien de **protéines** (en grammes) ?"),
    ("sodium", "Combien de **sodium** (en milligrammes) ?"),
    ("famille", "À quelle **famille** appartient ce produit ?", list(FAMILLE_MAPPING.keys()))
]

def show_page():
    # Initialisation
    init_session_state()
    
    # --- Avatar + Présentation ---
    col1, col2 = st.columns([1, 6])
    with col1:
        # Vérifier si l'image existe, sinon utiliser un emoji
        if os.path.exists("images/debby-avatar.png"):
            st.image("images/debby-avatar.png", width=90)
        else:
            st.markdown("## 👩‍⚕️")
    with col2:
        st.markdown("""
        ## Bonjour, je suis **Debby**
        Votre conseillère en nutrition et santé.
        Ensemble, analysons vos produits et prenons de meilleures décisions alimentaires 🍽️.
        """)

    st.markdown("---")

    # --- Authentification minimale ---
    if "user" not in st.session_state:
        st.error("❌ Vous devez vous connecter sur la Page 1.")
        st.stop()

    user = st.session_state.user
    st.title(f"Bienvenue {user} 🙂")
    st.markdown("Merci de remplir le formulaire ci-dessous pour analyser un produit alimentaire.")

    # Vérifier si les modèles sont chargés
    if model_cg is None:
        st.error("❌ Les modèles ML ne sont pas disponibles. Vérifiez les chemins des fichiers.")
        st.stop()
    
    

    # --- Formulaire complet en 2 colonnes ---
    with st.form("formulaire_complet"):
        st.markdown("### 📝 Informations sur le produit")

        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("🧾 Nom du produit", value="", key="form_nom")
            calories = st.number_input("🔥 Calories par portion (kcal)", min_value=0.0, step=1.0, value=0.0, key="form_calories")
            glucides = st.number_input("🍞 Glucides (g)", min_value=0.0, step=0.1, value=0.0, key="form_glucides")
            fibres = st.number_input("🌿 Fibres (g)", min_value=0.0, step=0.1, value=0.0, key="form_fibres")
        with col2:
            graisses = st.number_input("🥑 Graisses totales (g)", min_value=0.0, step=0.1, value=0.0, key="form_graisses")
            proteines = st.number_input("🍗 Protéines (g)", min_value=0.0, step=0.1, value=0.0, key="form_proteines")
            sodium = st.number_input("🧂 Sodium (mg)", min_value=0.0, step=1.0, value=0.0, key="form_sodium")
            # Liste directement les familles reconnues par le modèle pour éviter toute confusion
            famille = st.selectbox(
                "📂 Famille du produit",
                FAMILLES_MODELE,
                index=0,
                key="form_famille"
            )

        st.markdown("---")
        submitted = st.form_submit_button("✅ Valider les réponses")

    # --- Traitement de la soumission ---
    if submitted:
        # Validation des données
        if not nom.strip():
            st.error("❌ Veuillez entrer un nom de produit.")
        else:
            # Enregistrement des réponses en session_state
            st.session_state.answers = {
                "nom": nom.strip(),
                "calories": float(calories),
                "glucides": float(glucides),
                "fibres": float(fibres),
                "graisses": float(graisses),
                "proteines": float(proteines),
                "sodium": float(sodium),
                "famille": famille
            }
            st.session_state.question_index = len(questions)
            st.success("✅ Données enregistrées avec succès!")
            
            # Afficher immédiatement les résultats
            show_result()

def show_result():
    if "answers" not in st.session_state or not st.session_state.answers:
        st.error("❌ Aucune donnée trouvée. Veuillez remplir le formulaire.")
        return
        
    answers = st.session_state.answers
    user = st.session_state.user

    st.markdown("---")
    st.markdown("## 📊 Résultats de l'analyse")

    try:
        # --- Prédiction Charge Glycémique ---
        # La famille peut déjà être celle du modèle (si elle provient de FAMILLES_MODELE)
        if answers["famille"] in FAMILLES_MODELE:
            famille_modele = answers["famille"]
        else:
            famille_modele = FAMILLE_MAPPING.get(answers["famille"], "Autres")
        famille_col = "Famille_" + famille_modele
        
        # Créer le DataFrame avec les bonnes colonnes
        df_input = pd.DataFrame([{
            "Calories": answers["calories"],
            "Fibres": answers["fibres"],
            "Glucides": answers["glucides"],
            "Gras": answers["graisses"],  # Changé de "Graisses" à "Gras"
            "Proteines": answers["proteines"]  # Changé de "Protéines" à "Proteines"
        }])
        
        # Ajouter toutes les colonnes famille du modèle (initialisées à 0)
        for famille_mod in FAMILLES_MODELE:
            col = "Famille_" + famille_mod
            df_input[col] = 0
        
        # Mettre à 1 la famille correspondante
        df_input[famille_col] = 1
        
        # S'assurer que les colonnes sont dans le bon ordre (optionnel mais recommandé)
        colonnes_nutrition = ["Calories", "Fibres", "Glucides", "Gras", "Proteines"]  # Noms mis à jour
        colonnes_famille = ["Famille_" + f for f in FAMILLES_MODELE]
        df_input = df_input[colonnes_nutrition + colonnes_famille]
        
     
        
        cg = model_cg.predict(df_input)[0]
        st.session_state.cg = cg

        # --- Analyse Santé (ML) ---
        X_sante = [[
            answers["sodium"],
            answers["glucides"],
            answers["fibres"],
            answers["graisses"],
            answers["proteines"],
            answers["calories"]
        ]]
        
        risques = {
            "Diabète": model_diabete.predict(X_sante)[0],
            "Obésité": model_obesite.predict(X_sante)[0],
            "Maladie cardiovasculaire": model_mcv.predict(X_sante)[0],
            "Cancer colorectal": model_cancer.predict(X_sante)[0]
        }
        st.session_state.risques = risques

        # --- Sauvegarder l'historique ---
        if user not in st.session_state.historique_utilisateurs:
            st.session_state.historique_utilisateurs[user] = []

        # Éviter les doublons
        nouveau_produit = {
            "nom": answers["nom"],
            "cg": cg,
            "famille": answers["famille"],  # Garder la famille du formulaire pour l'affichage
            "famille_modele": famille_modele,  # Ajouter aussi la famille du modèle
            "risques": risques
        }
        
        # Vérifier si ce produit n'est pas déjà dans l'historique
        if not any(p["nom"] == nouveau_produit["nom"] for p in st.session_state.historique_utilisateurs[user]):
            st.session_state.historique_utilisateurs[user].append(nouveau_produit)

        # --- Affichage résultats ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🔥 Charge glycémique", f"{cg:.2f}")
            
        with col2:
            st.markdown("### 🧬 Analyse santé")
            for maladie, risque in risques.items():
                emoji = "🟢 Faible" if risque == 0 else "🔴 Élevé"
                st.markdown(f"- **{maladie}** : {emoji}")

        # --- Recommandation GPT ---
        if openai.api_key:
            with st.spinner("🤖 Génération de recommandations..."):
                prompt = f"""
                Tu es Debby, une diététicienne bienveillante.
                Voici un produit :
                - Nom : {answers['nom']}
                - Calories : {answers['calories']} kcal
                - Glucides : {answers['glucides']} g
                - Fibres : {answers['fibres']} g
                - Graisses : {answers['graisses']} g
                - Protéines : {answers['proteines']} g
                - Sodium : {answers['sodium']} mg
                - Famille : {answers['famille']}
                - Charge glycémique : {cg:.2f}

                Propose une alternative plus saine qui conserve le type d'ingrédient.
                Sois concise et bienveillante.
                """
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=300
                    )
                    suggestion = response.choices[0].message.content.strip()
                    st.markdown(f"### 💡 Suggestion de Debby")
                    st.info(suggestion)
                except Exception as e:
                    st.warning(f"⚠️ Impossible de générer une recommandation GPT : {e}")
        else:
            st.warning("⚠️ Clé API OpenAI non configurée. Recommandations GPT indisponibles.")

        # --- Export CSV ---
        st.markdown("---")
        st.markdown("### 📥 Exporter vos données")
        
        histo = st.session_state.historique_utilisateurs[user]
        if histo:
            histo_df = pd.DataFrame([
                {
                    "Produit": h["nom"],
                    "Famille": h["famille"],
                    "Charge glycémique": f"{h['cg']:.2f}",
                    "Risque diabète": "Élevé" if h["risques"]["Diabète"] else "Faible",
                    "Risque obésité": "Élevé" if h["risques"]["Obésité"] else "Faible",
                    "Risque MCV": "Élevé" if h["risques"]["Maladie cardiovasculaire"] else "Faible",
                    "Risque cancer colorectal": "Élevé" if h["risques"]["Cancer colorectal"] else "Faible"
                } for h in histo
            ])

            col1, col2 = st.columns(2)
            with col1:
                st.download_button(
                    "📥 Exporter en CSV",
                    data=histo_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"historique_{user}.csv",
                    mime="text/csv"
                )

            # --- Export PDF (avec gestion d'erreur pour le logo) ---
            with col2:
                if st.button("📄 Exporter PDF stylisé"):
                    try:
                        pdf = FPDF()
                        pdf.add_page()
                        pdf.set_font("Arial", "B", 14)
                        
                        # Essayer d'ajouter le logo
                        if os.path.exists("images/nutriprofil-logo.png"):
                            pdf.image("images/nutriprofil-logo.png", x=10, y=8, w=40)
                            pdf.ln(25)
                        else:
                            pdf.ln(10)
                            
                        pdf.cell(0, 10, f"Historique des analyses - {user}", ln=True)
                        pdf.ln(5)

                        for h in histo:
                            pdf.set_font("Arial", "B", 12)
                            pdf.cell(0, 10, f"{h['nom']} ({h['famille']})", ln=True)
                            pdf.set_font("Arial", "", 11)
                            pdf.cell(0, 8, f"Charge glycemique : {h['cg']:.2f}", ln=True)
                            for maladie, risque in h["risques"].items():
                                statut = "Eleve" if risque else "Faible"
                                pdf.cell(0, 8, f"{maladie} : {statut}", ln=True)
                            pdf.ln(5)

                        buffer = BytesIO()
                        pdf.output(buffer)
                        st.download_button(
                            "⬇️ Télécharger le PDF", 
                            data=buffer.getvalue(), 
                            file_name=f"rapport_{user}.pdf", 
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"Erreur lors de la génération du PDF : {e}")

    except Exception as e:
        st.error(f"❌ Erreur lors de l'analyse : {e}")
        st.error("Vérifiez que tous les modèles sont correctement chargés.")

    # --- Recommencer ---
    st.markdown("---")
    if st.button("🔄 Analyser un autre produit"):
        # Garder l'historique mais réinitialiser le formulaire
        for key in ["question_index", "answers", "cg", "risques"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

# --- Fonction principale ---
def main():
    st.set_page_config(
        page_title="Debby - Analyse Nutritionnelle",
        page_icon="🍽️",
        layout="wide"
    )
    
    show_page()

if __name__ == "__main__":
    main()