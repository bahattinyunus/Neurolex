import streamlit as st
import pandas as pd
import requests
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(
    page_title="Neurolex Dashboard",
    page_icon="🧠",
    layout="wide"
)

API_URL = "http://localhost:8000/api/v1"

st.title("🧠 Neurolex: Akıllı Stres & Erteleme Yönetim Sistemi")

# Tabs
tab1, tab2, tab3 = st.tabs(["⌚ Canlı Akıllı Saat", "📋 Öz-Değerlendirme (Anket)", "🧬 Biyolojik Analiz"])

# --- TAB 1: LIVE WATCH SIMULATION ---
with tab1:
    st.header("Gerçek Zamanlı Akıllı Saat İzleme")
    
    # Sidebar for User Profile
    st.sidebar.header("Kullanıcı Profili")
    user_id = st.sidebar.text_input("Öğrenci ID", "student_01")
    st.sidebar.markdown("---")
    st.sidebar.info("Bu sekme, simülasyon scriptinden gelen canlı verileri gösterir.")

    # Layout placeholders
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    chart_placeholder = st.empty()
    alert_placeholder = st.empty()

    if st.button("Verileri Yenile"):
        pass

    try:
        response = requests.get(f"{API_URL}/history?limit=50")
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
        else:
            df = pd.DataFrame()
    except:
        df = pd.DataFrame()

    if not df.empty:
        # Latest values
        latest = df.iloc[-1]
        
        # Risk Logic (Duplicate logic for visualization color)
        risk_score = 0
        if latest['cortisol_level'] > 20: risk_score += 0.4
        if latest['hrv'] < 30: risk_score += 0.3
        
        # KPIs
        kpi1.metric("Kortizol (µg/dL)", f"{latest['cortisol_level']}", delta_color="inverse")
        kpi2.metric("HRV (ms)", f"{latest['hrv']}")
        kpi3.metric("EDA (µS)", f"{latest['eda']}")
        kpi4.metric("Ekran Süresi (dk)", f"{latest['screen_time_minutes']}")
        
        # Alerts
        watch_status = "Focused"
        watch_color = "green"

        if risk_score >= 0.7:
             alert_placeholder.error("🚨 YÜKSEK ERTELEME RİSKİ! Sosyal Medya Kilidi Aktif Edildi. Nefes Egzersizi Başlatılıyor...")
             watch_status = "⚠️ STRESS!"
             watch_color = "red"
        elif risk_score >= 0.4:
             alert_placeholder.warning("⚠️ Stres Seviyesi Yükseliyor. Lütfen kısa bir mola verin.")
             watch_status = "Relax..."
             watch_color = "orange"
        else:
             alert_placeholder.success("✅ Durum Normal. Odaklanma seviyesi ideal.")

        # Charts and Watch UI
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            st.subheader("Kortizol Seviyesi")
            fig_cortisol = px.line(df, x="timestamp", y="cortisol_level", height=300)
            st.plotly_chart(fig_cortisol, use_container_width=True)
            
        with col2:
            st.subheader("Kalp Değişkenliği (HRV)")
            fig_hrv = px.line(df, x="timestamp", y="hrv", height=300)
            st.plotly_chart(fig_hrv, use_container_width=True)
            
        with col3:
            st.subheader("⌚ Akıllı Saat")
            # CSS Hack for Watch UI
            st.markdown(f"""
            <div style="
                width: 200px;
                height: 200px;
                border-radius: 50%;
                background-color: #222;
                border: 8px solid #444;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
                margin: auto;
            ">
                <div style="color: {watch_color}; font-size: 24px; font-weight: bold;">{watch_status}</div>
                <div style="color: white; font-size: 14px; margin-top: 10px;">HR: {int(100 - latest['hrv']/2)} bpm</div>
                <div style="color: #aaa; font-size: 10px; margin-top: 5px;">Neurolex AI</div>
            </div>
            """, unsafe_allow_html=True)
            
            if risk_score >= 0.7:
                 st.markdown("**📳 TİTREŞİM AKTİF**")

# --- TAB 2: SURVEY ASSESSMENT ---
with tab2:
    st.header("📋 Yaşam Tarzı ve Stres Anketi")
    st.info("Yapay zeka modelimiz, yaşam tarzı faktörlerinize göre stres seviyenizi tahmin eder (Low, Medium, High).")

    with st.form("survey_form"):
        col1, col2 = st.columns(2)
        with col1:
            anxiety = st.slider("Kaygı Seviyesi (1-20)", 0, 21, 10)
            mental_history = st.selectbox("Mental Sağlık Geçmişi Var mı?", [0, 1])
            depression = st.slider("Depresyon Hissi (0-27)", 0, 27, 5)
            headache = st.selectbox("Baş Ağrısı Sıklığı (0-5)", range(6))
            sleep = st.slider("Uyku Kalitesi (0-5)", 0, 5, 3)
        with col2:
            breathing = st.selectbox("Nefes Alma Problemi (0-5)", range(6))
            living = st.slider("Yaşam Koşulları (0-5)", 0, 5, 3)
            academic = st.slider("Akademik Başarı (0-5)", 0, 5, 3)
            load = st.slider("Ders Yükü (0-5)", 0, 5, 3)
            career = st.slider("Gelecek Kaygısı (0-5)", 0, 5, 3)
            activites = st.slider("Sosyal Aktivite (0-5)", 0, 5, 3)
            
        submitted = st.form_submit_button("Stres Seviyemi Analiz Et")
        
        if submitted:
            payload = {
                "anxiety_level": anxiety,
                "mental_health_history": mental_history,
                "depression": depression,
                "headache": headache,
                "sleep_quality": sleep,
                "breathing_problem": breathing,
                "living_conditions": living,
                "academic_performance": academic,
                "study_load": load,
                "future_career_concerns": career,
                "extracurricular_activities": activites
            }
            try:
                res = requests.post(f"{API_URL}/predict/survey", json=payload)
                if res.status_code == 200:
                    result = res.json()["stress_level"]
                    st.success(f"Tahmini Stres Seviyeniz: **{result}**")
                else:
                    st.error("API Hatası")
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")

# --- TAB 3: BIO-SIGNAL ANALYSIS ---
with tab3:
    st.header("🧬 Biyolojik Veri Analizi")
    st.info("Vücut sensörlerinden gelen anlık verilerle (Nabız, EDA, Sıcaklık) fizyolojik stres analizi.")

    with st.form("bio_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            hr_val = st.number_input("Kalp Atış Hızı (BPM)", 40, 200, 75)
        with col2:
            eda_val = st.number_input("EDA (Elektrodermal Aktivite) µS", 0.0, 20.0, 2.5)
        with col3:
            temp_val = st.number_input("Vücut Sıcaklığı (°C)", 35.0, 42.0, 36.6)
            
        bio_submitted = st.form_submit_button("Analiz Et")
        
        if bio_submitted:
            payload = {
                "hr": hr_val,
                "eda": eda_val,
                "temp": temp_val
            }
            try:
                res = requests.post(f"{API_URL}/predict/biological", json=payload)
                if res.status_code == 200:
                    data = res.json()
                    st.metric("Risk Skoru", f"{data['risk_score']}/10")
                    st.metric("Stres Sınıfı", f"{data['risk_label']}")
                    
                    if data['risk_label'] == "High":
                        st.error("Yüksek Fizyolojik Stres Algılandı!")
                    elif data['risk_label'] == "Medium":
                        st.warning("Orta Seviye Stres.")
                    else:
                        st.success("Düşük Stres / Normal.")
                else:
                    st.error("API Hatası")
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")
