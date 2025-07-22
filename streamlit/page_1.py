import streamlit as st

def show_page():
    st.title("Bienvenue sur Nutriprofil ")
    
    st.markdown("""
    Nutriprofil est une application d’analyse et de recommandation alimentaire conçue pour mieux comprendre les habitudes nutritionnelles des Français, évaluer les risques 
    sanitaires associés à certains types de consommation, et proposer des recommandations alimentaires personnalisées.
    """)
    st.info("N'hésitez pas à explorer chaque page pour en savoir plus sur vos habitudes alimentaires.")
    

    st.info("N'hésitez pas à ajouter vos propres composants Streamlit ici !")