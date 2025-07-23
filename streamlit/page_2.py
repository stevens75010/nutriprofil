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

# --- Chargement des modèles ---
@st.cache_resource
def load_models():
    base_path = "nutriprofil/streamlit/"
    model_cg = joblib.load(base_path + "model_charge_glycémique.pkl")
    model_diabete = joblib.load(base_path + "diabete_risque_randomforest.pkl")
    model_obesite = joblib.load(base_path + "obesite_risque_randomforest.pkl")
    model_mcv = joblib.load(base_path + "mcv_risque_randomforest.pkl")
    model_cancer = joblib.load(base_path + "cancercolorectal_risque_randomforest.pkl")
    return model_cg, model_diabete, model_obesite, model_mcv, model_cancer

model_cg, model_diabete, model_obesite, model_mcv, model_cancer = load_models()

# --- Questions posées par Debby ---
questions = [
    ("nom", "Comment s'appelle le produit que vous souhaitez analyser ?"),
    ("calories", "Combien de **calories** contient une portion (en kcal) ?"),
    ("glucides", "Combien de **glucides** (en grammes) par portion ?"),
    ("fibres", "Combien de **fibres** (en grammes) ?"),
    ("graisses", "Combien de **graisses** totales (en grammes) ?"),
    ("proteines", "Combien de **protéines** (en grammes) ?"),
    ("sodium", "Combien de **sodium** (en milligrammes) ?"),
    ("famille", "À quelle **famille** appartient ce produit ?", ["Légume", "Fruit", "Viande", "Laitier", "Transformé", "Céréale", "Boisson", "Autre"])
]

def show_page():
 HEAD
    # --- Avatar + Présentation ---
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("streamlit/images/debby-avatar.png", width=90)
    with col2:
        st.markdown("""
        ## Bonjour 👋 Je suis **Debby**
        Votre conseillère en nutrition et santé.
        Ensemble, analysons vos produits et prenons de meilleures décisions alimentaires 🍽️.
        """)

    st.markdown("---")

    # --- Interface simplifiée pour l'instant ---
    st.write("🔍 Cette page accueillera bientôt le formulaire intelligent de Debby.")
    st.write("Elle vous posera des questions nutritionnelles, analysera les données, puis vous donnera un avis personnalisé.")
    st.info("💡 Exemple à venir : prédiction de charge glycémique, évaluation des risques santé, recommandation d'alternatives.")

    st.warning("🛠️ Pensez à ajouter les modèles ML et la logique du chatbot ici.")

    # --- Espace réservé aux futurs composants ---
    st.empty()
=======
    # --- Authentification minimale ---
    if "user" not in st.session_state:
        st.error("❌ Vous devez vous connecter sur la Page 1.")
        st.stop()

    user = st.session_state.user

    st.title(f"👩🏽‍⚕️ Debby — Consultation de {user}")
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("streamlit/images/debby-avatar.png", width=90)
    with col2:
        st.markdown("### Répondez aux questions, je m’occupe du reste 😊")

    # --- Initialisation de session ---
    if "question_index" not in st.session_state:
        st.session_state.question_index = 0
        st.session_state.answers = {}
        st.session_state.cg = None
        st.session_state.risques = None
        st.session_state.historique_utilisateurs = {}

    i = st.session_state.question_index
    key, question = questions[i][:2]
    options = questions[i][2] if len(questions[i]) > 2 else None

    with st.chat_message("assistant"):
        st.markdown(question)

    if options:
        user_input = st.selectbox("Votre réponse :", options, key=f"input_{key}")
    else:
        user_input = st.text_input("Votre réponse :", key=f"input_{key}")

    if user_input:
        st.session_state.answers[key] = user_input
        if st.button("✅ Suivant"):
            st.session_state.question_index += 1

            if st.session_state.question_index >= len(questions):
                show_result()

def show_result():
    answers = st.session_state.answers
    user = st.session_state.user

    # --- Prédiction Charge Glycémique ---
    famille_col = "Famille_" + answers["famille"]
    df_input = pd.DataFrame([{
        "Calories": float(answers["calories"]),
        "Fibres": float(answers["fibres"]),
        "Glucides": float(answers["glucides"]),
        "Graisses": float(answers["graisses"]),
        "Protéines": float(answers["proteines"]),
        famille_col: 1
    }])
    for f in ["Légume", "Fruit", "Viande", "Laitier", "Transformé", "Céréale", "Boisson", "Autre"]:
        col = "Famille_" + f
        if col not in df_input.columns:
            df_input[col] = 0
    cg = model_cg.predict(df_input)[0]
    st.session_state.cg = cg

    # --- Analyse Santé (ML) ---
    X_sante = [[
        float(answers["sodium"]),
        float(answers["glucides"]),
        float(answers["fibres"]),
        float(answers["graisses"]),
        float(answers["proteines"]),
        float(answers["calories"])
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

    st.session_state.historique_utilisateurs[user].append({
        "nom": answers["nom"],
        "cg": cg,
        "famille": answers["famille"],
        "risques": risques
    })

    # --- Affichage résultats ---
    st.chat_message("assistant").markdown(f"📊 **Charge glycémique estimée** : `{cg:.2f}`")
    st.chat_message("assistant").markdown("🧬 **Analyse santé**")
    for maladie, risque in risques.items():
        emoji = "🟢 Faible" if risque == 0 else "🔴 Élevé"
        st.markdown(f"- **{maladie}** : {emoji}")

    # --- Recommandation GPT ---
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

    Propose une alternative plus saine qui conserve le type d’ingrédient.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        suggestion = response.choices[0].message.content.strip()
        st.chat_message("assistant").markdown(f"💡 **Suggestion de Debby :**\n\n{suggestion}")
    except Exception as e:
        st.error(f"Erreur GPT : {e}")

    # --- Export CSV ---
    histo = st.session_state.historique_utilisateurs[user]
    histo_df = pd.DataFrame([
        {
            "Produit": h["nom"],
            "Famille": h["famille"],
            "Charge glycémique": h["cg"],
            "Risque diabète": "Élevé" if h["risques"]["Diabète"] else "Faible",
            "Risque obésité": "Élevé" if h["risques"]["Obésité"] else "Faible",
            "Risque MCV": "Élevé" if h["risques"]["Maladie cardiovasculaire"] else "Faible",
            "Risque cancer colorectal": "Élevé" if h["risques"]["Cancer colorectal"] else "Faible"
        } for h in histo
    ])

    st.download_button(
        "📥 Exporter en CSV",
        data=histo_df.to_csv(index=False).encode("utf-8"),
        file_name=f"historique_{user}.csv",
        mime="text/csv"
    )

    # --- Export PDF (avec logo) ---
    if st.button("📄 Exporter PDF stylisé"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.image("images/nutriprofil-logo.png", x=10, y=8, w=40)
        pdf.ln(25)
        pdf.cell(0, 10, f"Historique des analyses – {user}", ln=True)

        for h in histo:
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"{h['nom']} ({h['famille']})", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 8, f"Charge glycémique : {h['cg']:.2f}", ln=True)
            for maladie, risque in h["risques"].items():
                statut = "Élevé" if risque else "Faible"
                pdf.cell(0, 8, f"{maladie} : {statut}", ln=True)
            pdf.ln(5)

        buffer = BytesIO()
        pdf.output(buffer)
        st.download_button("⬇️ Télécharger le PDF", data=buffer.getvalue(), file_name=f"rapport_{user}.pdf", mime="application/pdf")

    # --- Recommencer ---
    if st.button("🔄 Recommencer la consultation"):
        for key in ["question_index", "answers", "cg", "risques"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
>>>>>>> c43be99 (🧠 Ajout du chatbot Debby + consultation interactive + export PDF/CSV)
