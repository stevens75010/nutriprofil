import streamlit as st
import pandas as pd
import sqlite3

def show_admin2_view():
    st.subheader("🩺 Espace Professionnel de Santé – Niveau 2")
    st.markdown("Bienvenue dans l’interface dédiée aux professionnels de santé. Ici, vous pouvez **consulter les données utilisateurs** à des fins de suivi et de recherche.")

    try:
        df = pd.read_csv("historique/consultations.csv")

        st.markdown("### 📋 Données de consultation utilisateurs")
        st.dataframe(df, use_container_width=True)

        # Options de tri/filtrage
        pseudo_list = df["pseudo"].unique().tolist()
        selected_user = st.selectbox("🔎 Filtrer par utilisateur", ["Tous"] + pseudo_list)

        if selected_user != "Tous":
            df = df[df["pseudo"] == selected_user]
            st.dataframe(df, use_container_width=True)

        # Export CSV limité
        st.download_button("⬇️ Exporter la vue filtrée (CSV)", df.to_csv(index=False), file_name="consultations_utilisateur.csv", mime="text/csv")

    except FileNotFoundError:
        st.warning("Aucun fichier de consultations trouvé. Aucun utilisateur n’a encore consulté Debby.")
