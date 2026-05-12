import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import base64
from datetime import datetime

# ─── CONFIG ────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HOPE – CRM",
    page_icon="🐴",
    layout="wide",
    initial_sidebar_state="expanded"
)

ROSE       = "#E8186D"
ROSE_LIGHT = "#F5559A"
NOIR       = "#1A0A00"
GRIS_FOND  = "#F9F4F6"
BLANC      = "#FFFFFF"
GRIS_TEXT  = "#5C3D4A"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');
    .stApp {{ background-color: {GRIS_FOND}; font-family: 'DM Sans', sans-serif; }}
    [data-testid="stSidebar"] {{ background-color: {NOIR} !important; border-right: 3px solid {ROSE}; }}
    [data-testid="stSidebar"] * {{ color: {BLANC} !important; }}
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
    .rank-medal {{ font-size:1.1rem; min-width:22px; }}

    .data-table {{ width:100%; border-collapse:collapse; font-family:'DM Sans',sans-serif; font-size:0.88rem; }}
    .data-table th {{ background:{NOIR}; color:white; padding:10px 14px; text-align:left; font-weight:500; }}
    .data-table td {{ padding:10px 14px; border-bottom:1px solid #f0e8ec; }}
    .data-table tr:hover td {{ background:#fdf5f8; }}
    .badge-wa {{ background:#25D366; color:white; font-size:0.68rem; padding:2px 8px; border-radius:20px; margin-left:6px; }}
    .badge-inscrit {{ background:#d4edda; color:#155724; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-attente {{ background:#fff3cd; color:#856404; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-mecene {{ background:#e8d5f5; color:#5b2d8e; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-benevole {{ background:#d0eaff; color:#0a4a8c; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}
    .badge-beneficiaire {{ background:#fde8f0; color:#8c0a3c; font-size:0.72rem; padding:2px 8px; border-radius:20px; }}

    .action-card {{ background:{BLANC}; border-radius:14px; padding:20px 24px; box-shadow:0 1px 10px rgba(0,0,0,0.06); margin-bottom:16px; border-left:4px solid {ROSE_LIGHT}; }}
    .action-title {{ font-weight:700; font-size:0.95rem; color:{NOIR}; margin-bottom:10px; }}
    .wa-source {{ background:rgba(37,211,102,0.1); border:1px solid #25D366; border-radius:8px; padding:8px 14px; font-size:0.82rem; color:#1a8a45; margin-bottom:16px; display:flex; align-items:center; gap:8px; }}
    .sidebar-sep {{ border:none; border-top:1px solid rgba(255,255,255,0.15); margin:14px 0; }}
    .newsletter-zone {{ background: linear-gradient(135deg, #fff5f9 0%, #fff 100%); border: 2px dashed {ROSE_LIGHT}; border-radius: 14px; padding: 28px 24px; text-align: center; margin-bottom: 16px; }}
    .newsletter-icon {{ font-size: 2.5rem; margin-bottom: 8px; }}
    .stat-row {{ display:flex; gap:12px; margin-bottom:20px; }}
    .stat-chip {{ background:{BLANC}; border-radius:10px; padding:12px 18px; flex:1; text-align:center; box-shadow:0 1px 8px rgba(232,24,109,0.07); border-top:3px solid {ROSE}; }}
    .stat-chip-num {{ font-family:'Playfair Display',serif; font-size:1.6rem; font-weight:900; color:{ROSE}; }}
    .stat-chip-label {{ font-size:0.75rem; color:{GRIS_TEXT}; text-transform:uppercase; letter-spacing:0.06em; }}
</style>
""", unsafe_allow_html=True)


# ─── LOGO ──────────────────────────────────────────────────────────────────────
def get_logo_b64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

LOGO_PATH = r"C:\Users\bmond\Downloads\hope_logo.jpg"
logo_b64  = get_logo_b64(LOGO_PATH)


# ─── DONNÉES ───────────────────────────────────────────────────────────────────
centres = {
    "Île-de-France":            ["Centre Équestre de Versailles", "Poney Club de Vincennes", "Écuries du Bois de Boulogne"],
    "Provence-Alpes-Côte d'Azur": ["Centre Équestre d'Aix-en-Provence", "Haras de Marseille"],
    "Nouvelle-Aquitaine":       ["Centre Équestre de Bordeaux", "Poney Club de Bayonne"],
    "Occitanie":                ["Écuries de Montpellier", "Centre Équestre de Toulouse"],
    "Bretagne":                 ["Centre Équestre de Rennes", "Haras de Brest"],
}

beneficiaires_data = [
    {"Prénom":"Emma",  "Nom":"Laurent",  "Téléphone":"06 12 34 56 78","Séjour":"Été 2025",      "Centre":"Centre Équestre de Versailles",    "Mail":"emma.l@mail.com",  "Source":"WhatsApp"},
    {"Prénom":"Noah",  "Nom":"Bernard",  "Téléphone":"06 23 45 67 89","Séjour":"Printemps 2025","Centre":"Poney Club de Vincennes",           "Mail":"",                 "Source":"WhatsApp"},
    {"Prénom":"Chloé", "Nom":"Martin",   "Téléphone":"06 34 56 78 90","Séjour":"Été 2025",      "Centre":"Centre Équestre d'Aix-en-Provence", "Mail":"chloe.m@mail.com", "Source":"WhatsApp"},
    {"Prénom":"Hugo",  "Nom":"Dupont",   "Téléphone":"06 45 67 89 01","Séjour":"Hiver 2025",    "Centre":"Centre Équestre de Versailles",    "Mail":"",                 "Source":"WhatsApp"},
    {"Prénom":"Léa",   "Nom":"Rousseau", "Téléphone":"06 56 78 90 12","Séjour":"Été 2025",      "Centre":"Écuries du Bois de Boulogne",      "Mail":"lea.r@mail.com",   "Source":"WhatsApp"},
    {"Prénom":"Tom",   "Nom":"Petit",    "Téléphone":"06 67 89 01 23","Séjour":"Printemps 2025","Centre":"Haras de Marseille",                "Mail":"tom.p@mail.com",   "Source":"WhatsApp"},
]

benevoles_data = [
    {"Prénom":"Marie",  "Nom":"Dupont",  "Téléphone":"06 11 22 33 44","Mail":"marie.d@mail.com",  "Centre":"Centre Équestre de Versailles","Statut":"Actif"},
    {"Prénom":"Thomas", "Nom":"Martin",  "Téléphone":"06 22 33 44 55","Mail":"thomas.m@mail.com", "Centre":"Poney Club de Vincennes",      "Statut":"Relance"},
    {"Prénom":"Claire", "Nom":"Bernard", "Téléphone":"06 33 44 55 66","Mail":"claire.b@mail.com", "Centre":"Centre Équestre de Versailles","Statut":"Actif"},
    {"Prénom":"Lucas",  "Nom":"Petit",   "Téléphone":"06 44 55 66 77","Mail":"lucas.p@mail.com",  "Centre":"Haras de Marseille",           "Statut":"Inactif"},
    {"Prénom":"Sophie", "Nom":"Roux",    "Téléphone":"06 55 66 77 88","Mail":"sophie.r@mail.com", "Centre":"Écuries du Bois de Boulogne",  "Statut":"Actif"},
]

mecenes_data = [
    {"Prénom":"Jean",     "Nom":"Moreau",   "Société":"Moreau & Associés", "Mail":"j.moreau@moreau.fr",    "Don (€)":5000, "Reçu envoyé":"Oui"},
    {"Prénom":"Isabelle", "Nom":"Fontaine", "Société":"Groupe Fontaine",   "Mail":"i.fontaine@gf.com",     "Don (€)":2500, "Reçu envoyé":"Non"},
    {"Prénom":"Pierre",   "Nom":"Gauthier", "Société":"Gauthier Conseil",  "Mail":"p.gauthier@conseil.fr", "Don (€)":8000, "Reçu envoyé":"Oui"},
    {"Prénom":"Nathalie", "Nom":"Lemoine",  "Société":"NL Équipements",    "Mail":"n.lemoine@nl.fr",       "Don (€)":1500, "Reçu envoyé":"Non"},
    {"Prénom":"François", "Nom":"Mercier",  "Société":"Mercier Industries", "Mail":"f.mercier@mi.fr",      "Don (€)":12000,"Reçu envoyé":"Oui"},
]

classement = [
    {"rang":"🥇","nom":"Annabel","role":"Présidente",  "init":"AN","heures":20,"bg":"#F4C0D1","txt":"#993556"},
    {"rang":"🥈","nom":"Céline",   "role":"Directrice",      "init":"GI","heures":15,"bg":"#9FE1CB","txt":"#0F6E56"},
    {"rang":"🥉","nom":"Sandrine", "role":"Secrétariat",  "init":"SA","heures":12,"bg":"#B5D4F4","txt":"#185FA5"},
    {"rang":"4️⃣","nom":"Emeline",  "role":"Événementiel", "init":"EM","heures":10,"bg":"#FAC775","txt":"#854F0B"},
]

# ── Consolidation de tous les contacts avec mail ──
tous_contacts = []
for r in beneficiaires_data:
    if r["Mail"]:
        tous_contacts.append({"Prénom":r["Prénom"],"Nom":r["Nom"],"Mail":r["Mail"],"Type":"Bénéficiaire"})
for r in benevoles_data:
    if r["Mail"]:
        tous_contacts.append({"Prénom":r["Prénom"],"Nom":r["Nom"],"Mail":r["Mail"],"Type":"Bénévole"})
for r in mecenes_data:
    tous_contacts.append({"Prénom":r["Prénom"],"Nom":r["Nom"],"Mail":r["Mail"],"Type":"Mécène"})


# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if logo_b64:
        st.markdown(f'<div style="text-align:center;padding:16px 0 8px;"><img src="data:image/jpeg;base64,{logo_b64}" style="width:110px;border-radius:10px;" /></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:16px 0;font-size:1.8rem;color:{ROSE};">🐴 HOPE</div>', unsafe_allow_html=True)

    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)

    page = st.radio("", [
        "🏠  Accueil",
        "🧒  Bénéficiaires",
        "👥  Bénévoles",
        "💼  Mécènes",
        "📰  Newsletter",
    ], label_visibility="collapsed")

    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)

    st.markdown("<p style='font-size:0.7rem;opacity:0.45;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;'>Classement connexions</p>", unsafe_allow_html=True)
    max_h = max(p["heures"] for p in classement)
    for p in classement:
        pct = int(p["heures"] / max_h * 100)
        st.markdown(f"""
        <div class="rank-item">
            <div class="rank-medal">{p['rang']}</div>
            <div class="rank-avatar" style="background:{p['bg']};color:{p['txt']};">{p['init']}</div>
            <div style="flex:1;">
                <div style="font-size:0.85rem;font-weight:600;color:{BLANC};">{p['nom']}</div>
                <div style="background:rgba(255,255,255,0.15);border-radius:4px;height:4px;margin-top:4px;overflow:hidden;">
                    <div style="width:{pct}%;height:4px;background:{ROSE};border-radius:4px;"></div>
                </div>
            </div>
            <div style="font-size:0.75rem;opacity:0.65;color:{BLANC};">{p['heures']}h</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<hr class='sidebar-sep'>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.75rem;opacity:0.45;'>Connecté : <strong>Annabelle</strong></p>", unsafe_allow_html=True)


# ─── HEADER ────────────────────────────────────────────────────────────────────
logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="height:56px;border-radius:10px;" />' if logo_b64 else "🐴"
st.markdown(f"""
<div class="header-band">
    {logo_html}
    <div>
        <div class="header-title">Tableau de bord HOPE</div>
        <div class="header-sub">CRM · WhatsApp IA · Relances automatiques — {datetime.now().strftime("%d %B %Y")}</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : ACCUEIL
# ═══════════════════════════════════════════════════════════════════════════════
if "Accueil" in page:
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        (col1, str(len(benevoles_data)),    "Bénévoles actifs"),
        (col2, str(len(beneficiaires_data)),"Bénéficiaires"),
        (col3, str(len(mecenes_data)),      "Mécènes"),
        (col4, str(len(tous_contacts)),     "Contacts avec mail"),
    ]
    for col, num, label in kpis:
        with col:
            st.markdown(f'<div class="kpi-card"><div class="kpi-number">{num}</div><div class="kpi-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<span class="section-title">Activité WhatsApp – 30 jours</span>', unsafe_allow_html=True)
        mois = ["Jan","Fév","Mar","Avr","Mai","Jun"]
        msgs = [42, 58, 75, 61, 89, 94]
        fig = go.Figure(go.Bar(x=mois, y=msgs, marker_color=ROSE, opacity=0.85, text=msgs, textposition="outside"))
        fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(family="DM Sans"),
                          yaxis=dict(gridcolor="#f0e8ec", range=[0,110]),
                          margin=dict(t=20,b=10,l=10,r=10), height=260, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<span class="section-title">Résumés IA WhatsApp</span>', unsafe_allow_html=True)
        resumes = [
            ("Groupe Séjour Été 2025","Aujourd'hui 09h14","Confirmation hébergements ok. Transport du 14/07 en attente — 3 familles concernées."),
            ("Groupe Bénévoles",      "Hier 17h32",        "Thomas indisponible le 21. Marie propose de remplacer. 2 accompagnateurs manquants."),
            ("Groupe Familles HOPE",  "Hier 11h05",        "Plusieurs parents demandent le programme printemps. Régime spécifique pour Chloé M."),
        ]
        for groupe, date, resume in resumes:
            st.markdown(f"""
            <div style="background:linear-gradient(135deg,{NOIR} 0%,#3D1A2A 100%);border-radius:12px;padding:14px 18px;color:white;margin-bottom:10px;border-left:4px solid {ROSE};">
                <span style="background:{ROSE};color:white;font-size:0.68rem;padding:2px 8px;border-radius:20px;margin-bottom:6px;display:inline-block;">✨ IA WhatsApp</span>
                <div style="font-weight:600;font-size:0.9rem;margin-bottom:4px;">{groupe}</div>
                <div style="font-size:0.82rem;opacity:0.85;line-height:1.5;">{resume}</div>
                <div style="font-size:0.72rem;opacity:0.5;margin-top:6px;">📅 {date}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : BÉNÉFICIAIRES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Bénéficiaires" in page:
    st.markdown('<span class="section-title">🧒 Gestion des bénéficiaires</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="wa-source"><span style="font-size:1.1rem;">💬</span><span>Données récupérées automatiquement via l\'<strong>API WhatsApp</strong> — aucune saisie manuelle requise</span></div>', unsafe_allow_html=True)

    col_r, col_c = st.columns(2)
    with col_r:
        region = st.selectbox("📍 Région", ["Toutes les régions"] + list(centres.keys()))
    with col_c:
        if region == "Toutes les régions":
            tous_centres = [c for liste in centres.values() for c in liste]
            centre_sel = st.selectbox("🏇 Centre équestre", ["Tous les centres"] + tous_centres)
        else:
            centre_sel = st.selectbox("🏇 Centre équestre", ["Tous les centres"] + centres[region])

    st.markdown("<br>", unsafe_allow_html=True)
    df_ben = pd.DataFrame(beneficiaires_data)
    if centre_sel != "Tous les centres":
        df_ben = df_ben[df_ben["Centre"] == centre_sel]

    st.markdown('<span class="section-title" style="font-size:1rem;">Liste des bénéficiaires</span>', unsafe_allow_html=True)
    html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Téléphone</th><th>Séjour</th><th>Centre</th><th>Mail</th><th>Source</th></tr>'
    for _, row in df_ben.iterrows():
        mail_cell = row['Mail'] if row['Mail'] else f'<span style="color:{ROSE};font-size:0.8rem;cursor:pointer;">+ Ajouter</span>'
        html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td>{row["Téléphone"]}</td><td><span class="badge-inscrit">{row["Séjour"]}</span></td><td style="font-size:0.8rem;color:{GRIS_TEXT};">{row["Centre"]}</td><td>{mail_cell}</td><td><span class="badge-wa">📱 WhatsApp</span></td></tr>'
    html += "</table>"
    st.markdown(html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="action-card">
        <div class="action-title">📧 Proposition de bénévolat</div>
        <p style="font-size:0.85rem;color:{GRIS_TEXT};margin-bottom:0;">Envoyer automatiquement un mail à des bénéficiaires pour leur proposer de devenir bénévole.</p>
    </div>
    """, unsafe_allow_html=True)
    dest = st.multiselect("Sélectionner les destinataires",
        [f"{r['Prénom']} {r['Nom']}" for _, r in df_ben.iterrows() if r['Mail']],
        default=[f"{r['Prénom']} {r['Nom']}" for _, r in df_ben.iterrows() if r['Mail']])
    if st.button("📤 Envoyer la proposition de bénévolat", type="primary"):
        st.success(f"✅ Mail envoyé à {len(dest)} bénéficiaire(s) !")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : BÉNÉVOLES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Bénévoles" in page:
    st.markdown('<span class="section-title">👥 Gestion des bénévoles</span>', unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📋 Liste", "➕ Ajouter", "📧 Invitation séjour"])

    with tab1:
        df_benv = pd.DataFrame(benevoles_data)
        html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Téléphone</th><th>Mail</th><th>Centre</th><th>Statut</th></tr>'
        for _, row in df_benv.iterrows():
            if row['Statut'] == "Actif":   badge = '<span class="badge-inscrit">Actif</span>'
            elif row['Statut'] == "Relance": badge = '<span class="badge-attente">Relance</span>'
            else: badge = '<span style="background:#f8d7da;color:#721c24;font-size:0.72rem;padding:2px 8px;border-radius:20px;">Inactif</span>'
            html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td>{row["Téléphone"]}</td><td style="font-size:0.82rem;">{row["Mail"] or "—"}</td><td style="font-size:0.8rem;color:{GRIS_TEXT};">{row["Centre"]}</td><td>{badge}</td></tr>'
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

    with tab2:
        mode = st.radio("Mode d'ajout", ["Saisie manuelle", "Convertir un bénéficiaire"], horizontal=True)
        if mode == "Saisie manuelle":
            c1, c2 = st.columns(2)
            with c1:
                prenom_benv = st.text_input("Prénom")
                tel_benv    = st.text_input("Téléphone")
                region_benv = st.selectbox("Région", list(centres.keys()), key="reg_benv")
            with c2:
                nom_benv    = st.text_input("Nom")
                mail_benv   = st.text_input("Mail")
                centre_benv = st.selectbox("Centre", centres[region_benv], key="ctr_benv")
            if st.button("✅ Ajouter le bénévole", type="primary"):
                st.success(f"Bénévole {prenom_benv} {nom_benv} ajouté au centre {centre_benv} !")
        else:
            df_conv = pd.DataFrame(beneficiaires_data)
            choix = st.selectbox("Choisir un bénéficiaire",
                [f"{r['Prénom']} {r['Nom']} – {r['Centre']}" for _, r in df_conv.iterrows()])
            st.info("Le bénéficiaire sera converti avec ses informations WhatsApp existantes.")
            if st.button("🔄 Convertir en bénévole", type="primary"):
                st.success(f"✅ {choix.split('–')[0].strip()} est maintenant bénévole !")

    with tab3:
        st.markdown(f'<div class="action-card"><div class="action-title">📧 Inviter des bénévoles à participer à un séjour ou une journée découverte</div></div>', unsafe_allow_html=True)
        df_benv2 = pd.DataFrame(benevoles_data)
        benv_avec_mail = [f"{r['Prénom']} {r['Nom']}" for _, r in df_benv2.iterrows() if r['Mail']]
        type_event  = st.radio("Type d'événement", ["Séjour", "Journée découverte"], horizontal=True)
        date_event  = st.date_input("Date de l'événement")
        selec_benv  = st.multiselect("Sélectionner les bénévoles", benv_avec_mail, default=benv_avec_mail)
        if st.button(f"📤 Envoyer l'invitation ({type_event})", type="primary"):
            st.success(f"✅ Invitation pour le {type_event} du {date_event.strftime('%d/%m/%Y')} envoyée à {len(selec_benv)} bénévole(s) !")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : MÉCÈNES
# ═══════════════════════════════════════════════════════════════════════════════
elif "Mécènes" in page:
    st.markdown('<span class="section-title">💼 Gestion des mécènes</span>', unsafe_allow_html=True)
    tab_m1, tab_m2, tab_m3, tab_m4 = st.tabs(["📋 Liste", "🎉 Invitation événement", "🧾 Reçu fiscal", "➕ Ajouter un mécène"])

    df_mec = pd.DataFrame(mecenes_data)

    with tab_m1:
        html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Société</th><th>Mail</th><th>Don (€)</th><th>Reçu fiscal</th></tr>'
        for _, row in df_mec.iterrows():
            recu = '<span class="badge-inscrit">Envoyé</span>' if row['Reçu envoyé'] == "Oui" else '<span class="badge-attente">En attente</span>'
            html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td style="font-size:0.82rem;color:{GRIS_TEXT};">{row["Société"]}</td><td style="font-size:0.82rem;">{row["Mail"]}</td><td style="font-weight:700;color:{ROSE};">{row["Don (€)"]:,} €</td><td>{recu}</td></tr>'
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
        total = sum(r['Don (€)'] for r in mecenes_data)
        st.markdown(f'<div style="text-align:right;margin-top:12px;font-family:Playfair Display,serif;font-size:1.1rem;color:{NOIR};">Total des dons : <strong style="color:{ROSE};">{total:,} €</strong></div>', unsafe_allow_html=True)

    with tab_m2:
        st.markdown(f'<div class="action-card"><div class="action-title">🎉 Inviter des mécènes à un événement</div></div>', unsafe_allow_html=True)
        mec_liste  = [f"{r['Prénom']} {r['Nom']} – {r['Société']}" for _, r in df_mec.iterrows()]
        selec_mec  = st.multiselect("Sélectionner les mécènes", mec_liste, default=mec_liste)
        nom_event  = st.text_input("Nom de l'événement", placeholder="ex : Gala annuel HOPE 2025")
        date_mec   = st.date_input("Date de l'événement", key="date_mec")
        lieu_mec   = st.text_input("Lieu", placeholder="ex : Château de Versailles")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="action-card">
            <div class="action-title">📎 Joindre un document à l'invitation (optionnel)</div>
            <p style="font-size:0.83rem;color:{GRIS_TEXT};margin-bottom:0;">Programme de l'événement, carton d'invitation, plan d'accès…</p>
        </div>
        """, unsafe_allow_html=True)
        fichier_invitation = st.file_uploader("Déposer un fichier à joindre", type=["pdf","png","jpg","docx"], key="inv_mec")

        if st.button("📤 Envoyer les invitations", type="primary"):
            extra = f" avec le fichier « {fichier_invitation.name} »" if fichier_invitation else ""
            st.success(f"✅ Invitation pour « {nom_event} »{extra} envoyée à {len(selec_mec)} mécène(s) !")

    with tab_m3:
        st.markdown(f'<div class="action-card"><div class="action-title">🧾 Envoi du reçu fiscal & message de remerciement</div></div>', unsafe_allow_html=True)
        mec_recu = st.selectbox("Sélectionner le mécène",
            [f"{r['Prénom']} {r['Nom']} – {r['Société']} ({r['Don (€)']:,} €)" for _, r in df_mec.iterrows()])
        msg = st.text_area("Message de remerciement",
            value="Madame, Monsieur,\n\nNous vous remercions chaleureusement pour votre généreux soutien à l'association HOPE. Votre don nous permet de continuer à offrir des expériences uniques à nos bénéficiaires.\n\nVeuillez trouver ci-joint votre reçu fiscal.\n\nL'équipe HOPE",
            height=150)
        recu_file = st.file_uploader("Déposer le reçu fiscal (PDF)", type=["pdf"])
        if st.button("📨 Envoyer le reçu fiscal + message", type="primary"):
            if recu_file:
                st.success(f"✅ Reçu « {recu_file.name} » et message envoyés à {mec_recu.split('–')[0].strip()} !")
                st.balloons()
            else:
                st.warning("⚠️ Veuillez déposer le reçu fiscal avant d'envoyer.")
    
    with tab_m4:
        st.markdown(f'<div class="action-card"><div class="action-title">➕ Ajouter un mécène manuellement</div></div>', unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            prenom_mec = st.text_input("Prénom", key="prenom_mec")
            societe_mec = st.text_input("Société / Organisation", key="societe_mec")
            siren_mec = st.text_input("SIREN", key="siren_mec")
            don_mec = st.number_input("Montant du don (€)", min_value=0, step=100, key="don_mec")
        with c2:
            nom_mec_new = st.text_input("Nom", key="nom_mec_new")
            mail_mec = st.text_input("Mail", key="mail_mec")
            recu_mec = st.selectbox("Reçu fiscal envoyé ?", ["Non", "Oui"], key="recu_mec")

        note_mec = st.text_area("Notes (optionnel)", placeholder="Ex : intéressé par le gala, contact via Annabelle…", key="note_mec", height=100)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Ajouter le mécène", type="primary", key="btn_add_mec"):
            if prenom_mec and nom_mec_new and mail_mec:
                st.success(f"✅ Mécène {prenom_mec} {nom_mec_new} ({societe_mec}) ajouté avec un don de {don_mec:,} € !")
            else:
                st.warning("⚠️ Veuillez renseigner au minimum le prénom, le nom et le mail.")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE : NEWSLETTER
# ═══════════════════════════════════════════════════════════════════════════════
elif "Newsletter" in page:
    st.markdown('<span class="section-title">📰 Envoi de la newsletter</span>', unsafe_allow_html=True)

    # Stats contacts
    nb_ben   = sum(1 for r in beneficiaires_data if r["Mail"])
    nb_benv  = sum(1 for r in benevoles_data if r["Mail"])
    nb_mec   = len(mecenes_data)
    nb_total = nb_ben + nb_benv + nb_mec

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-chip"><div class="stat-chip-num">{nb_total}</div><div class="stat-chip-label">Total destinataires</div></div>
        <div class="stat-chip" style="border-top-color:#8c0a3c;"><div class="stat-chip-num" style="color:#8c0a3c;">{nb_ben}</div><div class="stat-chip-label">Bénéficiaires</div></div>
        <div class="stat-chip" style="border-top-color:#0a4a8c;"><div class="stat-chip-num" style="color:#0a4a8c;">{nb_benv}</div><div class="stat-chip-label">Bénévoles</div></div>
        <div class="stat-chip" style="border-top-color:#5b2d8e;"><div class="stat-chip-num" style="color:#5b2d8e;">{nb_mec}</div><div class="stat-chip-label">Mécènes</div></div>
    </div>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Sélection des destinataires
        st.markdown('<span class="section-title" style="font-size:1rem;">Sélection des destinataires</span>', unsafe_allow_html=True)

        df_contacts = pd.DataFrame(tous_contacts)

        filtre_type = st.multiselect("Filtrer par type",
            ["Bénéficiaire", "Bénévole", "Mécène"],
            default=["Bénéficiaire", "Bénévole", "Mécène"])

        df_filtre = df_contacts[df_contacts["Type"].isin(filtre_type)]

        html = f'<table class="data-table"><tr><th>Prénom</th><th>Nom</th><th>Mail</th><th>Type</th></tr>'
        for _, row in df_filtre.iterrows():
            if row["Type"] == "Bénéficiaire": badge = '<span class="badge-beneficiaire">Bénéficiaire</span>'
            elif row["Type"] == "Bénévole":   badge = '<span class="badge-benevole">Bénévole</span>'
            else:                             badge = '<span class="badge-mecene">Mécène</span>'
            html += f'<tr><td>{row["Prénom"]}</td><td>{row["Nom"]}</td><td style="font-size:0.82rem;">{row["Mail"]}</td><td>{badge}</td></tr>'
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)

    with col_right:
        st.markdown('<span class="section-title" style="font-size:1rem;">Envoi</span>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="newsletter-zone">
            <div class="newsletter-icon">📄</div>
            <div style="font-weight:600;font-size:0.9rem;color:{NOIR};margin-bottom:4px;">Déposer la newsletter</div>
            <div style="font-size:0.8rem;color:{GRIS_TEXT};">PDF, image ou document Word</div>
        </div>
        """, unsafe_allow_html=True)

        newsletter_file = st.file_uploader("", type=["pdf","png","jpg","jpeg","docx"], label_visibility="collapsed")

        objet_mail = st.text_input("Objet du mail", placeholder="ex : Newsletter HOPE – Juin 2025")

        msg_news = st.text_area("Message d'accompagnement",
            value="Bonjour,\n\nVeuillez trouver ci-joint la newsletter de l'association HOPE.\n\nBonne lecture !\n\nL'équipe HOPE",
            height=130)

        st.markdown("<br>", unsafe_allow_html=True)

        nb_dest = len(df_filtre)
        if st.button(f"📤 Envoyer à {nb_dest} destinataire(s)", type="primary", use_container_width=True):
            if newsletter_file and objet_mail:
                st.success(f"✅ Newsletter « {newsletter_file.name} » envoyée à {nb_dest} destinataire(s) !")
                st.balloons()
            elif not newsletter_file:
                st.warning("⚠️ Veuillez déposer le fichier de la newsletter.")
            else:
                st.warning("⚠️ Veuillez renseigner l'objet du mail.")