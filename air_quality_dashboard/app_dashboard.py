import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import time

# CONFIG
API_LATEST = "http://127.0.0.1:5000/latest"
API_HISTORY = "http://127.0.0.1:5000/history"

st.set_page_config(
    page_title="Air Quality Monitoring",
    page_icon="🌍",
    layout="wide"
)

# CSS
st.markdown("""
<style>

html, body, .block-container  {
    background: radial-gradient(circle at top, #0f172a, #020617);
    color: #e5e7eb;
    font-family: "Segoe UI", sans-serif;
}

h1 {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 10px;
    text-align: center;
}

h2, h3 {
    color: #38bdf8;
    font-weight: 600;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020617, #020617);
    padding: 20px;
}

section[data-testid="stSidebar"] h1 {
    color: #38bdf8;
    font-size: 22px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 25px;
}

section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span {
    color: #e5e7eb;
    font-size: 14px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 8px 12px;
    border-radius: 10px;
    margin-bottom: 6px;
    transition: background 0.2s ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] input:checked + div {
    background: rgba(56,189,248,0.15);
    font-weight: 600;
    border-radius: 10px;
}

section[data-testid="stSidebar"] input[type="checkbox"] {
    accent-color: #38bdf8;
}

.card-value {
    font-size: 42px;
    font-weight: 700;
    margin-top: 8px;
    color: #ffffff;
}

.ai-card {
    background: linear-gradient(160deg, #020617, #020617, #1f2937);
    padding: 45px;
    border-radius: 26px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 60px rgba(56,189,248,0.15);
    text-align: center;
}

.ai-result {
    font-size: 52px;
    font-weight: 800;
    letter-spacing: 2px;
}

.ai-desc {
    font-size: 16px;
    color: #cbd5f5;
    margin-top: 12px;
}

.system-status {
    margin-top: 18px;
    font-size: 15px;
    color: #9ca3af;
}

.good {
    color: #22c55e;
    text-shadow: 0 0 15px rgba(34,197,94,0.5);
}

.moderate {
    color: #eab308;
    text-shadow: 0 0 15px rgba(234,179,8,0.5);
}

.poor {
    color: #f97316;
    text-shadow: 0 0 15px rgba(249,115,22,0.5);
}

.dangerous {
    color: #ef4444;
    text-shadow: 0 0 18px rgba(239,68,68,0.7);
}

.block-container > div {
    margin-bottom: 30px;
}

[data-testid="stHorizontalBlock"] > div {
    background: linear-gradient(145deg, rgba(31,41,55,0.85), rgba(2,6,23,0.85));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    text-align: center;
}

[data-testid="metric-container"] {
    background: linear-gradient(145deg, #1f2937, #020617);
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}

[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.08);
}
        
[data-testid="stLineChart"] canvas,
[data-testid="stBarChart"] canvas  {
    background: rgba(2,6,23,0.6);
    border-radius: 14px;
    padding: 10px;
}

.stAlert {
    border-radius: 14px;
}

.footer {
    text-align: center;
    color: #6b7280;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# SIDEBAR
st.sidebar.title("Air Quality Monitoring")

page = st.sidebar.radio(
    "Navigation",
    ["📡 Temps Réel", "📈 Historique", "📊 Statistiques"],
    label_visibility="collapsed"

)

auto_refresh = st.sidebar.checkbox("Auto refresh (10s)")

# PAGE 1 : TEMPS RÉEL
if page == "📡 Temps Réel":

    st.title("Données en Temps Réel")

    r = requests.get(API_LATEST)
    if r.status_code == 200:
        data = r.json()
        quality = data["air_quality"]

        # CAPTEURS
        st.subheader("Mesures des capteurs")
        c1, c2, c3 = st.columns(3)

        c1.markdown(f"""
        <div class="card">
            <div class="card-title">Température (°C)</div>
            <div class="card-value">{data['temperature']}</div>
        </div>
        """, unsafe_allow_html=True)

        c2.markdown(f"""
        <div class="card">
            <div class="card-title">Humidité (%)</div>
            <div class="card-value">{data['humidity']}</div>
        </div>
        """, unsafe_allow_html=True)

        c3.markdown(f"""
        <div class="card">
            <div class="card-title">Gaz MQ-2</div>
            <div class="card-value">{data['mq2']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><br>", unsafe_allow_html=True)

        # PRÉDICTION IA
        st.subheader("Prédiction IA")

        if quality == "Good":
            css, desc, state = "good", "Air sain — aucune action requise", "🟢 Système stable"
        elif quality == "Moderate":
            css, desc, state = "moderate", "Qualité acceptable — surveillance recommandée", "🟡 Surveillance"
        elif quality == "Poor":
            css, desc, state = "poor", "Air pollué — limiter l'exposition", "🟠 Attention"
        else:
            css, desc, state = "dangerous", "Air dangereux — aération immédiate", "🔴 Situation critique"

        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-result {css}">{quality}</div>
            <div class="ai-desc">{desc}</div>
            <div class="system-status">État du système : <b>{state}</b></div>
        </div>
        """, unsafe_allow_html=True)

        st.caption(f" Dernière mise à jour : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# PAGE 2 : HISTORIQUE (AMÉLIORÉE)
elif page == "📈 Historique":

    st.title("Historique des Mesures")

    r = requests.get(API_HISTORY)
    if r.status_code == 200:
        df = pd.DataFrame(r.json())

        # Conversion sécurisée
        for col in ["temperature", "humidity", "mq2"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        if not df.empty:
            df["timestamp"] = pd.to_datetime(df["timestamp"])

            # FILTRES
            st.subheader("Filtres")

            col_f1, col_f2, col_f3 = st.columns(3)

            # Nombre de mesures
            with col_f1:
                n = st.slider(
                    "Nombre de mesures",
                    min_value=0,
                    max_value=len(df),
                    value=len(df)
                )

            # Qualité de l'air
            with col_f2:
                q = st.multiselect(
                    "Qualité de l'air",
                    ["Good", "Moderate", "Poor", "Dangerous"],
                    default=["Good", "Moderate", "Poor", "Dangerous"]
                )

            # ⏱FILTRE TIMESTAMP
            with col_f3:
                min_date = df["timestamp"].min().date()
                max_date = df["timestamp"].max().date()

                date_range = st.date_input(
                    "Période",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date
                )

            # APPLICATION DES FILTRES
            if len(date_range) == 2:
                start_date, end_date = date_range

                df = df[
                    (df["timestamp"].dt.date >= start_date) &
                    (df["timestamp"].dt.date <= end_date)
                ]

            df_f = df[df["air_quality"].isin(q)].tail(n)

            # TABLEAU
            st.subheader("Données filtrées")
            st.dataframe(df_f, use_container_width=True)

            # GRAPHIQUES
            st.subheader("Évolution des mesures")

            g1, g2, g3 = st.columns(3)

            with g1:
                st.markdown("**Température (°C)**")
                st.line_chart(df_f.set_index("timestamp")["temperature"])

            with g2:
                st.markdown("**Humidité (%)**")
                st.line_chart(df_f.set_index("timestamp")["humidity"])

            with g3:
                st.markdown("**Gaz MQ-2**")
                st.line_chart(df_f.set_index("timestamp")["mq2"])

            # ALERTE
            if (df_f["air_quality"] == "Dangerous").any():
                st.error("Attention : des niveaux dangereux ont été détectés")
            else:
                st.success("Aucun niveau dangereux détecté")

# PAGE 3 : STATISTIQUES
elif page == "📊 Statistiques":

    st.title("Analyse Statistique de la Qualité de l'Air")

    r = requests.get(API_HISTORY)
    if r.status_code == 200:
        df = pd.DataFrame(r.json())

        if not df.empty:
            # NETTOYAGE & CONVERSION
            for col in ["temperature", "humidity", "mq2"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")

            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.dropna()

            # KPI GLOBAUX
            st.subheader("Indicateurs Clés")

            dominant_quality = df["air_quality"].mode()[0]

            c1, c2, c3, c4= st.columns(4)

            c1.metric(
                "Température Moyenne",
                f"{df['temperature'].mean():.2f} °C"
            )

            c2.metric(
                "Humidité Moyenne",
                f"{df['humidity'].mean():.1f} %"
            )

            c3.metric(
                "MQ-2 Moyen",
                f"{df['mq2'].mean():.0f}"
            )

            c4.metric(
                "Total Mesures",
                len(df)
            )

            st.markdown("---")

            # EXTRÊMES & STABILITÉ
            st.subheader("Extrêmes & Stabilité des Capteurs")

            e1, e2, e3 = st.columns(3)

            e1.metric(
                "Température Min / Max",
                f"{df['temperature'].min():.1f} / {df['temperature'].max():.1f} °C"
            )

            e2.metric(
                "Humidité Min / Max",
                f"{df['humidity'].min():.1f} / {df['humidity'].max():.1f} %"
            )

            e3.metric(
                "MQ-2 Min / Max",
                f"{int(df['mq2'].min())} / {int(df['mq2'].max())}"
            )

            st.markdown("---")

            # RÉPARTITION QUALITÉ DE L’AIR
            st.subheader("Répartition de la Qualité de l’Air")

            # Calcul qualité dominante
            dominant_quality = df["air_quality"].mode()[0]

            col1, col2 = st.columns([2, 1])

            with col1:
                st.bar_chart(df["air_quality"].value_counts())

            with col2:
                st.metric(
                    "Qualité Dominante",
                    dominant_quality
                )

                st.markdown("---")

                total = len(df)
                counts = df["air_quality"].value_counts()

                for q in ["Good", "Moderate", "Poor", "Dangerous"]:
                    percent = (counts.get(q, 0) / total) * 100
                    st.metric(q, f"{percent:.1f} %")

            # ANALYSE DES ALERTES
            st.subheader("Analyse des Situations Dangereuses")

            dangerous_df = df[df["air_quality"] == "Dangerous"]

            d1, d2, d3 = st.columns(3)

            d1.metric(
                "Nombre d'alertes",
                len(dangerous_df)
            )

            d2.metric(
                "Première alerte",
                dangerous_df["timestamp"].min().strftime("%Y-%m-%d %H:%M:%S")
                if not dangerous_df.empty else "—"
            )

            d3.metric(
                "Dernière alerte",
                dangerous_df["timestamp"].max().strftime("%Y-%m-%d %H:%M:%S")
                if not dangerous_df.empty else "—"
            )

            st.markdown("---")

            # CONCLUSION AUTOMATIQUE
            danger_pct = (len(dangerous_df) / len(df)) * 100

            st.subheader("Conclusion Automatique")

            if danger_pct > 10:
                st.error(
                    f"La qualité de l'air est globalement **{dominant_quality}**, "
                    f"avec **{danger_pct:.1f} %** de situations dangereuses. "
                    "Une action corrective est recommandée."
                )
            else:
                st.success(
                    f"La qualité de l'air est globalement **{dominant_quality}**, "
                    f"avec seulement **{danger_pct:.1f} %** de situations dangereuses. "
                    "Le système fonctionne dans des conditions acceptables."
                )


# FOOTER
st.markdown("""
<div class="footer">
  Air Quality Monitoring — ESP32 + Machine Learning
</div>
""", unsafe_allow_html=True)

# AUTO REFRESH
if auto_refresh:
    time.sleep(10)
    st.rerun()
