import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def show_dashboard():
    st.title("Mon Tableau de Bord Interactif")
    st.write("Bienvenue sur votre dashboard ! Ici, vous pouvez visualiser vos données grâce à des graphiques dynamiques.")

    # --- Section 1: Données Simples ---
    st.header("Graphique simple : Ventes par Catégorie")

    # Création de données d'exemple
    data_ventes = {
        'Catégorie': ['Électronique', 'Vêtements', 'Alimentaire', 'Maison', 'Livres'],
        'Ventes': [15000, 12000, 8000, 7000, 4000],
        'Bénéfice': [3000, 4000, 2000, 1500, 1000]
    }
    df_ventes = pd.DataFrame(data_ventes)

    # Graphique à barres des ventes par catégorie
    fig_bar = px.bar(df_ventes, x='Catégorie', y='Ventes',
                     title='Ventes Totales par Catégorie de Produit',
                     labels={'Ventes': 'Montant des Ventes ($)'},
                     color='Catégorie',
                     template='plotly_white')
    st.plotly_chart(fig_bar, use_container_width=True)

    # Graphique en secteurs des bénéfices par catégorie
    st.subheader("Bénéfices par Catégorie (Répartition)")
    fig_pie = px.pie(df_ventes, values='Bénéfice', names='Catégorie',
                     title='Répartition des Bénéfices par Catégorie',
                     hole=0.3) # Pour un graphique en donut
    st.plotly_chart(fig_pie, use_container_width=True)


    # --- Section 2: Données temporelles et interactions ---
    st.header("Analyse de Tendances (Données Fictives)")

    # Génération de données temporelles aléatoires
    date_rng = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    df_tendance = pd.DataFrame(date_rng, columns=['Date'])
    df_tendance['Valeur A'] = np.random.rand(len(date_rng)).cumsum() * 100 + 500
    df_tendance['Valeur B'] = np.random.rand(len(date_rng)).cumsum() * 80 + 400
    df_tendance['Type'] = np.random.choice(['A', 'B', 'C'], len(date_rng))

    # Filtre par date
    # Note: st.sidebar.date_input doit être appelé dans la fonction de la page
    # si vous voulez que les filtres soient spécifiques à cette page.
    # Si vous voulez des filtres globaux, ils devraient être dans app.py
    st.sidebar.subheader("Filtres du Dashboard")
    start_date = st.sidebar.date_input("Date de début", min_value=df_tendance['Date'].min(), max_value=df_tendance['Date'].max(), value=df_tendance['Date'].min(), key="dashboard_start_date")
    end_date = st.sidebar.date_input("Date de fin", min_value=df_tendance['Date'].min(), max_value=df_tendance['Date'].max(), value=df_tendance['Date'].max(), key="dashboard_end_date")


    df_filtered = df_tendance[(df_tendance['Date'] >= pd.to_datetime(start_date)) & (df_tendance['Date'] <= pd.to_datetime(end_date))]

    # Graphique linéaire interactif
    fig_line = px.line(df_filtered, x='Date', y=['Valeur A', 'Valeur B'],
                       title='Tendances des Valeurs A et B au fil du temps',
                       labels={'value': 'Valeur', 'variable': 'Type de Valeur'},
                       template='plotly_dark') # Un autre thème
    st.plotly_chart(fig_line, use_container_width=True)

    # --- Section 3: Tableau de données brut ---
    st.header("Aperçu des Données Brutes")
    st.write("Voici un aperçu des 10 premières lignes des données de tendance filtrées :")
    st.dataframe(df_filtered.head(10), use_container_width=True)