"""
🏦 CréditScore Pro - Application Web
Assistant IA pour simulation de crédit

Pour lancer : streamlit run app.py
"""

import streamlit as st
import json
import re
from anthropic import Anthropic

# ============================================
# CONFIGURATION
# ============================================

st.set_page_config(
    page_title="CréditScore Pro",
    page_icon="🏦",
    layout="centered"
)

# Configuration crédit
CONFIG = {
    'MAX_DEBT_RATIO': 0.35,
    'MIN_RESTE_A_VIVRE': 700,
    'MIN_RESTE_A_VIVRE_ENFANT': 300,
    'MIN_AGE': 18,
    'MAX_AGE_FIN_PRET': 75,
    'TAUX_IMMO': 0.035,
    'TAUX_CONSO': 0.065,
    'SEUIL_IMMO': 75000,
    'MIN_APPORT_IMMO': 0.10
}

# ============================================
# CALCULATEUR DE CRÉDIT
# ============================================

class CalculateurCredit:
    @staticmethod
    def mensualite(capital, taux_annuel, duree_annees):
        if taux_annuel == 0:
            return capital / (duree_annees * 12)
        taux_mensuel = taux_annuel / 12
        nb_mois = duree_annees * 12
        return capital * (taux_mensuel * (1 + taux_mensuel)**nb_mois) / ((1 + taux_mensuel)**nb_mois - 1)

    @staticmethod
    def cout_total(capital, taux_annuel, duree_annees):
        mens = CalculateurCredit.mensualite(capital, taux_annuel, duree_annees)
        total = mens * duree_annees * 12
        return total, total - capital

    @staticmethod
    def taux_endettement(mensualite, revenu_mensuel):
        if revenu_mensuel <= 0:
            return float('inf')
        return mensualite / revenu_mensuel

    @staticmethod
    def capacite_emprunt(revenu_mensuel, taux_annuel, duree_annees, charges=0):
        mensualite_max = (revenu_mensuel * CONFIG['MAX_DEBT_RATIO']) - charges
        if mensualite_max <= 0:
            return 0
        taux_mensuel = taux_annuel / 12
        nb_mois = duree_annees * 12
        if taux_annuel == 0:
            return mensualite_max * nb_mois
        return mensualite_max * ((1 + taux_mensuel)**nb_mois - 1) / (taux_mensuel * (1 + taux_mensuel)**nb_mois)

    @staticmethod
    def type_credit(montant):
        return "immobilier" if montant >= CONFIG['SEUIL_IMMO'] else "consommation"

    @staticmethod
    def taux_interet(montant):
        return CONFIG['TAUX_IMMO'] if montant >= CONFIG['SEUIL_IMMO'] else CONFIG['TAUX_CONSO']

calc = CalculateurCredit()

# ============================================
# MOTEUR DE DÉCISION
# ============================================

class MoteurDecision:
    def analyser(self, dossier):
        revenu_annuel = dossier.get('revenu_annuel', 0)
        revenu_mensuel = revenu_annuel / 12
        montant = dossier.get('montant_credit', 0)
        duree = dossier.get('duree_annees', 20)
        age = dossier.get('age', 30)
        anciennete = dossier.get('anciennete_emploi', 0)
        nb_enfants = dossier.get('nb_enfants', 0)
        charges = dossier.get('charges_existantes', 0)
        apport = dossier.get('apport', 0)
        
        type_credit = calc.type_credit(montant)
        taux = calc.taux_interet(montant)
        mensualite = calc.mensualite(montant, taux, duree)
        mensualite_totale = mensualite + charges
        taux_endettement = calc.taux_endettement(mensualite_totale, revenu_mensuel)
        reste_a_vivre = revenu_mensuel - mensualite_totale
        cout_total, interets = calc.cout_total(montant, taux, duree)
        capacite_max = calc.capacite_emprunt(revenu_mensuel, taux, duree, charges)
        age_fin_pret = age + duree
        
        score = 100
        alertes = []
        points_forts = []
        
        # Règles d'évaluation
        if taux_endettement > 0.50:
            score -= 40
            alertes.append(f"⚠️ Taux d'endettement critique: {taux_endettement*100:.1f}%")
        elif taux_endettement > CONFIG['MAX_DEBT_RATIO']:
            score -= 25
            alertes.append(f"⚠️ Taux d'endettement élevé: {taux_endettement*100:.1f}% (max 35%)")
        elif taux_endettement <= 0.25:
            score += 10
            points_forts.append(f"✅ Excellent taux d'endettement: {taux_endettement*100:.1f}%")
        
        seuil_rav = CONFIG['MIN_RESTE_A_VIVRE'] + (nb_enfants * CONFIG['MIN_RESTE_A_VIVRE_ENFANT'])
        if reste_a_vivre < 400:
            score -= 35
            alertes.append(f"⚠️ Reste à vivre insuffisant: {reste_a_vivre:.0f}€")
        elif reste_a_vivre < seuil_rav:
            score -= 20
            alertes.append(f"⚠️ Reste à vivre limite: {reste_a_vivre:.0f}€")
        elif reste_a_vivre > seuil_rav * 2:
            score += 10
            points_forts.append(f"✅ Excellent reste à vivre: {reste_a_vivre:,.0f}€")
        
        if age < CONFIG['MIN_AGE']:
            score -= 50
            alertes.append(f"⚠️ Âge insuffisant: {age} ans")
        if age_fin_pret > CONFIG['MAX_AGE_FIN_PRET']:
            score -= 15
            alertes.append(f"⚠️ Âge en fin de prêt élevé: {age_fin_pret} ans")
        
        if anciennete < 0.5:
            score -= 15
            alertes.append(f"⚠️ Ancienneté emploi faible: {anciennete:.1f} ans")
        elif anciennete >= 5:
            score += 10
            points_forts.append(f"✅ Excellente stabilité professionnelle: {anciennete:.0f} ans")
        
        if type_credit == "immobilier":
            taux_apport = apport / (montant + apport) if montant > 0 else 0
            if taux_apport < 0.05:
                score -= 15
                alertes.append(f"⚠️ Apport très faible: {taux_apport*100:.1f}%")
            elif taux_apport >= 0.20:
                score += 15
                points_forts.append(f"✅ Excellent apport: {taux_apport*100:.1f}%")
        
        score = max(0, min(100, score))
        
        refus_auto = False
        raison_refus = None
        
        if taux_endettement > 0.50:
            refus_auto = True
            raison_refus = "Taux d'endettement excessif (>50%)"
        elif reste_a_vivre < 400:
            refus_auto = True
            raison_refus = "Reste à vivre insuffisant (<400€)"
        elif age < CONFIG['MIN_AGE']:
            refus_auto = True
            raison_refus = "Âge minimum non atteint"
        
        if refus_auto:
            decision = "REFUSÉ"
        elif score >= 70:
            decision = "ACCEPTÉ"
        elif score >= 50:
            decision = "ACCEPTÉ SOUS CONDITIONS"
        else:
            decision = "REFUSÉ"
        
        return {
            'decision': decision,
            'score': score,
            'alertes': alertes,
            'points_forts': points_forts,
            'refus_auto': refus_auto,
            'raison_refus': raison_refus,
            'details': {
                'type_credit': type_credit,
                'taux': taux,
                'mensualite': mensualite,
                'taux_endettement': taux_endettement,
                'reste_a_vivre': reste_a_vivre,
                'cout_total': cout_total,
                'interets': interets,
                'capacite_max': capacite_max,
                'age_fin_pret': age_fin_pret
            }
        }

moteur = MoteurDecision()

# ============================================
# SYSTEM PROMPT POUR LE LLM
# ============================================

SYSTEM_PROMPT = """Tu es un conseiller bancaire virtuel professionnel et empathique pour CréditScore Pro.
Ton rôle est de collecter les informations nécessaires pour évaluer une demande de crédit.

INFORMATIONS À COLLECTER (dans l'ordre de préférence) :
1. prenom : Le prénom du client
2. revenu_annuel : Revenus annuels nets en euros (nombre)
3. montant_credit : Montant du crédit souhaité en euros (nombre)
4. duree_annees : Durée souhaitée en années (nombre entre 5 et 25)
5. age : Âge du client (nombre)
6. anciennete_emploi : Ancienneté dans l'emploi actuel en années (nombre)
7. nb_enfants : Nombre d'enfants à charge (nombre, 0 si aucun)
8. charges_existantes : Charges mensuelles existantes en euros (crédits en cours, pensions, etc.)
9. apport : Apport personnel en euros (0 si aucun)

RÈGLES IMPORTANTES :
- Sois chaleureux et professionnel
- Pose UNE SEULE question à la fois
- Confirme chaque information reçue avant de passer à la suivante
- Si une valeur est ambiguë, demande une clarification
- Convertis les valeurs mensuelles en annuelles si nécessaire (revenus)
- Accepte les réponses approximatives et arrondis si besoin

FORMAT DE RÉPONSE :
À chaque message, tu dois inclure un bloc JSON à la fin (entre balises ```json```) avec :
- "collected": dictionnaire des informations déjà collectées
- "next_field": le prochain champ à demander (ou null si tout est collecté)
- "complete": true/false si toutes les infos sont collectées

Exemple :
```json
{"collected": {"prenom": "Marie", "revenu_annuel": 45000}, "next_field": "montant_credit", "complete": false}
```

Quand complete=true, termine par une phrase du type "J'ai toutes les informations, je lance l'analyse..."
"""

# ============================================
# FONCTIONS UTILITAIRES
# ============================================

def extract_json(text):
    """Extrait le bloc JSON de la réponse."""
    pattern = r'```json\s*(.+?)\s*```'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    return None

def clean_response(text):
    """Retire le bloc JSON de la réponse affichée."""
    return re.sub(r'```json\s*.+?\s*```', '', text, flags=re.DOTALL).strip()

def get_llm_response(messages, api_key):
    """Appelle l'API Claude."""
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages
    )
    return response.content[0].text

def run_analysis(collected_data):
    """Lance l'analyse du dossier."""
    dossier = {
        'revenu_annuel': float(collected_data.get('revenu_annuel', 0)),
        'montant_credit': float(collected_data.get('montant_credit', 0)),
        'duree_annees': int(collected_data.get('duree_annees', 20)),
        'age': int(collected_data.get('age', 30)),
        'anciennete_emploi': float(collected_data.get('anciennete_emploi', 0)),
        'nb_enfants': int(collected_data.get('nb_enfants', 0)),
        'charges_existantes': float(collected_data.get('charges_existantes', 0)),
        'apport': float(collected_data.get('apport', 0))
    }
    return moteur.analyser(dossier)

def display_result(result, prenom):
    """Affiche le résultat de l'analyse."""
    r = result
    d = r['details']
    
    # Couleur selon décision
    if r['decision'] == "ACCEPTÉ":
        st.success(f"🎉 {r['decision']}")
        color = "green"
    elif r['decision'] == "ACCEPTÉ SOUS CONDITIONS":
        st.warning(f"👍 {r['decision']}")
        color = "orange"
    else:
        st.error(f"😔 {r['decision']}")
        color = "red"
    
    st.markdown(f"**Score : {r['score']:.0f}/100**")
    
    # Métriques principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Mensualité", f"{d['mensualite']:,.2f}€")
    with col2:
        st.metric("Taux d'endettement", f"{d['taux_endettement']*100:.1f}%")
    with col3:
        st.metric("Reste à vivre", f"{d['reste_a_vivre']:,.0f}€")
    
    # Détails
    with st.expander("📊 Détails du crédit"):
        st.write(f"**Type de crédit:** {d['type_credit'].capitalize()}")
        st.write(f"**Taux d'intérêt:** {d['taux']*100:.2f}%")
        st.write(f"**Coût total:** {d['cout_total']:,.2f}€")
        st.write(f"**Dont intérêts:** {d['interets']:,.2f}€")
        st.write(f"**Capacité d'emprunt max:** {d['capacite_max']:,.0f}€")
        st.write(f"**Âge en fin de prêt:** {d['age_fin_pret']} ans")
    
    # Points forts
    if r['points_forts']:
        with st.expander("✅ Points forts", expanded=True):
            for pf in r['points_forts']:
                st.write(pf)
    
    # Alertes
    if r['alertes']:
        with st.expander("⚠️ Points d'attention", expanded=True):
            for al in r['alertes']:
                st.write(al)

# ============================================
# INTERFACE STREAMLIT
# ============================================

# CSS personnalisé
st.markdown("""
<style>
.stChatMessage {
    padding: 1rem;
}
.main-header {
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
}
.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
}
.main-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🏦 CréditScore Pro</h1>
    <p>Assistant IA pour votre simulation de crédit</p>
</div>
""", unsafe_allow_html=True)

# Sidebar pour la clé API
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input("Clé API Anthropic", type="password", help="Votre clé API Claude")
    
    if st.button("🔄 Nouvelle simulation"):
        st.session_state.messages = []
        st.session_state.collected_data = {}
        st.session_state.is_complete = False
        st.session_state.result = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📖 Comment ça marche ?")
    st.markdown("""
    1. Entrez votre clé API
    2. Discutez avec l'assistant
    3. Répondez aux questions
    4. Obtenez votre analyse !
    """)
    
    st.markdown("---")
    st.markdown("### 🔗 Obtenir une clé API")
    st.markdown("[Console Anthropic](https://console.anthropic.com/)")

# Initialisation de la session
if "messages" not in st.session_state:
    st.session_state.messages = []
if "collected_data" not in st.session_state:
    st.session_state.collected_data = {}
if "is_complete" not in st.session_state:
    st.session_state.is_complete = False
if "result" not in st.session_state:
    st.session_state.result = None

# Vérification de la clé API
if not api_key:
    st.info("👈 Entrez votre clé API Anthropic dans la barre latérale pour commencer.")
    st.stop()

# Message de bienvenue
if not st.session_state.messages:
    welcome = """Bonjour et bienvenue chez CréditScore Pro ! 👋

Je suis votre conseiller virtuel et je vais vous accompagner dans votre simulation de crédit.
En quelques questions, je pourrai analyser votre dossier et vous donner une réponse personnalisée.

Pour commencer, comment puis-je vous appeler ?"""
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Affichage des messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Affichage du résultat si terminé
if st.session_state.is_complete and st.session_state.result:
    st.markdown("---")
    st.header("📊 Résultat de votre simulation")
    prenom = st.session_state.collected_data.get('prenom', 'Client')
    display_result(st.session_state.result, prenom)

# Input utilisateur
if not st.session_state.is_complete:
    if prompt := st.chat_input("Votre message..."):
        # Ajoute le message utilisateur
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Prépare les messages pour l'API
        api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        
        # Appelle le LLM
        with st.chat_message("assistant"):
            with st.spinner("Réflexion en cours..."):
                try:
                    response = get_llm_response(api_messages, api_key)
                    
                    # Extrait le JSON
                    json_data = extract_json(response)
                    if json_data:
                        st.session_state.collected_data = json_data.get('collected', {})
                        st.session_state.is_complete = json_data.get('complete', False)
                    
                    # Nettoie et affiche
                    clean = clean_response(response)
                    st.write(clean)
                    st.session_state.messages.append({"role": "assistant", "content": clean})
                    
                    # Lance l'analyse si complet
                    if st.session_state.is_complete:
                        st.session_state.result = run_analysis(st.session_state.collected_data)
                        st.rerun()
                        
                except Exception as e:
                    st.error(f"Erreur: {str(e)}")
