# 🏦 CréditScore Pro - Application Web

Application de simulation de crédit avec un assistant IA conversationnel.

## 🚀 Déploiement rapide (Streamlit Cloud - GRATUIT)

### Méthode 1 : Via GitHub (Recommandé)

1. **Crée un compte GitHub** : https://github.com/signup

2. **Crée un nouveau repository** :
   - Clique sur "New repository"
   - Nom : `creditscore-pro`
   - Laisse en Public
   - Clique "Create repository"

3. **Upload les fichiers** :
   - Clique "uploading an existing file"
   - Dépose `app.py` et `requirements.txt`
   - Clique "Commit changes"

4. **Déploie sur Streamlit Cloud** :
   - Va sur https://share.streamlit.io/
   - Connecte-toi avec GitHub
   - Clique "New app"
   - Sélectionne ton repo `creditscore-pro`
   - Main file : `app.py`
   - Clique "Deploy!"

5. **Ton app est en ligne !** 🎉
   - URL : `https://ton-username-creditscore-pro.streamlit.app`

---

## 💻 Lancer en local

### Prérequis
- Python 3.8+
- Une clé API Anthropic

### Installation

```bash
# Clone ou télécharge les fichiers
cd credit_app

# Installe les dépendances
pip install -r requirements.txt

# Lance l'application
streamlit run app.py
```

L'app s'ouvre automatiquement dans ton navigateur à `http://localhost:8501`

---

## 🔑 Clé API

1. Va sur https://console.anthropic.com/
2. Crée un compte (5$ de crédits gratuits)
3. Génère une clé API
4. Colle-la dans l'application

---

## 📱 Fonctionnalités

- 💬 Chat naturel avec l'IA
- 📊 Analyse complète du dossier
- ✅ Décision instantanée (Accepté / Refusé / Sous conditions)
- 📈 Calcul des mensualités, taux d'endettement, reste à vivre
- 🎯 Conformité HCSF 2022 (taux d'endettement max 35%)

---

## 🛠️ Structure

```
credit_app/
├── app.py              # Application principale
├── requirements.txt    # Dépendances Python
└── README.md          # Ce fichier
```

---

## 💡 Conseils

- Utilise `claude-3-haiku-20240307` (le plus économique)
- Une simulation complète coûte ~0.01$ (1 centime)
- Avec 5$ gratuits = ~500 simulations

---

## 📝 Licence

Projet éducatif - M2 Data Science
