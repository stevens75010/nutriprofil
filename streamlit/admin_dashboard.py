import streamlit as st
import sqlite3
import pandas as pd

def show_admin_dashboard():
    st.subheader("👑 Espace Administrateur – Niveau 1")
    st.markdown("Bienvenue dans l’interface de **gestion complète** du système Nutriprofil.")

    # Connexion à la base utilisateurs
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # Récupérer la liste des utilisateurs
    cursor.execute("SELECT pseudo, role FROM utilisateurs")
    users = cursor.fetchall()

    st.markdown("### 👥 Liste des utilisateurs enregistrés")
    if users:
        df_users = pd.DataFrame(users, columns=["Pseudo", "Rôle"])
        st.dataframe(df_users, use_container_width=True)
    else:
        st.info("Aucun utilisateur enregistré.")

    # Afficher tous les fichiers de consultation
    st.markdown("---")
    st.markdown("### 📂 Historique global des consultations")

    try:
        conso_df = pd.read_csv("historique/consultations.csv")
        st.dataframe(conso_df, use_container_width=True)

        # Boutons d'export
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("⬇️ Télécharger en CSV", conso_df.to_csv(index=False), file_name="consultations.csv", mime="text/csv")
        with col2:
            st.download_button("⬇️ Télécharger en Excel", conso_df.to_excel("consultations.xlsx", index=False), file_name="consultations.xlsx")
    except FileNotFoundError:
        st.warning("Aucun historique de consultation trouvé.")

    st.markdown("---")
    st.info("🔧 D’autres fonctionnalités d’administration pourront être ajoutées : suppression, statistiques, logs...")

    conn.close()
