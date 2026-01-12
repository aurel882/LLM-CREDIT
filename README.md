# 🏦 CréditScore Pro

**Simulateur de crédit intelligent avec IA conversationnelle**


[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://creditscore-llm.streamlit.app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)


Clé API Anthropic : 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

CréditScore Pro est une application web qui révolutionne la simulation de crédit en remplaçant les formulaires traditionnels par une conversation naturelle avec une IA. Développé dans le cadre du Master 2 Data Science.

![Interface de l'application](https://img.shields.io/badge/Status-En%20ligne-brightgreen)

---

## 📑 Sommaire

- [🎯 Présentation](#-présentation)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture](#️-architecture)
- [🛠️ Stack technique](#️-stack-technique)
- [📊 Règles métier HCSF 2022](#-règles-métier-hcsf-2022)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [📖 Utilisation](#-utilisation)
- [🔮 Améliorations futures](#-améliorations-futures)
- [👥 Auteurs](#-auteurs)

---

## 🎯 Présentation

### Le problème

Les simulations de crédit traditionnelles souffrent de plusieurs défauts :
- **Formulaires longs et impersonnels** : décourageants pour l'utilisateur
- **Manque de transparence** : critères de décision opaques
- **Expérience froide** : absence d'accompagnement et de conseils personnalisés

### Notre solution

CréditScore Pro propose une approche conversationnelle où un assistant IA guide l'utilisateur comme le ferait un vrai conseiller bancaire :
- Collecte des informations de manière naturelle et fluide
- Explications claires des critères d'évaluation
- Transparence totale sur le score et la décision

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 💬 **Chatbot IA** | Dialogue naturel avec Claude (Anthropic) pour collecter les informations |
| 📊 **Règles HCSF 2022** | Moteur de décision basé sur les normes bancaires françaises réelles |
| 🎯 **Score détaillé** | Affichage du score sur 100 avec points forts et alertes |
| 🔄 **Adaptabilité** | Insensible à la casse, comprend différents formats de réponse |
| 💡 **Conseils personnalisés** | Recommandations adaptées au profil de l'utilisateur |
| 🔁 **Nouvelle simulation** | Possibilité de recommencer facilement |

### Adaptabilité du chatbot

Le chatbot est conçu pour être extrêmement flexible :
- **Insensible à la casse** : majuscules, minuscules, avec ou sans accents
- **Formats multiples** : "45k", "45000", "quarante-cinq mille", "3500 par mois"
- **Gestion des erreurs** : demande de reformulation polie si une information n'est pas claire
- **Tolérance aux fautes** : comprend les fautes de frappe et abréviations courantes

---

## 🏗️ Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Utilisateur │────▶│  Streamlit  │────▶│  Claude API │────▶│   Moteur    │
│             │◀────│  Interface  │◀────│    (LLM)    │◀────│  Décision   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Flux de données

1. **Collecte conversationnelle** : Le LLM pose les questions une par une et extrait les données au format JSON structuré
2. **Calculs financiers** : Mensualité, taux d'endettement, reste à vivre, capacité d'emprunt
3. **Décision finale** : Score sur 100, décision (Accepté / Sous conditions / Refusé), alertes et conseils

---

## 🛠️ Stack technique

### Packages Python

| Package | Version | Description |
|---------|---------|-------------|
| `streamlit` | ≥1.28.0 | Framework web pour interfaces interactives |
| `anthropic` | ≥0.18.0 | SDK officiel pour l'API Claude |
| `pandas` | ≥2.0.0 | Manipulation de données structurées |
| `numpy` | ≥1.24.0 | Calculs numériques et formules financières |

### Services

- **Claude 3 Haiku** : Modèle LLM rapide et économique (~0.01€/simulation)
- **Streamlit Cloud** : Hébergement gratuit avec déploiement automatique
- **GitHub** : Versioning et intégration continue

---

## 📊 Règles métier HCSF 2022

L'application applique les normes du Haut Conseil de Stabilité Financière :

### Critères d'évaluation

| Critère | Seuil | Description |
|---------|-------|-------------|
| **Taux d'endettement** | Max 35% | Mensualités / Revenus mensuels nets |
| **Reste à vivre** | Min 700€ | +300€ par enfant à charge |
| **Âge fin de prêt** | Max 75 ans | Âge actuel + durée du prêt |
| **Ancienneté emploi** | Bonus | Stabilité professionnelle valorisée |

### Décisions possibles

| Décision | Score | Condition |
|----------|-------|-----------|
| ✅ **ACCEPTÉ** | ≥ 70/100 | Tous les critères respectés |
| ⚠️ **SOUS CONDITIONS** | 50-69/100 | Critères limites |
| ❌ **REFUSÉ** | < 50/100 | Ou critère éliminatoire |

### Critères éliminatoires

- Taux d'endettement > 50%
- Reste à vivre < 400€
- Âge < 18 ans

---

## 🚀 Installation

### Prérequis

- Python 3.9 ou supérieur
- Clé API Anthropic ([obtenir une clé](https://console.anthropic.com/))

### Installation locale

```bash
# Cloner le repository
git clone https://github.com/aurel882/LLM-CREDIT.git
cd LLM-CREDIT

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

L'application sera accessible sur `http://localhost:8501`

---

## ⚙️ Configuration

### Clé API Anthropic

1. Créez un compte sur [console.anthropic.com](https://console.anthropic.com/)
2. Générez une clé API
3. Dans l'application, entrez votre clé dans la sidebar (section Configuration)

### Variables d'environnement (optionnel)

Vous pouvez aussi définir la clé API via une variable d'environnement :

```bash
export ANTHROPIC_API_KEY="votre-clé-api"
```

---

## 📖 Utilisation

1. **Lancez l'application** et entrez votre clé API Anthropic
2. **Cliquez sur "Nouvelle simulation"** pour commencer
3. **Répondez aux questions** du chatbot de manière naturelle
4. **Consultez les résultats** : score, décision, détails financiers
5. **Analysez les alertes** et conseils personnalisés

### Exemple de conversation

```
🤖 Bonjour ! Je suis votre conseiller virtuel. Comment puis-je vous appeler ?
👤 Marie

🤖 Enchanté Marie ! Quel est votre revenu annuel net ?
👤 45000 euros

🤖 Parfait. Quel montant souhaitez-vous emprunter ?
👤 200k

🤖 Sur quelle durée ? (en années)
👤 20 ans
...
```

---

## 🔮 Améliorations futures

### Machine Learning (en développement)

Nous avons travaillé sur l'intégration d'un modèle de machine learning :

- **Base de données** : 300 000 dossiers de crédit historiques
- **Modèle** : HistGradientBoostingClassifier (scikit-learn)
- **Architecture hybride prévue** : 70% règles métier + 30% ML

Cette fonctionnalité n'est pas encore déployée en raison de problèmes de compatibilité de versions entre l'environnement d'entraînement et Streamlit Cloud.

### Autres améliorations envisagées

- [ ] Intégration du modèle ML
- [ ] Export PDF du résultat
- [ ] Historique des simulations
- [ ] Comparaison de scénarios
- [ ] Support multilingue

---

## 👥 Auteurs

Projet réalisé dans le cadre du **Master 2 Data Science** — Janvier 2026

| Nom | GitHub |
|-----|--------|
| **Aurélien BRESSON** | [@aurel882](https://github.com/aurel882) |
| **Lenny LEPETIT-AVISSE** | [@lennylepetit1](https://github.com/lennylepetit1) |

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<p align="center">
  <i>Développé avec ❤️ et beaucoup de ☕</i>
</p>

