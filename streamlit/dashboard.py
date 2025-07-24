import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

st.set_page_config(
    page_title="Nutrition & Santé Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_db(path):
    if not os.path.exists(path):
        st.error(f"Fichier introuvable : {path}")
        st.stop()
    return sqlite3.connect(path)

def show_kpis(conn):
    # SECTION SANTÉ
    st.markdown("# 🏥 KPIs Santé")
    years_health = pd.read_sql_query(
        "SELECT DISTINCT year_id FROM fact_health ORDER BY year_id", conn
    )["year_id"].tolist()
    sel_year_health = st.sidebar.selectbox(
        "Année Santé", years_health, index=len(years_health)-1
    )
    df_h = pd.read_sql(f"SELECT * FROM fact_health WHERE year_id={sel_year_health}", conn)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🩸 Diabète (%)",     f"{df_h['diabete_prev'].iat[0]:.1f}%")
    c2.metric("🍔 Obésité (%)",     f"{df_h['obesite_prev'].iat[0]:.1f}%"    if "obesite_prev"    in df_h else "N/A")
    c3.metric("⚡ Hypertension (%)",f"{df_h['hypertension_prev'].iat[0]:.1f}%" if "hypertension_prev" in df_h else "N/A")

    st.markdown("---")
    # SECTION NUTRITION
    st.markdown("# 🍽️ KPIs Nutrition")
    # SECTION : RÉPARTITION DES FAMILLES PAR TENEUR
    st.markdown("## 🌈 Répartition des familles par teneur moyenne")
    df_fam = pd.read_sql("""
        SELECT f.family_name AS Famille,
               AVG(d.Fibres) AS Fibres_moyennes,
               AVG(d.Gras) AS Gras_moyens,
               AVG(d.Glucides) AS Glucides_moyens
        FROM dim_food d
        JOIN dim_family f ON CAST(d.family_id AS INTEGER )= f.family_id
        GROUP BY f.family_name
    """, conn)

    col1, col2, col3 = st.columns(3)
    col1.plotly_chart(
        px.bar(df_fam, x="Famille", y="Fibres_moyennes",
               title="💚 Fibres moyennes par famille"),
        use_container_width=True
    )
    col2.plotly_chart(
        px.bar(df_fam, x="Famille", y="Gras_moyens",
               title="🧈 Gras moyens par famille"),
        use_container_width=True
    )
    col3.plotly_chart(
        px.bar(df_fam, x="Famille", y="Glucides_moyens",
               title="🍬 Glucides moyens par famille"),
        use_container_width=True
    )

    st.markdown("---")

   
   
    years_cons = pd.read_sql_query(
        "SELECT DISTINCT year_id FROM fact_consumption ORDER BY year_id", conn
    )["year_id"].tolist()
    sel_year_cons = st.sidebar.selectbox(
        "Année Consommation", years_cons, index=len(years_cons)-1
    )

    # Consommation par catégorie
    st.markdown("## 📈 Consommation par catégorie")
    df_cat = pd.read_sql(f"""
        SELECT f.family_name AS Catégorie,
               SUM(CAST(REPLACE(value,' ','') AS REAL)) AS Quantité
        FROM fact_consumption c
        JOIN dim_family f ON c.family_id = f.family_id
        WHERE c.year_id = {sel_year_cons}
        GROUP BY f.family_name
    """, conn)
    st.plotly_chart(
        px.bar(df_cat, x="Catégorie", y="Quantité",
               labels={"Quantité":"kg/habitant"}, height=350),
        use_container_width=True
    )

    # Répartition
    st.markdown("## 🔍 Répartition de la consommation")
    df_cat["Part (%)"] = df_cat["Quantité"] / df_cat["Quantité"].sum() * 100
    st.plotly_chart(
        px.pie(df_cat, names="Catégorie", values="Part (%)", hole=0.4, height=350),
        use_container_width=True
    )

    # Évolution
    st.markdown("## 📊 Évolution de la consommation totale")
    df_trend = pd.read_sql("""
        SELECT year_id AS Année,
               SUM(CAST(REPLACE(value,' ','') AS REAL)) AS Total_Consommation
        FROM fact_consumption
        GROUP BY year_id
        ORDER BY year_id
    """, conn)
    st.plotly_chart(
        px.line(df_trend, x="Année", y="Total_Consommation",
                labels={"Total_Consommation":"kg/habitant"}, height=350),
        use_container_width=True
    )


def show_dashboard():
    st.title("🌟 Dashboard Nutrition & Santé")
    db_path = '/Users/coulibalykani/Desktop/Projet 3/nutriprofil/nutriprofil_final.db'
    conn = load_db(db_path)
    show_kpis(conn)
    conn.close()
