import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import base64
from datetime import datetime
 
# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(page_title="HOPE – CRM", page_icon="🐴", layout="wide", initial_sidebar_state="expanded")
 
ROSE       = "#E8186D"
ROSE_LIGHT = "#F5559A"
NOIR       = "#1A0A00"
GRIS_FOND  = "#F9F4F6"
BLANC      = "#FFFFFF"
GRIS_TEXT  = "#5C3D4A"
 
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');
    .stApp {{ background-color:{GRIS_FOND}; font-family:'DM Sans',sans-serif; }}
    [data-testid="stSidebar"] {{ background-color:{NOIR} !important; border-right:3px solid {ROSE}; }}
    [data-testid="stSidebar"] * {{ color:{BLANC} !important; }}
    h1,h2,h3 {{ font-family:'Playfair Display',serif !important; color:{NOIR} !important; }}
    .header-band {{ background:linear-gradient(90deg,{NOIR} 60%,{ROSE} 100%); border-radius:18px; padding:24px 32px; color:white; margin-bottom:28px; display:flex; align-items:center; gap:20px; }}
    .header-title {{ font-family:'Playfair Display',serif; font-size:2rem; font-weight:900; color:white; }}
    .header-sub {{ font-size:0.9rem; opacity:0.75; margin-top:4px; }}
    .section-title {{ font-family:'Playfair Display',serif; font-size:1.3rem; color:{NOIR}; font-weight:700; margin-bottom:16px; padding-bottom:8px; border-bottom:2px solid {ROSE}; display:inline-block; }}
    .kpi-card {{ background:{BLANC}; border-radius:14px; padding:20px; box-shadow:0 2px 12px rgba(232,24,109,0.08); border-left:5px solid {ROSE}; margin-bottom:12px; }}
    .kpi-number {{ font-family:'Playfair Display',serif; font-size:2.2rem; font-weight:900; color:{ROSE}; line-height:1; }}
    .kpi-label {{ font-size:0.82rem; color:{GRIS_TEXT}; margin-top:4px; text-transform:uppercase; letter-spacing:0.08em; }}
    .rank-item {{ background:rgba(255,255,255,0.07); border-radius:10px; padding:8px 12px; margin-bottom:7px; display:flex; align-items:center; gap:10px; }}
    .rank-avatar {{ width:34px; height:34px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:700; font-size:0.75rem; flex-shrink:0; }}
    .data-table {{ width:100%; border-collapse:collapse; font-family:'DM Sans',sans-serif; font-size:0.88rem; }}
    .data-table th {{ background:{NOIR}; color:white; padding:10px 14px; text-align:left; font-weight:500; }}
    .data-table td {{ padding:10px 14px; border-bottom:1px solid #f0e8ec; }}
    .data-table tr:hover td {{ background:#fdf5f8; }}
    .badge-wa       {{ background:#25D366; color:white; font-size:0.68rem; padding:2px 8px; border-radius:20px; }}
    .badge-inscrit  {{ background:#d4edda; color:#155724; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-attente  {{ background:#fff3cd; color:#856404; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-mecene   {{ background:#e8d5f5; color:#5b2d8e; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-benevole {{ background:#d0eaff; color:#0a4a8c; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-beneficiaire {{ background:#fde8f0; color:#8c0a3c; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-regulier  {{ background:#1a3a6b; color:white; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-evenement {{ background:#7c3aed; color:white; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-externe   {{ background:#374151; color:white; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-potentiel {{ background:{ROSE}; color:white; font-size:0.68rem; padding:2px 8px; border-radius:20px; }}
    .badge-actif    {{ background:#d4edda; color:#155724; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-inactif  {{ background:#f8d7da; color:#721c24; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .action-card {{ background:{BLANC}; border-radius:14px; padding:20px 24px; box-shadow:0 1px 10px rgba(0,0,0,0.06); margin-bottom:16px; border-left:4px solid {ROSE_LIGHT}; }}
    .action-title {{ font-weight:700; font-size:0.95rem; color:{NOIR}; margin-bottom:10px; }}
    .wa-source {{ background:rgba(37,211,102,0.1); border:1px solid #25D366; border-radius:8px; padding:8px 14px; font-size:0.82rem; color:#1a8a45; margin-bottom:16px; display:flex; align-items:center; gap:8px; }}
    .sidebar-sep {{ border:none; border-top:1px solid rgba(255,255,255,0.15); margin:14px 0; }}
    .newsletter-hero {{ background:linear-gradient(135deg,{ROSE} 0%,{NOIR} 100%); border-radius:18px; padding:36px 32px; color:white; text-align:center; margin-bottom:24px; }}
    .newsletter-hero h2 {{ color:white !important; font-size:1.8rem; margin-bottom:8px; }}
    .newsletter-zone {{ background:#fff5f9; border:2px dashed {ROSE_LIGHT}; border-radius:14px; padding:24px; text-align:center; margin-bottom:16px; }}
    .stat-row {{ display:flex; gap:12px; margin-bottom:20px; flex-wrap:wrap; }}
    .stat-chip {{ background:{BLANC}; border-radius:10px; padding:12px 18px; flex:1; text-align:center; box-shadow:0 1px 8px rgba(232,24,109,0.07); border-top:3px solid {ROSE}; }}
    .stat-chip-num {{ font-family:'Playfair Display',serif; font-size:1.6rem; font-weight:900; color:{ROSE}; }}
    .stat-chip-label {{ font-size:0.75rem; color:{GRIS_TEXT}; text-transform:uppercase; letter-spacing:0.06em; }}
    .antenne-card {{ background:{BLANC}; border-radius:16px; padding:24px; box-shadow:0 2px 14px rgba(232,24,109,0.08); margin-bottom:16px; border-top:4px solid {ROSE}; }}
    .transcript-block {{ background:#f8f4ff; border-radius:12px; padding:18px 20px; margin-bottom:12px; border-left:4px solid #7c3aed; font-size:0.85rem; line-height:1.7; color:#2d1a4a; }}
    .vocal-block {{ background:#fff8e1; border-radius:12px; padding:18px 20px; margin-bottom:12px; border-left:4px solid #f59e0b; font-size:0.85rem; line-height:1.7; }}
    .info-importante {{ background:#fde8f0; border-radius:10px; padding:12px 16px; margin-bottom:10px; border-left:4px solid {ROSE}; font-size:0.85rem; }}
    .mail-compose {{ background:{BLANC}; border-radius:14px; padding:24px; box-shadow:0 2px 12px rgba(0,0,0,0.07); }}
    .photo-card {{ background:{BLANC}; border-radius:12px; overflow:hidden; box-shadow:0 2px 10px rgba(0,0,0,0.08); }}
    .tool-card {{ background:{BLANC}; border-radius:14px; padding:20px; box-shadow:0 2px 12px rgba(232,24,109,0.07); border-top:3px solid {ROSE}; text-align:center; cursor:pointer; transition:transform 0.15s; }}
    .tool-card:hover {{ transform:translateY(-2px); box-shadow:0 4px 20px rgba(232,24,109,0.14); }}
    .tool-icon {{ font-size:2rem; margin-bottom:8px; }}
    .tool-name {{ font-weight:700; font-size:0.9rem; color:{NOIR}; }}
    .tool-desc {{ font-size:0.78rem; color:{GRIS_TEXT}; margin-top:4px; }}
    .tool-card-newsletter {{ background:linear-gradient(135deg,{ROSE} 0%,{NOIR} 100%); border-radius:18px; padding:28px 24px; box-shadow:0 4px 20px rgba(232,24,109,0.22); text-align:center; cursor:pointer; }}
    .tool-card-newsletter .tool-icon {{ font-size:3rem; }}
    .tool-card-newsletter .tool-name {{ color:white; font-size:1.2rem; font-family:'Playfair Display',serif; }}
    .tool-card-newsletter .tool-desc {{ color:rgba(255,255,255,0.75); font-size:0.88rem; margin-top:6px; }}
    .profil-badge {{ background:{ROSE}; color:white; font-size:0.75rem; padding:3px 12px; border-radius:20px; font-weight:600; }}
    .ant-section {{ font-weight:700; font-size:0.95rem; color:{ROSE}; margin:18px 0 8px; border-left:4px solid {ROSE}; padding-left:10px; }}
    .parcours-tag {{ font-size:0.7rem; background:#f0fdf4; color:#166534; border:1px solid #86efac; padding:2px 7px; border-radius:20px; margin-left:6px; }}
    .parcours-ext  {{ font-size:0.7rem; background:#f0f4ff; color:#1e3a8a; border:1px solid #93c5fd; padding:2px 7px; border-radius:20px; margin-left:6px; }}
    .potentiel-banner {{ background:linear-gradient(90deg,#fde8f0,#fff); border:1px solid {ROSE_LIGHT}; border-radius:10px; padding:10px 16px; margin-bottom:14px; font-size:0.85rem; color:{NOIR}; display:flex; align-items:center; gap:10px; }}
    .antenne-respo-card {{ background:{BLANC}; border-radius:14px; padding:18px 20px; box-shadow:0 2px 10px rgba(232,24,109,0.07); border-left:5px solid {ROSE}; margin-bottom:12px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
    .antenne-respo-info {{ display:flex; flex-direction:column; gap:4px; }}
    .antenne-respo-name {{ font-weight:700; font-size:1rem; color:{NOIR}; }}
    .antenne-respo-ant {{ font-size:0.8rem; color:{GRIS_TEXT}; }}
    .antenne-respo-actions {{ display:flex; gap:8px; }}
    .btn-mail {{ background:{ROSE}; color:white; border:none; border-radius:8px; padding:7px 14px; font-size:0.82rem; font-weight:600; cursor:pointer; text-decoration:none; display:inline-flex; align-items:center; gap:5px; }}
    .btn-tel {{ background:{NOIR}; color:white; border:none; border-radius:8px; padding:7px 14px; font-size:0.82rem; font-weight:600; cursor:pointer; text-decoration:none; display:inline-flex; align-items:center; gap:5px; }}
    .newsletter-compose-card {{ background:{BLANC}; border-radius:16px; padding:28px; box-shadow:0 2px 14px rgba(232,24,109,0.09); border-top:4px solid {ROSE}; }}
    .contacts-panel {{ background:{GRIS_FOND}; border-radius:14px; padding:18px; border:1px solid #f0dde6; }}
</style>
""", unsafe_allow_html=True)
 
 
# ─── LOGO ──────────────────────────────────────────────────────────────────────
def get_logo_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""
 
LOGO_PATH = r"hope_logo.jpg"
logo_b64  = get_logo_b64(LOGO_PATH)
 
# ─── DONNÉES ───────────────────────────────────────────────────────────────────
antennes = ["Paris – Île-de-France", "Lyon – Auvergne-Rhône-Alpes", "Marseille – PACA", "Bordeaux – Nouvelle-Aquitaine", "Rennes – Bretagne"]
 
centres = {
    "Paris – Île-de-France":           ["Centre Équestre de Versailles", "Poney Club de Vincennes", "Écuries du Bois de Boulogne"],
    "Lyon – Auvergne-Rhône-Alpes":     ["Centre Équestre de Lyon", "Haras de Villeurbanne"],
    "Marseille – PACA":                ["Centre Équestre d'Aix-en-Provence", "Haras de Marseille"],
    "Bordeaux – Nouvelle-Aquitaine":   ["Centre Équestre de Bordeaux", "Poney Club de Bayonne"],
    "Rennes – Bretagne":               ["Centre Équestre de Rennes", "Haras de Brest"],
}
 
# Responsables par antenne avec mail et téléphone
respos_antenne = [
    {"nom":"Annabel Marchand","antenne":"Paris – Île-de-France",         "mail":"annabel.marchand@association-hope.fr","tel":"06 12 34 56 78","emoji":"🗼"},
    {"nom":"Gilles Tournebrise", "antenne":"Lyon – Auvergne-Rhône-Alpes",  "mail":"gilles.tournebrise@association-hope.fr","tel":"06 23 45 67 89","emoji":"🦁"},
    {"nom":"Sandrine Azoulay",   "antenne":"Marseille – PACA",             "mail":"sandrine.azoulay@association-hope.fr", "tel":"06 34 56 78 90","emoji":"🌊"},
    {"nom":"Emeline Courtet",    "antenne":"Bordeaux – Nouvelle-Aquitaine","mail":"emeline.courtet@association-hope.fr",  "tel":"06 45 67 89 01","emoji":"🍷"},
    {"nom":"(En cours)",         "antenne":"Rennes – Bretagne",            "mail":"rennes@association-hope.fr",           "tel":"—",            "emoji":"⚓"},
]
 
antennes_data = [
    {"nom":"Paris – Île-de-France",         "emoji":"🗼","description":"Antenne historique fondée en 2015, la plus grande avec 3 centres partenaires.","localisation":"Paris 75, 92, 93, 94","membres":["Annabel (Resp.)","Marie D.","Claire B.","Sophie R.","Laurence P.","Nathalie V."],"couleur":ROSE},
    {"nom":"Lyon – Auvergne-Rhône-Alpes",   "emoji":"🦁","description":"Créée en 2018, très active sur les séjours découverte.","localisation":"Lyon 69, Villeurbanne","membres":["Gilles (Coord.)","Thomas M.","Julie R.","Marc S."],"couleur":"#1D9E75"},
    {"nom":"Marseille – PACA",              "emoji":"🌊","description":"Ouverte en 2019. Forte dynamique associative et nombreux partenariats.","localisation":"Marseille 13, Aix-en-Provence","membres":["Sandrine (Sec.)","Lucas P.","Nadia E.","Karim B."],"couleur":"#378ADD"},
    {"nom":"Bordeaux – Nouvelle-Aquitaine", "emoji":"🍷","description":"Antenne en pleine croissance (2021), forte présence rurale.","localisation":"Bordeaux 33, Bayonne 64","membres":["Emeline (Coord.)","Pauline D.","Romain F."],"couleur":"#BA7517"},
    {"nom":"Rennes – Bretagne",             "emoji":"⚓","description":"Dernière antenne ouverte (2023), focus journées découverte.","localisation":"Rennes 35, Brest 29","membres":["En cours de constitution"],"couleur":"#7c3aed"},
]
 
# Données réalistes : asso proche de 1M€ de dons, centaines de bénévoles
evenements = ["Journée Découverte Versailles – Mai 2025", "Séjour Été 2025", "Séjour Printemps 2025", "Séjour Hiver 2025", "Gala des Mécènes 2024"]
 
beneficiaires_data = [
    {"Prénom":"Emma",      "Nom":"Laurent",    "Téléphone":"06 12 34 56 78","Séjour":"Été 2025",      "Événement":"Séjour Été 2025",                    "Antenne":"Paris – Île-de-France",         "Mail":"emma.l@mail.com",     "Source":"WhatsApp","Potentielle_benv":"Contactée","Inscription":"Confirmée"},
    {"Prénom":"Chloé",     "Nom":"Martin",     "Téléphone":"06 34 56 78 90","Séjour":"Été 2025",      "Événement":"Séjour Été 2025",                    "Antenne":"Marseille – PACA",               "Mail":"chloe.m@mail.com",    "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"En attente"},
    {"Prénom":"Léa",       "Nom":"Rousseau",   "Téléphone":"06 56 78 90 12","Séjour":"Été 2025",      "Événement":"Journée Découverte Versailles – Mai 2025","Antenne":"Paris – Île-de-France",     "Mail":"lea.r@mail.com",      "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"Confirmée"},
    {"Prénom":"Inès",      "Nom":"Dubois",     "Téléphone":"06 78 90 12 34","Séjour":"Printemps 2025","Événement":"Séjour Printemps 2025",               "Antenne":"Lyon – Auvergne-Rhône-Alpes",    "Mail":"ines.d@mail.com",     "Source":"WhatsApp","Potentielle_benv":"Contactée","Inscription":"Confirmée"},
    {"Prénom":"Camille",   "Nom":"Perrin",     "Téléphone":"06 89 01 23 45","Séjour":"Hiver 2025",    "Événement":"Séjour Hiver 2025",                   "Antenne":"Bordeaux – Nouvelle-Aquitaine",  "Mail":"",                    "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"En attente"},
    {"Prénom":"Zoé",       "Nom":"Fontaine",   "Téléphone":"06 90 12 34 56","Séjour":"Été 2025",      "Événement":"Séjour Été 2025",                    "Antenne":"Rennes – Bretagne",              "Mail":"zoe.f@mail.com",      "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"Confirmée"},
    {"Prénom":"Sarah",     "Nom":"Benali",     "Téléphone":"06 11 22 33 44","Séjour":"Été 2025",      "Événement":"Journée Découverte Versailles – Mai 2025","Antenne":"Paris – Île-de-France",     "Mail":"sarah.b@mail.com",    "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"En attente"},
    {"Prénom":"Jade",      "Nom":"Chevalier",  "Téléphone":"06 22 33 44 55","Séjour":"Printemps 2025","Événement":"Séjour Printemps 2025",               "Antenne":"Lyon – Auvergne-Rhône-Alpes",    "Mail":"jade.c@mail.com",     "Source":"WhatsApp","Potentielle_benv":"Contactée","Inscription":"Confirmée"},
    {"Prénom":"Manon",     "Nom":"Lefebvre",   "Téléphone":"06 33 44 55 66","Séjour":"Hiver 2025",    "Événement":"Séjour Hiver 2025",                   "Antenne":"Marseille – PACA",               "Mail":"manon.l@mail.com",    "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"En attente"},
    {"Prénom":"Ambre",     "Nom":"Dupré",      "Téléphone":"06 44 55 66 77","Séjour":"Été 2025",      "Événement":"Séjour Été 2025",                    "Antenne":"Bordeaux – Nouvelle-Aquitaine",  "Mail":"ambre.d@mail.com",    "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"Confirmée"},
    {"Prénom":"Yasmine",   "Nom":"Ait Hamou",  "Téléphone":"06 55 66 77 88","Séjour":"Été 2025",      "Événement":"Journée Découverte Versailles – Mai 2025","Antenne":"Paris – Île-de-France",     "Mail":"yasmine.a@mail.com",  "Source":"WhatsApp","Potentielle_benv":"Oui",       "Inscription":"Confirmée"},
    {"Prénom":"Lola",      "Nom":"Girard",     "Téléphone":"06 66 77 88 99","Séjour":"Printemps 2025","Événement":"Séjour Printemps 2025",               "Antenne":"Rennes – Bretagne",              "Mail":"lola.g@mail.com",     "Source":"WhatsApp","Potentielle_benv":"Contactée","Inscription":"En attente"},
]
 
benevoles_data = [
    {"Prénom":"Marie",     "Nom":"Dupont",     "Téléphone":"06 11 22 33 44","Mail":"marie.d@mail.com",     "Antenne":"Paris – Île-de-France",         "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Thomas",    "Nom":"Martin",     "Téléphone":"06 22 33 44 55","Mail":"thomas.m@mail.com",    "Antenne":"Lyon – Auvergne-Rhône-Alpes",   "Type":"Régulier",     "Statut":"Relance", "Parcours":"Recrutement externe"},
    {"Prénom":"Claire",    "Nom":"Bernard",    "Téléphone":"06 33 44 55 66","Mail":"claire.b@mail.com",    "Antenne":"Paris – Île-de-France",         "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Lucas",     "Nom":"Petit",      "Téléphone":"06 44 55 66 77","Mail":"lucas.p@mail.com",     "Antenne":"Marseille – PACA",              "Type":"Événementiel", "Statut":"Inactif", "Parcours":"Recrutement externe"},
    {"Prénom":"Sophie",    "Nom":"Roux",       "Téléphone":"06 55 66 77 88","Mail":"sophie.r@mail.com",    "Antenne":"Paris – Île-de-France",         "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Emeline",   "Nom":"Cours",      "Téléphone":"06 66 77 88 99","Mail":"emeline.c@mail.com",   "Antenne":"Bordeaux – Nouvelle-Aquitaine", "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Julie",     "Nom":"Renard",     "Téléphone":"06 77 88 99 00","Mail":"julie.r@mail.com",     "Antenne":"Lyon – Auvergne-Rhône-Alpes",  "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Paul",      "Nom":"Lefort",     "Téléphone":"06 88 99 00 11","Mail":"paul.l@mail.com",      "Antenne":"Rennes – Bretagne",             "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Nadia",     "Nom":"El Amri",    "Téléphone":"06 99 00 11 22","Mail":"nadia.e@mail.com",     "Antenne":"Marseille – PACA",              "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Laura",     "Nom":"Schneider",  "Téléphone":"06 10 20 30 40","Mail":"laura.s@mail.com",     "Antenne":"Paris – Île-de-France",         "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Karim",     "Nom":"Boussaid",   "Téléphone":"06 20 30 40 50","Mail":"karim.b@mail.com",     "Antenne":"Marseille – PACA",              "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Agathe",    "Nom":"Vidal",      "Téléphone":"06 30 40 50 60","Mail":"agathe.v@mail.com",    "Antenne":"Lyon – Auvergne-Rhône-Alpes",  "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Romain",    "Nom":"Faure",      "Téléphone":"06 40 50 60 70","Mail":"romain.f@mail.com",    "Antenne":"Bordeaux – Nouvelle-Aquitaine", "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Élise",     "Nom":"Morin",      "Téléphone":"06 50 60 70 80","Mail":"elise.m@mail.com",     "Antenne":"Paris – Île-de-France",         "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Damien",    "Nom":"Leclercq",   "Téléphone":"06 60 70 80 90","Mail":"damien.l@mail.com",    "Antenne":"Rennes – Bretagne",             "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Fatima",    "Nom":"Zouaoui",    "Téléphone":"06 70 80 90 01","Mail":"fatima.z@mail.com",    "Antenne":"Paris – Île-de-France",         "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Hugo",      "Nom":"Bertrand",   "Téléphone":"06 80 90 01 12","Mail":"hugo.b@mail.com",      "Antenne":"Lyon – Auvergne-Rhône-Alpes",  "Type":"Événementiel", "Statut":"Relance", "Parcours":"Recrutement externe"},
    {"Prénom":"Pauline",   "Nom":"Deschamps",  "Téléphone":"06 90 01 12 23","Mail":"pauline.d@mail.com",   "Antenne":"Bordeaux – Nouvelle-Aquitaine", "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Marc",      "Nom":"Souchard",   "Téléphone":"06 01 12 23 34","Mail":"marc.s@mail.com",      "Antenne":"Lyon – Auvergne-Rhône-Alpes",  "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Nathalie",  "Nom":"Vasseur",    "Téléphone":"06 11 23 34 45","Mail":"nathalie.v@mail.com",  "Antenne":"Paris – Île-de-France",         "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Antoine",   "Nom":"Gimenez",    "Téléphone":"06 21 34 45 56","Mail":"antoine.g@mail.com",   "Antenne":"Marseille – PACA",              "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Coralie",   "Nom":"Blanc",      "Téléphone":"06 31 45 56 67","Mail":"coralie.b@mail.com",   "Antenne":"Rennes – Bretagne",             "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Sébastien", "Nom":"Marchal",    "Téléphone":"06 41 56 67 78","Mail":"sebastien.m@mail.com", "Antenne":"Paris – Île-de-France",         "Type":"Régulier",     "Statut":"Actif",   "Parcours":"Recrutement externe"},
    {"Prénom":"Iris",      "Nom":"Legrand",    "Téléphone":"06 51 67 78 89","Mail":"iris.l@mail.com",      "Antenne":"Bordeaux – Nouvelle-Aquitaine", "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Ancienne bénéficiaire"},
    {"Prénom":"Théo",      "Nom":"Roussel",    "Téléphone":"06 61 78 89 90","Mail":"theo.r@mail.com",      "Antenne":"Lyon – Auvergne-Rhône-Alpes",  "Type":"Événementiel", "Statut":"Actif",   "Parcours":"Recrutement externe"},
]
 
mecenes_data = [
    {"Prénom":"Jean",      "Nom":"Moreau",     "Société":"Moreau & Associés",      "Mail":"j.moreau@moreau.fr",       "Don (€)":45000,  "Reçu envoyé":"Oui","Antenne":"Paris – Île-de-France"},
    {"Prénom":"Isabelle",  "Nom":"Fontaine",   "Société":"Groupe Fontaine",        "Mail":"i.fontaine@gf.com",        "Don (€)":80000,  "Reçu envoyé":"Non","Antenne":"Lyon – Auvergne-Rhône-Alpes"},
    {"Prénom":"Pierre",    "Nom":"Gauthier",   "Société":"Gauthier Conseil",       "Mail":"p.gauthier@conseil.fr",    "Don (€)":120000, "Reçu envoyé":"Oui","Antenne":"Paris – Île-de-France"},
    {"Prénom":"Nathalie",  "Nom":"Lemoine",    "Société":"NL Équipements",         "Mail":"n.lemoine@nl.fr",          "Don (€)":35000,  "Reçu envoyé":"Non","Antenne":"Marseille – PACA"},
    {"Prénom":"François",  "Nom":"Mercier",    "Société":"Mercier Industries",     "Mail":"f.mercier@mi.fr",          "Don (€)":200000, "Reçu envoyé":"Oui","Antenne":"Bordeaux – Nouvelle-Aquitaine"},
    {"Prénom":"Hélène",    "Nom":"Desnoyers",  "Société":"HD Partenaires",         "Mail":"h.desnoyers@hdp.fr",       "Don (€)":60000,  "Reçu envoyé":"Oui","Antenne":"Paris – Île-de-France"},
    {"Prénom":"Bertrand",  "Nom":"Castaing",   "Société":"Castaing Immobilier",    "Mail":"b.castaing@castimmo.fr",   "Don (€)":90000,  "Reçu envoyé":"Non","Antenne":"Bordeaux – Nouvelle-Aquitaine"},
    {"Prénom":"Sylvie",    "Nom":"Aubert",     "Société":"Fondation Aubert",       "Mail":"s.aubert@fondaubert.org",  "Don (€)":150000, "Reçu envoyé":"Oui","Antenne":"Lyon – Auvergne-Rhône-Alpes"},
    {"Prénom":"Christophe","Nom":"Villain",    "Société":"CV Consulting",          "Mail":"c.villain@cvconsult.fr",   "Don (€)":25000,  "Reçu envoyé":"Oui","Antenne":"Marseille – PACA"},
    {"Prénom":"Valérie",   "Nom":"Truchot",    "Société":"Truchot Santé",          "Mail":"v.truchot@truchotsante.fr","Don (€)":75000,  "Reçu envoyé":"Non","Antenne":"Rennes – Bretagne"},
    {"Prénom":"Arnaud",    "Nom":"Peltier",    "Société":"Peltier Groupe",         "Mail":"a.peltier@peltiergroupe.fr","Don (€)":110000,"Reçu envoyé":"Oui","Antenne":"Paris – Île-de-France"},
]
 
classement = [
    {"rang":"🥇","nom":"Annabel","role":"Responsable",  "init":"AN","heures":47,"bg":"#F4C0D1","txt":"#993556"},
    {"rang":"🥈","nom":"Gilles",   "role":"Terrain",      "init":"GI","heures":38,"bg":"#9FE1CB","txt":"#0F6E56"},
    {"rang":"🥉","nom":"Sandrine", "role":"Secrétariat",  "init":"SA","heures":29,"bg":"#B5D4F4","txt":"#185FA5"},
    {"rang":"4️⃣","nom":"Emeline",  "role":"Événementiel", "init":"EM","heures":21,"bg":"#FAC775","txt":"#854F0B"},
]
 
profils = {
    "Annabel – Responsable nationale": {"role":"responsable","antenne":"Toutes","acces":["accueil","groupes","beneficiaires","benevoles","mecenes","newsletter","antennes","photos"]},
    "Gilles – Antenne Lyon":             {"role":"antenne",    "antenne":"Lyon – Auvergne-Rhône-Alpes","acces":["accueil","groupes","beneficiaires","benevoles","antennes","photos"]},
    "Sandrine – Secrétariat":            {"role":"secretariat","antenne":"Toutes","acces":["accueil","groupes","beneficiaires","benevoles","mecenes","newsletter","antennes","photos"]},
    "Emeline – Communication":           {"role":"communication","antenne":"Toutes","acces":["accueil","newsletter","photos","antennes"]},
    "Laurence – Antenne Paris":          {"role":"antenne",    "antenne":"Paris – Île-de-France","acces":["accueil","groupes","beneficiaires","benevoles","antennes","photos"]},
}
 
tous_contacts = []
for r in beneficiaires_data:
    if r["Mail"]: tous_contacts.append({"Prénom":r["Prénom"],"Nom":r["Nom"],"Mail":r["Mail"],"Type":"Bénéficiaire","Antenne":r["Antenne"]})
for r in benevoles_data:
    if r["Mail"]: tous_contacts.append({"Prénom":r["Prénom"],"Nom":r["Nom"],"Mail":r["Mail"],"Type":"Bénévole","Antenne":r["Antenne"]})
for r in mecenes_data:
    tous_contacts.append({"Prénom":r["Prénom"],"Nom":r["Nom"],"Mail":r["Mail"],"Type":"Mécène","Antenne":r["Antenne"]})
 
groupes_wa = [
    {"nom":"Groupe Administrateurs HOPE","membres":["Annabel","Gilles","Sandrine","Emeline","Laurence"],
     "infos_importantes":["Budget Q2 validé à 85% — vigilance frais transport","Nouvelle réglementation équestre dès sept. 2025","Recrutement coordinateur Rennes — 3 candidatures reçues"],
     "messages":[
         {"auteur":"Annabel","heure":"09:14","type":"texte","contenu":"Bonjour à tous, le dossier de subvention région IDF a été déposé hier. On attend retour sous 6 semaines."},
         {"auteur":"Gilles","heure":"09:32","type":"vocal","duree":"1min 24s","transcription":"Salut tout le monde. J'ai eu le responsable du centre de Lyon hier soir. Il confirme les dates pour le séjour de juillet. Par contre il nous demande si on peut anticiper le versement de l'acompte avant le 15 juin, sinon il ne peut pas garantir la disponibilité des chevaux. Faut valider ça rapidement."},
         {"auteur":"Sandrine","heure":"10:05","type":"texte","contenu":"Reçu Gilles. Je prépare le bon de commande aujourd'hui. Annabel tu peux valider la dépense ? L'acompte c'est 800€."},
         {"auteur":"Annabel","heure":"10:18","type":"texte","contenu":"Oui validé. Sandrine envoie-moi le bon pour signature avant midi stp."},
     ]},
    {"nom":"Groupe Coordination Séjours","membres":["Annabel","Gilles","Laurence","Marie D."],
     "infos_importantes":["Séjour été 2025 : 38 bénéficiaires confirmées, 4 places restantes","Transport 14 juillet non résolu — urgent","3 accompagnateurs manquants week-end du 21"],
     "messages":[
         {"auteur":"Laurence","heure":"08:45","type":"texte","contenu":"Bonjour équipe. J'ai finalisé la liste des bénéficiaires pour le séjour été. On a 38 jeunes confirmées, il reste 4 places."},
         {"auteur":"Gilles","heure":"09:10","type":"vocal","duree":"52s","transcription":"Pour le transport du 14 juillet, j'ai appelé deux prestataires et c'est compliqué, ils sont tous complets. J'essaie encore avec un troisième. Si ça marche pas, on va devoir faire du covoiturage bénévoles."},
         {"auteur":"Marie D.","heure":"10:22","type":"texte","contenu":"Pour les accompagnateurs, j'ai contacté Sophie et Claire, elles sont dispo le 21. Il manque encore 3 personnes."},
     ]},
]
 
photos_data = [
    {"titre":"Séjour Été 2024 – Lyon","date":"Juillet 2024","antenne":"Lyon – Auvergne-Rhône-Alpes","emoji":"🏇","description":"Retour en images sur le séjour équestre été 2024 — 42 participantes."},
    {"titre":"Journée Découverte – Paris","date":"Mai 2025","antenne":"Paris – Île-de-France","emoji":"🌸","description":"Journée découverte au Centre Équestre de Versailles, 67 participantes."},
    {"titre":"Gala des Mécènes 2024","date":"Novembre 2024","antenne":"Toutes antennes","emoji":"✨","description":"Soirée de remerciement des mécènes — 11 entreprises partenaires."},
    {"titre":"Formation Bénévoles","date":"Mars 2025","antenne":"Marseille – PACA","emoji":"📚","description":"Week-end de formation pour les nouveaux bénévoles Marseille — 28 participants."},
]
 
 
# ─── NAVIGATION STATE ──────────────────────────────────────────────────────────
menu_labels = {
    "accueil":"🏠  Accueil","groupes":"💬  Transcription Groupe HOPE","beneficiaires":"🧒  Bénéficiaires",
    "benevoles":"👥  Bénévoles","mecenes":"💼  Mécènes","newsletter":"📰  Newsletter",
    "antennes":"📍  Antennes","photos":"📷  Photos",
}
menu_labels_inv = {v: k for k, v in menu_labels.items()}  # label → key
 
def navigate_to(page_key):
    """Set current page by key (e.g. 'newsletter') and rerun."""
    st.session_state["current_page_key"] = page_key
    st.rerun()
 
# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if logo_b64:
        st.markdown(f'<div style="text-align:center;padding:14px 0 6px;"><img src="data:image/jpeg;base64,{logo_b64}" style="width:100px;border-radius:10px;" /></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:14px 0;font-size:1.8rem;color:{ROSE};">🐴 HOPE</div>', unsafe_allow_html=True)
 
    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)
 
    prev_profil = st.session_state.get("prev_profil", None)
    profil_sel = st.selectbox("Profil", list(profils.keys()), label_visibility="collapsed")
    profil     = profils[profil_sel]
 
    # Reset page when profil changes
    if prev_profil != profil_sel:
        st.session_state["prev_profil"] = profil_sel
        st.session_state["current_page_key"] = "accueil"
 
    st.markdown(f'<div style="text-align:center;margin-bottom:8px;"><span class="profil-badge">{profil["role"].upper()}</span></div>', unsafe_allow_html=True)
    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)
 
    menu_options = [menu_labels[k] for k in profil["acces"] if k in menu_labels]
 
    # Determine current index for the radio from session state
    current_key = st.session_state.get("current_page_key", "accueil")
    # Fallback if current_key not in this profil's access
    if current_key not in profil["acces"]:
        current_key = profil["acces"][0]
        st.session_state["current_page_key"] = current_key
    current_label = menu_labels.get(current_key, menu_options[0])
    current_idx = menu_options.index(current_label) if current_label in menu_options else 0
 
    selected_label = st.radio("", menu_options, index=current_idx, label_visibility="collapsed")
    # Sync radio → session state
    selected_key = menu_labels_inv.get(selected_label, "accueil")
    if selected_key != st.session_state.get("current_page_key"):
        st.session_state["current_page_key"] = selected_key
 
    page = selected_label  # keep 'page' variable for downstream if/elif checks
 
    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)
    max_h = max(p["heures"] for p in classement)
    st.markdown("<p style='font-size:0.68rem;opacity:0.4;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px;'>Classement connexions</p>", unsafe_allow_html=True)
    for p in classement:
        pct = int(p["heures"] / max_h * 100)
        st.markdown(f"""
        <div class="rank-item">
            <div style="font-size:1rem;min-width:20px;">{p['rang']}</div>
            <div class="rank-avatar" style="background:{p['bg']};color:{p['txt']};">{p['init']}</div>
            <div style="flex:1;">
                <div style="font-size:0.82rem;font-weight:600;color:{BLANC};">{p['nom']}</div>
                <div style="background:rgba(255,255,255,0.15);border-radius:4px;height:3px;margin-top:3px;overflow:hidden;">
                    <div style="width:{pct}%;height:3px;background:{ROSE};border-radius:4px;"></div>
                </div>
            </div>
            <div style="font-size:0.72rem;opacity:0.6;color:{BLANC};">{p['heures']}h</div>
        </div>
        """, unsafe_allow_html=True)
 
 
# ─── HEADER ────────────────────────────────────────────────────────────────────
logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="height:52px;border-radius:10px;" />' if logo_b64 else "🐴"
nom_user  = profil_sel.split("–")[0].strip()
role_user = profil_sel.split("–")[1].strip() if "–" in profil_sel else ""
st.markdown(f"""
<div class="header-band">
    {logo_html}
    <div style="flex:1;">
        <div class="header-title">Tableau de bord HOPE</div>
        <div class="header-sub">CRM · WhatsApp IA · {datetime.now().strftime("%d %B %Y")}</div>
    </div>
    <div style="text-align:right;">
        <div style="font-size:1rem;font-weight:700;color:white;">👤 {nom_user}</div>
        <div style="font-size:0.8rem;opacity:0.7;">{role_user}</div>
    </div>
</div>
""", unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : ACCUEIL
# ═══════════════════════════════════════════════════════════════════════════════
if "Accueil" in page:
    role = profil["role"]
    antenne_profil = profil["antenne"]
 
    # ── Infos importantes WhatsApp (remplacent les KPIs) ──
    # On collecte toutes les infos importantes de tous les groupes accessibles
    all_infos = []
    for g in groupes_wa:
        for info in g["infos_importantes"]:
            all_infos.append({"info": info, "groupe": g["nom"]})
 
    st.markdown('<span class="section-title">⚡ Infos importantes — Groupes HOPE</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="wa-source" style="margin-bottom:16px;"><span>💬</span><span>Remontées automatiquement depuis les <strong>groupes WhatsApp HOPE</strong></span></div>', unsafe_allow_html=True)
 
    cols_inf = st.columns(2)
    for i, item in enumerate(all_infos):
        with cols_inf[i % 2]:
            st.markdown(f"""
            <div style="background:{BLANC};border-radius:12px;padding:14px 18px;margin-bottom:10px;
                        border-left:4px solid {ROSE};box-shadow:0 2px 10px rgba(232,24,109,0.07);">
                <div style="font-size:0.72rem;color:{GRIS_TEXT};text-transform:uppercase;letter-spacing:0.06em;margin-bottom:4px;">
                    💬 {item['groupe']}
                </div>
                <div style="font-size:0.88rem;color:{NOIR};font-weight:500;">⚠️ {item['info']}</div>
            </div>
            """, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── Actualité — retour en images ──
    if "photos" in profil["acces"]:
        dernier_album = photos_data[1]  # Journée Découverte Paris - Mai 2025, le plus récent
        st.markdown('<span class="section-title">📸 Actualité — Retour en images</span>', unsafe_allow_html=True)
        col_actu, col_actu_btn = st.columns([3, 1])
        with col_actu:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{NOIR} 0%,{ROSE} 100%);border-radius:16px;
                        padding:28px 32px;color:white;display:flex;align-items:center;gap:24px;">
                <div style="font-size:4rem;">{dernier_album['emoji']}</div>
                <div>
                    <div style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:900;margin-bottom:6px;">
                        {dernier_album['titre']}
                    </div>
                    <div style="opacity:0.8;font-size:0.88rem;margin-bottom:6px;">
                        📅 {dernier_album['date']} · 📍 {dernier_album['antenne']}
                    </div>
                    <div style="font-size:0.85rem;opacity:0.9;">{dernier_album['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_actu_btn:
            st.markdown("<br><br>", unsafe_allow_html=True)
            if st.button("📷 Voir tous les albums", key="btn_photos_actu", use_container_width=True, type="primary"):
                navigate_to("photos")
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── BLOCS OUTILS — Newsletter en grand, reste en grille avec boutons fonctionnels ──
    st.markdown('<span class="section-title">🛠️ Accès rapide</span>', unsafe_allow_html=True)
 
    outils_acces = profil["acces"]
 
    outil_map = {
        "beneficiaires": ("🧒", "Bénéficiaires",    "Gérer les jeunes accompagnées"),
        "benevoles":     ("👥", "Bénévoles",         "Gérer les bénévoles"),
        "mecenes":       ("💼", "Mécènes",           "Gérer les mécènes et les dons"),
        "groupes":       ("💬", "Transcription HOPE", "Messages & vocaux transcrits"),
        "antennes":      ("📍", "Antennes",          "Fiches antennes et responsables"),
        "photos":        ("📷", "Photos",            "Albums et galerie"),
        "newsletter":    ("📰", "Newsletter",        "Envoyer une campagne à tous vos contacts"),
    }
 
    if "newsletter" in outils_acces:
        col_nws, col_rest = st.columns([1, 2])
        with col_nws:
            st.markdown(f"""
            <div class="tool-card-newsletter">
                <div class="tool-icon">📰</div>
                <div class="tool-name">Newsletter</div>
                <div class="tool-desc">Envoyer une campagne à tous vos contacts</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("→ Newsletter", key="btn_nws_accueil", use_container_width=True):
                navigate_to("newsletter")
 
        with col_rest:
            autres = [k for k in outils_acces if k not in ["accueil", "newsletter"]]
            cols_tools = st.columns(3)
            for i, k in enumerate(autres):
                if k in outil_map:
                    icon, nom, desc = outil_map[k]
                    with cols_tools[i % 3]:
                        st.markdown(f'<div class="tool-card"><div class="tool-icon">{icon}</div><div class="tool-name">{nom}</div><div class="tool-desc">{desc}</div></div>', unsafe_allow_html=True)
                        if st.button(f"→ {nom}", key=f"btn_{k}_accueil", use_container_width=True):
                            navigate_to(k)
    else:
        autres = [k for k in outils_acces if k != "accueil"]
        cols_tools = st.columns(4)
        for i, k in enumerate(autres):
            if k in outil_map:
                icon, nom, desc = outil_map[k]
                with cols_tools[i % 4]:
                    st.markdown(f'<div class="tool-card"><div class="tool-icon">{icon}</div><div class="tool-name">{nom}</div><div class="tool-desc">{desc}</div></div>', unsafe_allow_html=True)
                    if st.button(f"→ {nom}", key=f"btn_{k}_accueil", use_container_width=True):
                        navigate_to(k)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : BÉNÉFICIAIRES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Bénéficiaires" in page:
    st.markdown('<span class="section-title">🧒 Bénéficiaires — Jeunes femmes accompagnées</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="wa-source"><span>💬</span><span>Données récupérées automatiquement via l\'<strong>API WhatsApp</strong></span></div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="potentiel-banner">
        <span style="font-size:1.3rem;">💡</span>
        <span>Toutes les bénéficiaires sont considérées comme <strong>bénévoles potentielles</strong>.
        Le statut de démarche est indiqué dans la colonne <em>Potentielle</em>.</span>
    </div>
    """, unsafe_allow_html=True)
 
    df_ben = pd.DataFrame(beneficiaires_data).sort_values("Antenne")
    antenne_profil = profil["antenne"]
 
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1:
        ant_opts = [antenne_profil] if antenne_profil != "Toutes" else ["Toutes les antennes"] + antennes
        ant_sel  = st.selectbox("📍 Antenne", ant_opts)
    with col_f2:
        evt_opts = ["Tous les événements"] + sorted(df_ben["Événement"].unique().tolist())
        evt_sel  = st.selectbox("🎪 Événement", evt_opts)
    with col_f3:
        sejour_sel = st.selectbox("🏕️ Séjour", ["Tous"] + sorted(df_ben["Séjour"].unique().tolist()))
    with col_f4:
        pot_sel = st.selectbox("🌱 Statut bénévole potentielle", ["Toutes","Oui","Contactée"])
 
    if ant_sel != "Toutes les antennes":          df_ben = df_ben[df_ben["Antenne"] == ant_sel]
    if evt_sel != "Tous les événements":           df_ben = df_ben[df_ben["Événement"] == evt_sel]
    if sejour_sel != "Tous":                       df_ben = df_ben[df_ben["Séjour"] == sejour_sel]
    if pot_sel != "Toutes":                        df_ben = df_ben[df_ben["Potentielle_benv"] == pot_sel]
 
    # Résumé inscription si filtre événement actif
    if evt_sel != "Tous les événements":
        nb_conf = len(df_ben[df_ben["Inscription"]=="Confirmée"])
        nb_att  = len(df_ben[df_ben["Inscription"]=="En attente"])
        st.markdown(f"""
        <div style="background:{BLANC};border-radius:12px;padding:14px 20px;margin-bottom:14px;
                    display:flex;gap:20px;align-items:center;box-shadow:0 2px 10px rgba(232,24,109,0.07);
                    border-top:3px solid {ROSE};">
            <div style="font-size:0.85rem;font-weight:700;color:{NOIR};">📋 {evt_sel}</div>
            <div style="margin-left:auto;display:flex;gap:12px;">
                <span style="background:#d4edda;color:#155724;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;">
                    ✅ {nb_conf} confirmée(s)
                </span>
                <span style="background:#fff3cd;color:#856404;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;">
                    ⏳ {nb_att} en attente
                </span>
                <span style="background:#f0e8ff;color:#5b21b6;padding:4px 12px;border-radius:20px;font-size:0.8rem;font-weight:600;">
                    👥 {len(df_ben)} total
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    for ant in df_ben["Antenne"].unique():
        df_a = df_ben[df_ben["Antenne"] == ant]
        st.markdown(f'<div class="ant-section">📍 {ant} ({len(df_a)})</div>', unsafe_allow_html=True)
        html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Téléphone</th><th>Événement</th><th>Séjour</th><th>Mail</th><th>Inscription</th><th>Bénévole potentielle</th><th>Source</th></tr>'
        for _, row in df_a.iterrows():
            mail_cell = row['Mail'] if row['Mail'] else f'<span style="color:{ROSE};font-size:0.8rem;">+ Ajouter</span>'
            if row["Potentielle_benv"] == "Contactée":
                pot_badge = f'<span style="background:#fef9c3;color:#854d0e;font-size:0.7rem;padding:2px 8px;border-radius:20px;">📩 Contactée</span>'
            else:
                pot_badge = f'<span class="badge-potentiel">🌱 Oui</span>'
            if row["Inscription"] == "Confirmée":
                insc_badge = '<span class="badge-actif">✅ Confirmée</span>'
            else:
                insc_badge = '<span class="badge-attente">⏳ En attente</span>'
            html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td>{row["Téléphone"]}</td><td style="font-size:0.78rem;color:{GRIS_TEXT};">{row["Événement"]}</td><td><span class="badge-inscrit">{row["Séjour"]}</span></td><td>{mail_cell}</td><td>{insc_badge}</td><td>{pot_badge}</td><td><span class="badge-wa">📱 WA</span></td></tr>'
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # Actions groupées
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        st.markdown(f'<div class="action-card"><div class="action-title">✅ Valider les inscriptions en attente</div></div>', unsafe_allow_html=True)
        att_list = [f"{r['Prénom']} {r['Nom']} — {r['Événement']}" for _, r in df_ben.iterrows() if r["Inscription"] == "En attente"]
        sel_val = st.multiselect("Bénéficiaires à valider", att_list, default=att_list, key="sel_val")
        if st.button("✅ Valider les inscriptions sélectionnées", type="primary", key="btn_val"):
            st.success(f"✅ {len(sel_val)} inscription(s) confirmée(s) !")
    with col_act2:
        st.markdown(f'<div class="action-card"><div class="action-title">📧 Envoyer une proposition de bénévolat</div></div>', unsafe_allow_html=True)
        dest_pot = [f"{r['Prénom']} {r['Nom']}" for _, r in df_ben.iterrows() if r['Mail'] and r['Potentielle_benv'] == "Oui"]
        sel_pot  = st.multiselect("Potentielles non encore contactées", dest_pot, default=dest_pot, key="sel_pot")
        if st.button("📤 Envoyer la proposition de bénévolat", type="primary", key="btn_benv"):
            st.success(f"✅ Proposition envoyée à {len(sel_pot)} bénéficiaire(s). Leur statut passera à « Contactée ».")
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : BÉNÉVOLES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Bénévoles" in page:
    st.markdown('<span class="section-title">👥 Gestion des bénévoles</span>', unsafe_allow_html=True)
 
    df_bv = pd.DataFrame(benevoles_data)
    nb_reg = len(df_bv[df_bv["Type"]=="Régulier"])
    nb_evt = len(df_bv[df_bv["Type"]=="Événementiel"])
    nb_anc = len(df_bv[df_bv["Parcours"]=="Ancienne bénéficiaire"])
    nb_ext = len(df_bv[df_bv["Parcours"]=="Recrutement externe"])
    col1,col2,col3,col4 = st.columns(4)
    with col1: st.markdown(f'<div class="kpi-card" style="border-left-color:#1a3a6b;"><div class="kpi-number" style="color:#1a3a6b;">{nb_reg}</div><div class="kpi-label">Réguliers</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="kpi-card" style="border-left-color:#7c3aed;"><div class="kpi-number" style="color:#7c3aed;">{nb_evt}</div><div class="kpi-label">Événementiels</div></div>', unsafe_allow_html=True)
    with col3: st.markdown(f'<div class="kpi-card" style="border-left-color:{ROSE};"><div class="kpi-number" style="color:{ROSE};">{nb_anc}</div><div class="kpi-label">Anciennes bénéficiaires</div></div>', unsafe_allow_html=True)
    with col4: st.markdown(f'<div class="kpi-card" style="border-left-color:#374151;"><div class="kpi-number" style="color:#374151;">{nb_ext}</div><div class="kpi-label">Recrutement externe</div></div>', unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Tous les bénévoles","🔵 Réguliers","🟣 Événementiels","➕ Ajouter / Inviter"])
 
    def render_benevoles_table(df_filtered):
        antenne_profil = profil["antenne"]
        if antenne_profil != "Toutes":
            df_filtered = df_filtered[df_filtered["Antenne"] == antenne_profil]
        ant_f = st.selectbox("📍 Antenne", (["Toutes"] + antennes) if profil["antenne"]=="Toutes" else [profil["antenne"]], key=f"ant_{id(df_filtered)}")
        if ant_f != "Toutes": df_filtered = df_filtered[df_filtered["Antenne"]==ant_f]
        for ant in df_filtered["Antenne"].unique():
            df_a = df_filtered[df_filtered["Antenne"]==ant]
            st.markdown(f'<div class="ant-section">📍 {ant} ({len(df_a)})</div>', unsafe_allow_html=True)
            html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Téléphone</th><th>Mail</th><th>Type</th><th>Parcours</th><th>Statut</th></tr>'
            for _, row in df_a.iterrows():
                if row["Type"]=="Régulier":     type_b = '<span class="badge-regulier">Régulier</span>'
                elif row["Type"]=="Événementiel": type_b = '<span class="badge-evenement">Événementiel</span>'
                else:                            type_b = '<span class="badge-externe">Externe</span>'
                if row["Parcours"]=="Ancienne bénéficiaire": parc_b = f'<span class="parcours-tag">🌱 Anc. bénéficiaire</span>'
                else:                                         parc_b = f'<span class="parcours-ext">🔗 Recrutement ext.</span>'
                if row["Statut"]=="Actif":    stat_b = '<span class="badge-actif">Actif</span>'
                elif row["Statut"]=="Relance": stat_b = '<span class="badge-attente">Relance</span>'
                else:                          stat_b = '<span class="badge-inactif">Inactif</span>'
                html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td>{row["Téléphone"]}</td><td style="font-size:0.82rem;">{row["Mail"] or "—"}</td><td>{type_b}</td><td>{parc_b}</td><td>{stat_b}</td></tr>'
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
 
    with tab1:
        render_benevoles_table(df_bv.sort_values(["Antenne","Type"]).copy())
 
    with tab2:
        st.markdown(f'<div class="potentiel-banner"><span style="font-size:1.2rem;">🔵</span><span>Les bénévoles <strong>réguliers</strong> s\'engagent sur la durée. Ils constituent le cœur de l\'association.</span></div>', unsafe_allow_html=True)
        render_benevoles_table(df_bv[df_bv["Type"]=="Régulier"].sort_values("Antenne").copy())
 
    with tab3:
        st.markdown(f'<div class="potentiel-banner" style="background:linear-gradient(90deg,#f0e8ff,#fff);border-color:#c4b5fd;"><span style="font-size:1.2rem;">🟣</span><span>Les bénévoles <strong>événementiels</strong> interviennent ponctuellement sur des séjours ou journées découverte spécifiques.</span></div>', unsafe_allow_html=True)
        render_benevoles_table(df_bv[df_bv["Type"]=="Événementiel"].sort_values("Antenne").copy())
 
    with tab4:
        st.markdown("#### ➕ Ajouter un bénévole")
        mode = st.radio("Mode", ["Saisie manuelle (externe)","Convertir une bénéficiaire"], horizontal=True)
 
        if mode == "Saisie manuelle (externe)":
            st.info("Ce bénévole sera marqué comme **recrutement externe** — il n'est pas issu du parcours bénéficiaire.")
            c1,c2 = st.columns(2)
            with c1:
                pf = st.text_input("Prénom *")
                tf = st.text_input("Téléphone")
                ant_add = st.selectbox("Antenne *", antennes, key="ant_add")
            with c2:
                nf = st.text_input("Nom *")
                mf = st.text_input("Mail")
                type_add = st.selectbox("Type d'engagement", ["Régulier","Événementiel"], key="type_add")
            if st.button("✅ Ajouter le bénévole", type="primary"):
                if pf and nf:
                    st.success(f"✅ {pf} {nf} ajouté(e) comme bénévole {type_add} (recrutement externe) sur l'antenne {ant_add} !")
                else: st.warning("⚠️ Prénom et nom obligatoires.")
        else:
            st.info("La bénéficiaire convertie sera marquée **ancienne bénéficiaire** dans son profil bénévole.")
            choix = st.selectbox("Choisir une bénéficiaire", [f"{r['Prénom']} {r['Nom']} – {r['Antenne']}" for r in beneficiaires_data])
            type_conv = st.radio("Type d'engagement souhaité", ["Régulier","Événementiel"], horizontal=True, key="type_conv")
            if st.button("🔄 Convertir en bénévole", type="primary"):
                st.success(f"✅ {choix.split('–')[0].strip()} est maintenant bénévole {type_conv} (ancienne bénéficiaire) !")
 
        st.markdown("---")
        st.markdown("#### 📧 Inviter des bénévoles à un événement")
        col_inv1, col_inv2 = st.columns(2)
        with col_inv1:
            type_evt  = st.radio("Type d'événement", ["Séjour","Journée découverte"], horizontal=True, key="type_evt_inv")
            date_evt  = st.date_input("Date", key="date_inv")
        with col_inv2:
            cible_inv = st.multiselect("Cibler par type de bénévole", ["Régulier","Événementiel"], default=["Régulier","Événementiel"])
            ant_inv   = st.selectbox("Antenne cible", ["Toutes"] + antennes, key="ant_inv")
 
        df_inv = df_bv[df_bv["Type"].isin(cible_inv)]
        if ant_inv != "Toutes": df_inv = df_inv[df_inv["Antenne"]==ant_inv]
        benv_inv = [f"{r['Prénom']} {r['Nom']}" for _, r in df_inv.iterrows() if r['Mail']]
        sel_inv  = st.multiselect("Sélection finale", benv_inv, default=benv_inv)
        if st.button(f"📤 Envoyer l'invitation ({type_evt})", type="primary"):
            st.success(f"✅ Invitation {type_evt} du {date_evt.strftime('%d/%m/%Y')} envoyée à {len(sel_inv)} bénévole(s) !")
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : MÉCÈNES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Mécènes" in page:
    st.markdown('<span class="section-title">💼 Gestion des mécènes</span>', unsafe_allow_html=True)
    tab_m1,tab_m2,tab_m3,tab_m4 = st.tabs(["📋 Liste par antenne","🎉 Invitation événement","🧾 Reçu fiscal","➕ Ajouter un mécène"])
    df_mec = pd.DataFrame(mecenes_data).sort_values("Antenne")
    with tab_m1:
        ant_mec = st.selectbox("📍 Antenne",["Toutes les antennes"]+antennes,key="ant_mec_liste")
        df_m = df_mec if ant_mec=="Toutes les antennes" else df_mec[df_mec["Antenne"]==ant_mec]
        for ant in df_m["Antenne"].unique():
            df_a = df_m[df_m["Antenne"]==ant]
            st.markdown(f'<div class="ant-section">📍 {ant}</div>', unsafe_allow_html=True)
            html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Société</th><th>Mail</th><th>Don (€)</th><th>Reçu</th></tr>'
            for _,row in df_a.iterrows():
                recu = '<span class="badge-actif">Envoyé</span>' if row['Reçu envoyé']=="Oui" else '<span class="badge-attente">En attente</span>'
                html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td style="font-size:0.82rem;">{row["Société"]}</td><td style="font-size:0.82rem;">{row["Mail"]}</td><td style="font-weight:700;color:{ROSE};">{row["Don (€)"]:,} €</td><td>{recu}</td></tr>'
            html += "</table>"
            st.markdown(html, unsafe_allow_html=True)
        st.markdown(f'<div style="text-align:right;margin-top:10px;font-family:Playfair Display,serif;">Total : <strong style="color:{ROSE};">{df_m["Don (€)"].sum():,} €</strong></div>', unsafe_allow_html=True)
    with tab_m2:
        mec_liste=[f"{r['Prénom']} {r['Nom']} – {r['Société']}" for _,r in df_mec.iterrows()]
        sel_mec=st.multiselect("Mécènes",mec_liste,default=mec_liste)
        nom_evt=st.text_input("Événement",placeholder="ex : Gala annuel HOPE 2025")
        date_evt_m=st.date_input("Date",key="date_mec")
        lieu_evt=st.text_input("Lieu",placeholder="ex : Château de Versailles")
        st.markdown(f'<div class="action-card"><div class="action-title">📎 Joindre un document</div></div>', unsafe_allow_html=True)
        fichier_inv=st.file_uploader("Document",type=["pdf","png","jpg","docx"],key="inv_mec")
        if st.button("📤 Envoyer",type="primary"):
            extra=f" + « {fichier_inv.name} »" if fichier_inv else ""
            st.success(f"✅ Invitation « {nom_evt} »{extra} envoyée à {len(sel_mec)} mécène(s) !")
    with tab_m3:
        mec_r=st.selectbox("Mécène",[f"{r['Prénom']} {r['Nom']} – {r['Société']} ({r['Don (€)']:,} €)" for _,r in df_mec.iterrows()])
        msg_r=st.text_area("Message",value="Madame, Monsieur,\n\nNous vous remercions chaleureusement pour votre soutien à l'association HOPE.\nVeuillez trouver ci-joint votre reçu fiscal.\n\nL'équipe HOPE",height=120)
        recu_f=st.file_uploader("Reçu fiscal (PDF)",type=["pdf"])
        if st.button("📨 Envoyer",type="primary"):
            if recu_f: st.success(f"✅ Envoyé à {mec_r.split('–')[0].strip()} !"); st.balloons()
            else: st.warning("⚠️ Déposez le reçu fiscal.")
    with tab_m4:
        st.markdown(f'<div class="action-card"><div class="action-title">➕ Ajouter un mécène</div></div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        with c1:
            prenom_m=st.text_input("Prénom *",key="pm"); societe_m=st.text_input("Société",key="sm")
            don_num=st.number_input("Don numéraire (€)",min_value=0,step=1000,key="dn")
            antenne_m=st.selectbox("Antenne *",antennes,key="am"); numero_m=st.text_input("Numéro de dossier",key="num_m")
        with c2:
            nom_m=st.text_input("Nom *",key="nm"); mail_m=st.text_input("Mail *",key="mm")
            mecen_comp=st.text_input("Mécénat en compétence (société/nom)",key="mc")
            recu_m=st.selectbox("Reçu fiscal envoyé ?",["Non","Oui"],key="rm"); info_m=st.text_input("Info / Contact",key="im")
        info_comp_m=st.text_area("Informations complémentaires",key="icm",height=80)
        if st.button("✅ Ajouter",type="primary",key="btn_mec"):
            if prenom_m and nom_m and mail_m: st.success(f"✅ {prenom_m} {nom_m} ajouté(e) — Don : {don_num:,} € — Antenne : {antenne_m} !")
            else: st.warning("⚠️ Prénom, nom et mail obligatoires.")
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : NEWSLETTER — compose à gauche, contacts à droite
# ═══════════════════════════════════════════════════════════════════════════════
elif "Newsletter" in page:
    st.markdown(f'<div class="newsletter-hero"><h2>📰 Newsletter HOPE</h2><p style="opacity:0.85;">Envoyez votre newsletter à l\'ensemble de vos contacts en quelques clics</p></div>', unsafe_allow_html=True)
 
    nb_ben  = sum(1 for r in beneficiaires_data if r["Mail"])
    nb_benv = sum(1 for r in benevoles_data if r["Mail"])
    nb_mec  = len(mecenes_data)
    st.markdown(f'<div class="stat-row"><div class="stat-chip"><div class="stat-chip-num">{nb_ben+nb_benv+nb_mec}</div><div class="stat-chip-label">Total destinataires</div></div><div class="stat-chip" style="border-top-color:#8c0a3c;"><div class="stat-chip-num" style="color:#8c0a3c;">{nb_ben}</div><div class="stat-chip-label">Bénéficiaires</div></div><div class="stat-chip" style="border-top-color:#0a4a8c;"><div class="stat-chip-num" style="color:#0a4a8c;">{nb_benv}</div><div class="stat-chip-label">Bénévoles</div></div><div class="stat-chip" style="border-top-color:#5b2d8e;"><div class="stat-chip-num" style="color:#5b2d8e;">{nb_mec}</div><div class="stat-chip-label">Mécènes</div></div></div>', unsafe_allow_html=True)
 
    # Deux colonnes : compose à gauche (plus large), liste contacts à droite
    col_compose, col_contacts = st.columns([3, 2])
 
    with col_compose:
        st.markdown('<span class="section-title">✉️ Composer et envoyer</span>', unsafe_allow_html=True)
        st.markdown('<div class="newsletter-compose-card">', unsafe_allow_html=True)
 
        st.markdown("**📎 Fichier newsletter**")
        nws_file = st.file_uploader("", type=["pdf","png","jpg","jpeg","docx"], label_visibility="collapsed", key="nws_file")
        if nws_file:
            st.success(f"✅ Fichier chargé : {nws_file.name}")
 
        objet = st.text_input("📌 Objet", placeholder="Newsletter HOPE – Été 2025")
        msg_nws = st.text_area("💬 Message d'accompagnement", value="Bonjour,\n\nVeuillez trouver ci-joint la newsletter HOPE de cet été.\n\nBonne lecture !\n\nL'équipe HOPE", height=140)
 
        st.markdown("</div>", unsafe_allow_html=True)
 
        # Filtres destinataires (sous le compose)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="section-title" style="font-size:1rem;">🎯 Filtrer les destinataires</span>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            filtre_type = st.multiselect("Type", ["Bénéficiaire","Bénévole","Mécène"], default=["Bénéficiaire","Bénévole","Mécène"])
        with c2:
            filtre_ant = st.multiselect("Antenne", antennes, default=antennes)
 
        df_c = pd.DataFrame(tous_contacts)
        df_c = df_c[df_c["Type"].isin(filtre_type) & df_c["Antenne"].isin(filtre_ant)]
        nb_dest = len(df_c)
 
        st.markdown(f'<div style="background:{GRIS_FOND};border-radius:10px;padding:12px 16px;margin-bottom:12px;font-size:0.88rem;color:{GRIS_TEXT};">👥 <strong style="color:{NOIR};">{nb_dest} destinataire(s)</strong> sélectionné(s) après filtrage</div>', unsafe_allow_html=True)
 
        if st.button(f"📤 Envoyer à {nb_dest} destinataire(s)", type="primary", use_container_width=True):
            if nws_file and objet:
                st.success(f"✅ Newsletter envoyée à {nb_dest} contact(s) !")
                st.balloons()
            elif not nws_file:
                st.warning("⚠️ Déposez d'abord le fichier newsletter.")
            else:
                st.warning("⚠️ Renseignez l'objet du mail.")
 
    with col_contacts:
        st.markdown('<span class="section-title">📋 Liste des contacts</span>', unsafe_allow_html=True)
        st.markdown('<div class="contacts-panel">', unsafe_allow_html=True)
        html = f'<table class="data-table" style="font-size:0.8rem;"><tr><th>Prénom</th><th>Nom</th><th>Type</th><th>Antenne</th></tr>'
        for _, row in df_c.iterrows():
            if row["Type"]=="Bénéficiaire": b='<span class="badge-beneficiaire">Bénéf.</span>'
            elif row["Type"]=="Bénévole":   b='<span class="badge-benevole">Bénév.</span>'
            else:                           b='<span class="badge-mecene">Mécène</span>'
            ant_short = row["Antenne"].split("–")[0].strip()
            html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td>{b}</td><td style="font-size:0.75rem;color:{GRIS_TEXT};">{ant_short}</td></tr>'
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : GROUPES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Transcription" in page:
    st.markdown('<span class="section-title">💬 Transcription Groupe HOPE — Messages & vocaux</span>', unsafe_allow_html=True)
    groupe_sel=st.selectbox("Groupe",[g["nom"] for g in groupes_wa])
    groupe=next(g for g in groupes_wa if g["nom"]==groupe_sel)
    col_g1,col_g2=st.columns([2,1])
    with col_g1:
        st.markdown(f"<p style='font-size:0.82rem;color:{GRIS_TEXT};margin-bottom:16px;'>👥 {', '.join(groupe['membres'])}</p>", unsafe_allow_html=True)
        for msg in groupe["messages"]:
            if msg["type"]=="vocal":
                st.markdown(f'<div class="vocal-block"><div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;"><span style="font-size:1.2rem;">🎙️</span><div><span style="font-weight:700;color:{NOIR};">{msg["auteur"]}</span><span style="font-size:0.75rem;color:{GRIS_TEXT};margin-left:8px;">{msg["heure"]} · {msg["duree"]}</span></div><span style="margin-left:auto;background:#f59e0b;color:white;font-size:0.7rem;padding:2px 8px;border-radius:20px;">🎙️ Transcription IA</span></div><div style="background:white;border-radius:8px;padding:12px;font-size:0.85rem;line-height:1.7;border-left:3px solid #f59e0b;">« {msg["transcription"]} »</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="transcript-block"><span style="font-weight:700;color:{NOIR};">{msg["auteur"]}</span><span style="font-size:0.75rem;color:#7c3aed;margin-left:8px;">{msg["heure"]}</span><div style="margin-top:6px;">{msg["contenu"]}</div></div>', unsafe_allow_html=True)
    with col_g2:
        st.markdown('<span class="section-title" style="font-size:1rem;">⚡ Infos importantes</span>', unsafe_allow_html=True)
        for info in groupe["infos_importantes"]:
            st.markdown(f'<div class="info-importante">⚠️ {info}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-card" style="margin-top:16px;"><div class="kpi-number">{len(groupe["messages"])}</div><div class="kpi-label">Messages</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="kpi-card" style="border-left-color:#f59e0b;"><div class="kpi-number" style="color:#f59e0b;">{sum(1 for m in groupe["messages"] if m["type"]=="vocal")}</div><div class="kpi-label">Vocaux transcrits</div></div>', unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : ANTENNES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Antennes" in page:
    st.markdown('<span class="section-title">📍 Espace Antennes</span>', unsafe_allow_html=True)
    tab_a1,tab_a2=st.tabs(["🗺️ Nos antennes","📋 Guide Antenne"])
    with tab_a1:
        # ── Tableau des responsables ──
        st.markdown('<span class="section-title" style="font-size:1.1rem;">📞 Responsables d\'antenne</span>', unsafe_allow_html=True)
        ant_profil_filtre = profil["antenne"]
        respos_show = respos_antenne if ant_profil_filtre == "Toutes" else [r for r in respos_antenne if r["antenne"] == ant_profil_filtre]
        for r in respos_show:
            tel_part = f'<a class="btn-tel" href="tel:{r["tel"].replace(" ","")}" style="text-decoration:none;">📞 {r["tel"]}</a>' if r["tel"] != "—" else '<span style="font-size:0.8rem;color:#aaa;">Tél. non renseigné</span>'
            st.markdown(f"""
            <div class="antenne-respo-card">
                <div class="antenne-respo-info">
                    <div class="antenne-respo-name">{r['emoji']} {r['nom']}</div>
                    <div class="antenne-respo-ant">{r['antenne']}</div>
                    <div style="font-size:0.78rem;color:{GRIS_TEXT};margin-top:2px;">✉️ {r['mail']}</div>
                </div>
                <div class="antenne-respo-actions">
                    <a class="btn-mail" href="mailto:{r['mail']}?subject=HOPE - Contact responsable antenne" style="text-decoration:none;">✉️ Envoyer un mail</a>
                    {tel_part}
                </div>
            </div>
            """, unsafe_allow_html=True)
 
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<span class="section-title" style="font-size:1.1rem;">🗺️ Fiches antennes</span>', unsafe_allow_html=True)
 
        for ant in antennes_data:
            with st.expander(f"{ant['emoji']}  {ant['nom']}", expanded=False):
                col_i,col_m=st.columns([2,1])
                with col_i:
                    st.markdown(f'<div class="antenne-card"><div style="font-size:2.5rem;">{ant["emoji"]}</div><div style="font-weight:700;font-size:1.1rem;color:{NOIR};margin:8px 0;">{ant["nom"]}</div><div style="font-size:0.88rem;color:{GRIS_TEXT};line-height:1.6;">{ant["description"]}</div><div style="font-size:0.85rem;margin-top:10px;">📍 {ant["localisation"]}</div></div>', unsafe_allow_html=True)
                with col_m:
                    st.markdown(f"<div style='font-weight:700;margin-bottom:10px;'>👥 Équipe</div>", unsafe_allow_html=True)
                    for m in ant["membres"]: st.markdown(f"<div style='background:{GRIS_FOND};border-radius:8px;padding:8px 12px;margin-bottom:6px;font-size:0.85rem;'>👤 {m}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-weight:700;margin:10px 0 6px;'>🐴 Centres partenaires</div>", unsafe_allow_html=True)
                    for c in centres.get(ant["nom"],[]): st.markdown(f"<div style='font-size:0.82rem;padding:4px 0 4px 12px;color:{GRIS_TEXT};'>🐴 {c}</div>", unsafe_allow_html=True)
    with tab_a2:
        for icon,titre,contenu in [
            ("🚀","Démarrer avec le CRM","Connectez-vous avec votre profil antenne. Le dashboard s'adapte à votre rôle."),
            ("💬","WhatsApp","Continuez vos groupes habituels. L'API récupère automatiquement les données."),
            ("🧒","Bénéficiaires","Toutes sont bénévoles potentielles. Vous pouvez déclencher une proposition directement."),
            ("👥","Bénévoles","Ajoutez manuellement ou convertissez une bénéficiaire. Distinguez réguliers et événementiels."),
            ("📰","Newsletter","Déposez un PDF et sélectionnez vos destinataires. Envoi automatique."),
            ("🆘","Support","Contactez Annabel ou Sandrine via l'Accueil → Responsables des antennes."),
        ]:
            st.markdown(f'<div class="action-card"><div class="action-title">{icon} {titre}</div><div style="font-size:0.85rem;color:{GRIS_TEXT};">{contenu}</div></div>', unsafe_allow_html=True)
 
 
# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : PHOTOS
# ═══════════════════════════════════════════════════════════════════════════════
elif "Photos" in page:
    st.markdown('<span class="section-title">📷 Albums photos</span>', unsafe_allow_html=True)
    ant_photo=st.selectbox("📍 Antenne",["Toutes"]+antennes)
    photos_f=[p for p in photos_data if ant_photo in ["Toutes",p["antenne"],"Toutes antennes"]]
    cols=st.columns(2)
    for i,photo in enumerate(photos_f):
        with cols[i%2]:
            st.markdown(f'<div class="photo-card"><div style="background:linear-gradient(135deg,{NOIR} 0%,{ROSE} 100%);height:130px;display:flex;align-items:center;justify-content:center;font-size:3.5rem;">{photo["emoji"]}</div><div style="padding:14px;"><div style="font-weight:700;font-size:0.95rem;color:{NOIR};">{photo["titre"]}</div><div style="font-size:0.78rem;color:{GRIS_TEXT};margin:4px 0;">📅 {photo["date"]} · 📍 {photo["antenne"]}</div><div style="font-size:0.82rem;color:{GRIS_TEXT};">{photo["description"]}</div></div></div><br>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="section-title" style="font-size:1rem;">📤 Ajouter des photos</span>', unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: titre_p=st.text_input("Titre de l'album")
    with c2: ant_p=st.selectbox("Antenne",antennes,key="ant_photo")
    with c3: date_p=st.date_input("Date",key="date_photo")
    photos_up=st.file_uploader("Photos",type=["jpg","jpeg","png"],accept_multiple_files=True)
    if st.button("📁 Créer l'album",type="primary"):
        if titre_p and photos_up: st.success(f"✅ Album « {titre_p} » créé avec {len(photos_up)} photo(s) !")
        else: st.warning("⚠️ Titre et photos obligatoires.")
