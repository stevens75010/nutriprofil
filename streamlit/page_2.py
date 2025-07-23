import streamlit as st

def show_page():
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
