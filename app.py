
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import plotly.express as px
import plotly.graph_objects as go
from scipy.sparse import hstack, csr_matrix

st.set_page_config(
    page_title="ReviewLens",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.metric-card {
    background: #1A1D27;
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 12px;
}
.metric-card .label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #6B7280;
    margin-bottom: 6px;
}
.metric-card .value {
    font-size: 28px;
    font-weight: 700;
    color: #F9FAFB;
}
.result-box {
    background: #1A1D27;
    border: 1px solid #2A2D3E;
    border-radius: 12px;
    padding: 20px 24px;
    margin: 12px 0;
}
.result-box.problem { border-left: 4px solid #EF4444; }
.result-box.ok      { border-left: 4px solid #10B981; }
.summary-text {
    font-size: 15px;
    line-height: 1.7;
    color: #D1D5DB;
    background: #13151F;
    border-radius: 8px;
    padding: 16px 18px;
}
.divider { height: 1px; background: #2A2D3E; margin: 24px 0; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def nlp_yukle():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    try:
        from transformers import pipeline as hf_pipeline
        classifier = hf_pipeline(
            "zero-shot-classification",
            model="typeform/distilbart-mnli-12-3",
            device=-1,
        )
        zero_shot_ok = True
    except Exception:
        classifier   = None
        zero_shot_ok = False
    return analyzer, classifier, zero_shot_ok

KURALLAR = {
    "Teknik Destek": [
        "broken","defect","malfunction","not working","stopped working",
        "hardware","damage","cracked","dead","faulty","repair","doesnt work",
    ],
    "Yazilim Ekibi": [
        "software","app","crash","bug","update","glitch","freeze","error",
        "install","compatible","firmware","driver","bluetooth","wifi","sync",
    ],
    "Lojistik": [
        "shipping","delivery","package","arrived","late","damaged box",
        "missing","lost","never received","wrong item","return","tracking",
    ],
    "Musteri Hizmetleri": [
        "customer service","support","refund","warranty","response",
        "replied","contact","ignored","rude","representative","exchange",
    ],
    "Urun Yonetimi": [
        "design","quality","cheap","material","size","color","uncomfortable",
        "usability","confusing","misleading","overpriced","build quality","flimsy",
    ],
}

DEPT_RENK = {
    "Teknik Destek":      "#60A5FA",
    "Yazilim Ekibi":      "#4ADE80",
    "Lojistik":           "#FCD34D",
    "Musteri Hizmetleri": "#F87171",
    "Urun Yonetimi":      "#C084FC",
    "Arsiv (Olumlu)":     "#34D399",
}

ETIKETLER = [
    "hardware defect or malfunction",
    "software bug or app issue",
    "shipping and delivery problem",
    "customer service complaint",
    "product design or usability issue",
]
TURKCE = {
    "hardware defect or malfunction":    "Teknik Destek",
    "software bug or app issue":         "Yazilim Ekibi",
    "shipping and delivery problem":     "Lojistik",
    "customer service complaint":        "Musteri Hizmetleri",
    "product design or usability issue": "Urun Yonetimi",
}

def kural_ile_departman(metin):
    metin_lower = str(metin).lower()
    skorlar = {d: sum(1 for k in ks if k in metin_lower) for d, ks in KURALLAR.items()}
    en_iyi  = max(skorlar, key=skorlar.get)
    max_s   = skorlar[en_iyi]
    if max_s == 0:
        return {"departman": "Teknik Destek", "guven": 0.25}
    return {"departman": en_iyi, "guven": round(min(0.45 + max_s * 0.1, 0.90), 2)}

def ozet_cikar(metin, cumle=2):
    try:
        from sumy.parsers.plaintext import PlaintextParser
        from sumy.nlp.tokenizers import Tokenizer
        from sumy.summarizers.lsa import LsaSummarizer
        if len(str(metin)) < 100:
            return metin
        parser = PlaintextParser.from_string(str(metin), Tokenizer("english"))
        s = LsaSummarizer()(parser.document, cumle)
        return " ".join(str(c) for c in s) or str(metin)[:200]
    except Exception:
        return str(metin)[:200]

def analiz_et(metin, star, analyzer, classifier, zero_shot_ok):
    vader       = analyzer.polarity_scores(str(metin))["compound"]
    star_val    = star if star else (1 if vader < -0.3 else 4)
    prob_skor   = int(star_val <= 3) * 0.6 + int(vader < -0.05) * 0.4
    problem_var = prob_skor >= 0.5

    if problem_var:
        kural = kural_ile_departman(metin)
        if kural["guven"] < 0.45 and zero_shot_ok:
            try:
                s   = classifier(str(metin)[:512], ETIKETLER, multi_label=False)
                dept  = TURKCE[s["labels"][0]]
                guven = round(s["scores"][0], 3)
            except Exception:
                dept, guven = kural["departman"], kural["guven"]
        else:
            dept, guven = kural["departman"], kural["guven"]
    else:
        dept, guven = "Arsiv (Olumlu)", 1.0

    return {
        "ozet":        ozet_cikar(metin),
        "problem_var": problem_var,
        "vader":       round(vader, 3),
        "prob_skor":   round(prob_skor, 2),
        "departman":   dept,
        "guven":       guven,
    }

analyzer, classifier, zero_shot_ok = nlp_yukle()

with st.sidebar:
    st.markdown("## ReviewLens")
    st.markdown("<div style=\'color:#6B7280;font-size:13px;margin-bottom:24px\'>Amazon Review Analyzer</div>", unsafe_allow_html=True)
    sayfa = st.radio("Sayfa", ["Tek Yorum Analizi", "Toplu CSV Analizi", "Dashboard"], label_visibility="collapsed")

if sayfa == "Tek Yorum Analizi":
    st.markdown("# Tek Yorum Analizi")
    st.markdown("<div style=\'color:#6B7280;margin-bottom:24px\'>Yorum gir, ozet + departman + problem durumu al.</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        metin = st.text_area("Yorum", placeholder="Yorumu buraya yaz...", height=160, label_visibility="collapsed")
    with col2:
        star = st.select_slider("Yildiz", options=[1,2,3,4,5], value=3)
        st.markdown(f"<div style=\'text-align:center;font-size:28px\'>{"⭐"*star}</div>", unsafe_allow_html=True)
        btn = st.button("Analiz Et", use_container_width=True, type="primary")

    if btn and metin.strip():
        with st.spinner("Analiz ediliyor..."):
            s = analiz_et(metin, star, analyzer, classifier, zero_shot_ok)

        st.markdown("<div class=\'divider\'></div>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        renk = "#EF4444" if s["problem_var"] else "#10B981"
        durum = "Problemli" if s["problem_var"] else "Sorunsuz"
        m1.markdown(f"<div class=\'metric-card\'><div class=\'label\'>Durum</div><div class=\'value\' style=\'color:{renk};font-size:20px\'>{durum}</div><div style=\'color:#6B7280;font-size:12px\'>Skor: {s[\'prob_skor\']}</div></div>", unsafe_allow_html=True)
        vr = "#EF4444" if s["vader"]<-0.05 else "#10B981" if s["vader"]>0.05 else "#F59E0B"
        m2.markdown(f"<div class=\'metric-card\'><div class=\'label\'>VADER</div><div class=\'value\' style=\'color:{vr}\'>{s[\'vader\']:+.3f}</div></div>", unsafe_allow_html=True)
        m3.markdown(f"<div class=\'metric-card\'><div class=\'label\'>Guven</div><div class=\'value\'>%{s[\'guven\']*100:.0f}</div></div>", unsafe_allow_html=True)

        dr = DEPT_RENK.get(s["departman"], "#ffffff")
        st.markdown(f"<div class=\'result-box {\'problem\' if s[\'problem_var\'] else \'ok\'}\' ><div style=\'font-size:12px;color:#6B7280;margin-bottom:8px\'>DEPARTMAN</div><span style=\'color:{dr};font-size:18px;font-weight:600\'>{s[\'departman\']}</span></div>", unsafe_allow_html=True)
        st.markdown(f"<div class=\'result-box\'><div style=\'font-size:12px;color:#6B7280;margin-bottom:8px\'>OZET</div><div class=\'summary-text\'>{s[\'ozet\']}</div></div>", unsafe_allow_html=True)
    elif btn:
        st.warning("Lutfen bir yorum gir.")

elif sayfa == "Toplu CSV Analizi":
    st.markdown("# Toplu CSV Analizi")
    yuklenen = st.file_uploader("CSV sec", type=["csv"], label_visibility="collapsed")
    if yuklenen:
        df = pd.read_csv(yuklenen)
        st.markdown(f"**{len(df):,} satir** yuklendi.")
        with st.expander("Onizle"):
            st.dataframe(df.head(5), use_container_width=True)
        max_s = st.slider("Kac satir analiz edilsin?", 10, min(500, len(df)), min(100, len(df)))
        if st.button("Baslat", type="primary"):
            prog = st.progress(0)
            sonuclar = []
            df_a = df.head(max_s).copy()
            for i, row in df_a.iterrows():
                m = str(row.get("review_body", row.get("text", "")))
                sr = row.get("star_rating", None)
                try: sr = int(sr)
                except: sr = None
                sonuclar.append(analiz_et(m, sr, analyzer, classifier, zero_shot_ok))
                prog.progress((i+1)/len(df_a))
            prog.empty()
            res = pd.concat([df_a.reset_index(drop=True), pd.DataFrame(sonuclar)], axis=1)
            st.dataframe(res[["review_body","departman","problem_var","guven","vader","ozet"]], use_container_width=True, height=400)
            st.download_button("Indir (CSV)", res.to_csv(index=False).encode("utf-8"), "sonuclar.csv", "text/csv", use_container_width=True)

elif sayfa == "Dashboard":
    st.markdown("# Dashboard")
    f = st.file_uploader("Sonuc CSV yukle", type=["csv"], label_visibility="collapsed")
    if f:
        df = pd.read_csv(f)
        toplam = len(df)
        prob   = df["problem_var"].sum() if "problem_var" in df.columns else 0
        k1,k2,k3 = st.columns(3)
        k1.metric("Toplam", f"{toplam:,}")
        k2.metric("Problemli", f"{int(prob):,}")
        k3.metric("Oran", f"%{prob/toplam*100:.1f}")
        col1, col2 = st.columns(2)
        with col1:
            if "departman" in df.columns:
                d = df["departman"].value_counts().reset_index()
                d.columns = ["Departman","Sayi"]
                fig = px.bar(d, x="Sayi", y="Departman", orientation="h",
                             color="Departman", title="Departman Dagilimi", template="plotly_dark")
                fig.update_layout(showlegend=False, plot_bgcolor="#1A1D27", paper_bgcolor="#1A1D27")
                st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig2 = go.Figure(go.Pie(
                labels=["Problemli","Sorunsuz"],
                values=[int(prob), int(toplam-prob)],
                hole=0.55,
                marker_colors=["#EF4444","#10B981"],
            ))
            fig2.update_layout(title="Problem Dagilimi", template="plotly_dark",
                               plot_bgcolor="#1A1D27", paper_bgcolor="#1A1D27")
            st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Once Toplu CSV Analizi sayfasindan analiz yap, sonucu buraya yukle.")
