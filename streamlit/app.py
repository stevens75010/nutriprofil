import streamlit as st
import os

# Import des pages
import page_1
import page_2
import page_3  # "Mes recettes"
import dashboard

# Import pages admin
try:
    import admin_dashboard
    import vue_admin2
except ImportError:
    pass

st.set_page_config(layout="wide")

def main():
    # --- Logo dans la sidebar ---
    image_path = "images/nutriprofil-logo.png"
    if os.path.exists(image_path):
        st.sidebar.image(image_path, use_container_width=True)
    else:
        st.sidebar.warning("Image non trouvée : images/nutriprofil-logo.png")

    # --- Affichage utilisateur connecté ---
    if "user" in st.session_state:
        st.sidebar.success(f"👤 Connecté en tant que : **{st.session_state.user}**")

        if st.sidebar.button("🔓 Se déconnecter"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.experimental_rerun()

    # --- Pages disponibles ---
    pages = {
        "Accueil": page_1.show_page,
        "Mon suivi": page_2.show_page,
        "Mes recettes": page_3.show_page,
        "Statistiques": dashboard.show_dashboard,
    }

    # --- Ajouter les pages Admin selon le rôle ---
    role = st.session_state.get("role", "")
    if role == "admin1":
        pages["👑 Administration"] = admin_dashboard.show_admin_dashboard
    elif role == "admin2":
        pages["🔬 Vue admin santé"] = vue_admin2.show_admin2_view

    # --- Initialiser la page courante ---
    if "current_page" not in st.session_state:
        # Redirection automatique
        if role in ["user", "admin2"]:
            st.session_state.current_page = "Mon suivi"
        else:
            st.session_state.current_page = "Accueil"

    # --- Menu navigation (sidebar) ---
    st.sidebar.markdown("### 📁 Navigation")
    for page_name in pages:
        if st.sidebar.button(page_name, use_container_width=True, key=f"nav_{page_name}"):
            st.session_state.current_page = page_name
            st.experimental_rerun()

    # --- Afficher la page sélectionnée ---
    selected_page = st.session_state.current_page
    st.title(selected_page)

    # Protection : empêcher accès sans login sauf accueil
    if selected_page != "Accueil" and "user" not in st.session_state:
        st.warning("🔐 Veuillez vous connecter via la page Accueil pour accéder à cette section.")
        page_1.show_page()
    else:
        pages[selected_page]()


if __name__ == "__main__":
    main()
