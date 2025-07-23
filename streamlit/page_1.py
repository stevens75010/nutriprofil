import streamlit as st
import sqlite3
import hashlib
import os

# ----------------------
# 🔐 Base de données SQLite
# ----------------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT UNIQUE,
            password TEXT,
            role TEXT CHECK(role IN ('user', 'admin1', 'admin2')) DEFAULT 'user'
        )
    """)
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(pseudo, password, role="user"):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (pseudo, password, role) VALUES (?, ?, ?)", 
              (pseudo, hash_password(password), role))
    conn.commit()
    conn.close()

def check_login(pseudo, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT password, role FROM users WHERE pseudo=?", (pseudo,))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return result[1]
    return None

# ----------------------
# 🚀 Page principale
# ----------------------
def show_page():
    init_db()

    st.markdown("## 🧠 Bienvenue sur Nutriprofil")
    st.image("images/nutriprofil-logo.png", width=200)

    st.markdown("""
Bienvenue dans **Nutriprofil**, votre outil intelligent pour :
- comprendre l’impact de vos choix alimentaires sur votre santé,
- recevoir des conseils personnalisés avec **Debby**, notre conseillère diététique virtuelle,
- permettre aux **professionnels de santé** de suivre les profils nutritionnels de leurs patients.

Grâce à une interface simple et interactive, Nutriprofil est adapté :
- à tous ceux qui veulent **reprendre le contrôle de leur alimentation**
- et aux **acteurs médicaux** en quête d’un suivi fiable et automatisé.

---
""")

    # Si déjà connecté
    if "user" in st.session_state and "role" in st.session_state:
        st.success(f"✅ Connecté en tant que **{st.session_state.user}** (rôle : {st.session_state.role})")
        if st.session_state.role in ["user", "admin2"]:
            st.session_state.current_page = "Mon suivi"
            st.experimental_rerun()
        else:
            st.info("En tant qu'administrateur, vous pouvez naviguer librement.")
        return

    # --- Tabs Connexion / Inscription
    tab1, tab2 = st.tabs(["🔐 Se connecter", "🆕 Créer un compte"])

    with tab1:
        st.subheader("Connexion")
        with st.form("login_form"):
            pseudo = st.text_input("👤 Pseudo")
            password = st.text_input("🔑 Mot de passe", type="password")
            submit = st.form_submit_button("Se connecter")

        if submit:
            role = check_login(pseudo, password)
            if role:
                st.session_state["user"] = pseudo
                st.session_state["role"] = role
                st.success("Connexion réussie ! Redirection...")
                if role in ["user", "admin2"]:
                    st.session_state.current_page = "Mon suivi"
                st.experimental_rerun()
            else:
                st.error("❌ Identifiants incorrects.")

    with tab2:
        st.subheader("Créer un compte")
        with st.form("signup_form"):
            new_pseudo = st.text_input("👤 Choisissez un pseudo")
            new_password = st.text_input("🔑 Mot de passe", type="password")
            confirm_password = st.text_input("🔁 Confirmez le mot de passe", type="password")
            role_choice = st.selectbox("🎓 Rôle souhaité", ["user", "admin2"])  # admin1 = manuel
            submit = st.form_submit_button("Créer mon compte")

        if submit:
            if new_password != confirm_password:
                st.warning("❗ Les mots de passe ne correspondent pas.")
            elif new_pseudo == "":
                st.warning("❗ Veuillez entrer un pseudo.")
            else:
                try:
                    add_user(new_pseudo, new_password, role_choice)
                    st.success("✅ Compte créé avec succès ! Vous pouvez vous connecter.")
                except sqlite3.IntegrityError:
                    st.error("❌ Ce pseudo est déjà utilisé.")
