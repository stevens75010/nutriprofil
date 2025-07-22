import streamlit as st
import os

# Importez les fonctions de chaque page
import page_1, page_2, page_3, dashboard

st.set_page_config(layout="wide")

def main():


    # --- Afficher une image dans la sidebar ---
    image_path = "images/nutriprofil-logo.png" # Assurez-vous que ce chemin est correct
    if os.path.exists(image_path):
        st.sidebar.image(image_path,  use_container_width=True)
    else:
        st.sidebar.warning(f"Image non trouvée : {image_path}. Veuillez la placer dans le dossier 'images'.")
    # ----------------------------------------

    # Définir les pages disponibles et les fonctions associées
    pages = {
        "Accueil": page_1.show_page,
        "Mon suivi": page_2.show_page,
        "Recettes": page_3.show_page,
        "Statistiques": dashboard.show_dashboard
    }

    # Initialiser la page courante dans le session state si elle n'existe pas
    if "current_page" not in st.session_state:
        st.session_state.current_page = list(pages.keys())[0] # Définit la première page comme page par défaut

    # Créer des liens (boutons discrets) dans la sidebar
    for page_name, page_function in pages.items():
        if st.sidebar.button(page_name, use_container_width=True, key=f"nav_{page_name}"):
            st.session_state.current_page = page_name

    # Afficher le titre de la page principale en fonction de la page sélectionnée
    st.title(st.session_state.current_page)

    # Appeler la fonction de la page sélectionnée
    pages[st.session_state.current_page]()


if __name__ == "__main__":
    main()