
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="ReviewLens — Amazon Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0A0C13;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1117 0%, #141721 100%);
    border-right: 1px solid #1E2130;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADER */
.hero {
    background: linear-gradient(135deg, #1a1f35 0%, #0f1117 50%, #1a1225 100%);
    border: 1px solid #2A2D3E;
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    color: #818CF8;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 99px;
    margin-bottom: 14px;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    color: #F9FAFB;
    margin: 0 0 8px 0;
    line-height: 1.2;
}
.hero-title span {
    background: linear-gradient(135deg, #818CF8, #C084FC);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 14px;
    color: #6B7280;
    margin: 0;
    max-width: 500px;
    line-height: 1.6;
}
.hero-stats {
    display: flex;
    gap: 28px;
    margin-top: 20px;
}
.hero-stat {
    text-align: center;
}
.hero-stat .num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #F9FAFB;
}
.hero-stat .lbl {
    font-size: 11px;
    color: #6B7280;
    margin-top: 2px;
}

/* INPUT ALANI */
.input-card {
    background: #13151F;
    border: 1px solid #1E2130;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    transition: border-color .2s;
}
.input-card:hover {
    border-color: #2A2D3E;
}
.input-label {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #6B7280;
    margin-bottom: 10px;
}

/* SONUÇ KARTLARI */
.result-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 20px 0;
}
.result-card {
    background: #13151F;
    border: 1px solid #1E2130;
    border-radius: 14px;
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}
.result-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
}
.result-card.green::after { background: linear-gradient(90deg, #10B981, #34D399); }
.result-card.red::after   { background: linear-gradient(90deg, #EF4444, #F87171); }
.result-card.blue::after  { background: linear-gradient(90deg, #6366F1, #818CF8); }
.result-card.amber::after { background: linear-gradient(90deg, #F59E0B, #FCD34D); }

.rc-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #4B5563;
    margin-bottom: 8px;
}
.rc-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #F9FAFB;
    margin-bottom: 4px;
}
.rc-sub {
    font-size: 12px;
    color: #6B7280;
}

/* DEPARTMAN KARTI */
.dept-card {
    background: #13151F;
    border: 1px solid #1E2130;
    border-radius: 16px;
    padding: 24px 28px;
    margin: 16px 0;
    display: flex;
    align-items: center;
    gap: 20px;
}
.dept-card.problem { border-left: 3px solid #EF4444; }
.dept-card.ok      { border-left: 3px solid #10B981; }
.dept-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    flex-shrink: 0;
}
.dept-info .dept-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: .08em;
    text-transform: uppercase;
    color: #4B5563;
    margin-bottom: 4px;
}
.dept-info .dept-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #F9FAFB;
}
.dept-info .dept-sub {
    font-size: 12px;
    color: #6B7280;
    margin-top: 3px;
}
.dept-guven {
    margin-left: auto;
    text-align: right;
}
.dept-guven .guven-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 28px;
    font-weight: 700;
}
.dept-guven .guven-lbl {
    font-size: 11px;
    color: #6B7280;
}

/* DIVIDER */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E2130, transparent);
    margin: 24px 0;
}

/* SECTION TITLE */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 16px;
    font-weight: 600;
    color: #E5E7EB;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* SIDEBAR */
.sidebar-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: #F9FAFB;
    margin-bottom: 4px;
}
.sidebar-sub {
    font-size: 12px;
    color: #4B5563;
    margin-bottom: 28px;
}
.sidebar-section {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: #374151;
    margin: 20px 0 8px;
}

/* INFO BOX */
.info-box {
    background: rgba(99,102,241,0.08);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 13px;
    color: #818CF8;
    margin-top: 16px;
    line-height: 1.6;
}

/* STAGGER ANİMASYON */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
.fade-up { animation: fadeUp .4s ease forwards; }
.fade-up-2 { animation: fadeUp .4s .1s ease both; }
.fade-up-3 { animation: fadeUp .4s .2s ease both; }
</style>
""", unsafe_allow_html=True)

# ── NLP YÜKLEME ─────────────────────────────────────────────────────────────
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

# ── SABİTLER ────────────────────────────────────────────────────────────────
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

DEPT_CONFIG = {
    "Teknik Destek":      {"renk": "#60A5FA", "bg": "rgba(96,165,250,0.1)",  "ikon": "🔧", "aciklama": "Donanim & arizalar"},
    "Yazilim Ekibi":      {"renk": "#4ADE80", "bg": "rgba(74,222,128,0.1)",  "ikon": "💻", "aciklama": "Yazilim & uygulama sorunlari"},
    "Lojistik":           {"renk": "#FCD34D", "bg": "rgba(252,211,77,0.1)",  "ikon": "📦", "aciklama": "Kargo & teslimat sorunlari"},
    "Musteri Hizmetleri": {"renk": "#F87171", "bg": "rgba(248,113,113,0.1)", "ikon": "🤝", "aciklama": "Musteri iliskileri & iade"},
    "Urun Yonetimi":      {"renk": "#C084FC", "bg": "rgba(192,132,252,0.1)", "ikon": "📊", "aciklama": "Urun tasarimi & kalite"},
    "Arsiv (Olumlu)":     {"renk": "#34D399", "bg": "rgba(52,211,153,0.1)",  "ikon": "✅", "aciklama": "Olumlu yorum — arsivlendi"},
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

# ── FONKSİYONLAR ────────────────────────────────────────────────────────────
def kural_ile_departman(metin):
    metin_lower = str(metin).lower()
    skorlar = {d: sum(1 for k in ks if k in metin_lower) for d, ks in KURALLAR.items()}
    en_iyi  = max(skorlar, key=skorlar.get)
    max_s   = skorlar[en_iyi]
    if max_s == 0:
        return {"departman": "Teknik Destek", "guven": 0.25}
    return {"departman": en_iyi, "guven": round(min(0.45 + max_s * 0.1, 0.90), 2)}

def analiz_et(metin, star, analyzer, classifier, zero_shot_ok):
    vader       = analyzer.polarity_scores(str(metin))["compound"]
    star_val    = star if star else (1 if vader < -0.3 else 4)
    prob_skor   = int(star_val <= 3) * 0.6 + int(vader < -0.05) * 0.4
    problem_var = prob_skor >= 0.5
    zero_shot_skorlar = {}

    if problem_var:
        kural = kural_ile_departman(metin)
        if kural["guven"] < 0.45 and zero_shot_ok:
            try:
                sonuc = classifier(str(metin)[:512], ETIKETLER, multi_label=False)
                dept  = TURKCE[sonuc["labels"][0]]
                guven = round(sonuc["scores"][0], 3)
                zero_shot_skorlar = {
                    TURKCE[l]: round(s, 3)
                    for l, s in zip(sonuc["labels"], sonuc["scores"])
                }
            except Exception:
                dept, guven = kural["departman"], kural["guven"]
        else:
            dept, guven = kural["departman"], kural["guven"]
    else:
        dept, guven = "Arsiv (Olumlu)", 1.0

    return {
        "problem_var":       problem_var,
        "vader":             round(vader, 3),
        "prob_skor":         round(prob_skor, 2),
        "departman":         dept,
        "guven":             guven,
        "zero_shot_skorlar": zero_shot_skorlar,
    }

analyzer, classifier, zero_shot_ok = nlp_yukle()

# ── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("<div class='sidebar-logo'>🔍 ReviewLens</div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-sub'>Amazon Review Intelligence</div>", unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section'>Navigasyon</div>", unsafe_allow_html=True)
    sayfa = st.radio(
        "Sayfa",
        ["Tek Yorum Analizi", "Toplu CSV Analizi", "Dashboard"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section'>Model Durumu</div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:12px;color:#4B5563;line-height:1.8'>"
        "VADER Sentiment &nbsp; <span style='color:#34D399'>✓ Aktif</span><br>"
        "Zero-shot BART &nbsp;&nbsp; <span style='color:" + ("#34D399' >✓ Aktif" if zero_shot_ok else "#EF4444' >✗ Yuklenemedi") + "</span><br>"
        "Kural Motoru &nbsp;&nbsp;&nbsp;&nbsp; <span style='color:#34D399'>✓ Aktif</span>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='sidebar-section'>Kategoriler</div>", unsafe_allow_html=True)
    for dept, cfg in DEPT_CONFIG.items():
        st.markdown(
            "<div style='display:flex;align-items:center;gap:8px;margin-bottom:6px'>"
            "<span style='font-size:14px'>" + cfg["ikon"] + "</span>"
            "<span style='font-size:12px;color:#6B7280'>" + dept + "</span>"
            "</div>",
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════════════════════
# SAYFA 1 — TEK YORUM ANALİZİ
# ════════════════════════════════════════════════════════════════════════════
if sayfa == "Tek Yorum Analizi":

    # Hero header
    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>AI-Powered Review Analysis</div>
        <h1 class='hero-title'>Yorum <span>Analiz</span> Motoru</h1>
        <p class='hero-sub'>
            Musteri yorumlarini yapay zeka ile analiz et. Problem tespit et,
            ilgili departmana yonlendir.
        </p>
        <div class='hero-stats'>
            <div class='hero-stat'>
                <div class='num'>6</div>
                <div class='lbl'>Departman</div>
            </div>
            <div class='hero-stat'>
                <div class='num'>2</div>
                <div class='lbl'>NLP Modeli</div>
            </div>
            <div class='hero-stat'>
                <div class='num'>~1s</div>
                <div class='lbl'>Analiz Suresi</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Input alanı
    col1, col2 = st.columns([3, 1], gap="medium")

    with col1:
        st.markdown("<div class='input-label'>Musteri Yorumu</div>", unsafe_allow_html=True)
        metin = st.text_area(
            "yorum",
            placeholder="Musterinin yorumunu buraya yapistirin...",
            height=180,
            label_visibility="collapsed"
        )

    with col2:
        st.markdown("<div class='input-label'>Yildiz Puani</div>", unsafe_allow_html=True)
        star = st.select_slider(
            "yildiz",
            options=[1, 2, 3, 4, 5],
            value=3,
            label_visibility="collapsed"
        )
        renk_map = {1: "#EF4444", 2: "#F97316", 3: "#F59E0B", 4: "#84CC16", 5: "#10B981"}
        st.markdown(
            "<div style='text-align:center;margin:12px 0'>"
            "<div style='font-size:32px;margin-bottom:6px'>" + "⭐" * star + "</div>"
            "<div style='font-size:13px;font-weight:600;color:" + renk_map[star] + "'>"
            + ["", "Cok Kotu", "Kotu", "Orta", "Iyi", "Mukemmel"][star] +
            "</div></div>",
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        btn = st.button("🔍 Analiz Et", use_container_width=True, type="primary")

    # Analiz sonucu
    if btn and metin.strip():
        with st.spinner("Analiz ediliyor..."):
            s = analiz_et(metin, star, analyzer, classifier, zero_shot_ok)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # Sonuç kartları
        durum_renk  = "red" if s["problem_var"] else "green"
        durum_text  = "⚠️ Problemli" if s["problem_var"] else "✅ Sorunsuz"
        vader_renk  = "red" if s["vader"] < -0.05 else "green" if s["vader"] > 0.05 else "amber"

        st.markdown(
            "<div class='result-grid fade-up'>"

            "<div class='result-card " + durum_renk + "'>"
            "<div class='rc-label'>Durum</div>"
            "<div class='rc-value'>" + durum_text + "</div>"
            "<div class='rc-sub'>Problem skoru: " + str(s["prob_skor"]) + "</div>"
            "</div>"

            "<div class='result-card " + vader_renk + "'>"
            "<div class='rc-label'>Duygu Skoru (VADER)</div>"
            "<div class='rc-value'>" + str(s["vader"]) + "</div>"
            "<div class='rc-sub'>-1.0 negatif → +1.0 pozitif</div>"
            "</div>"

            "<div class='result-card blue'>"
            "<div class='rc-label'>Model Guveni</div>"
            "<div class='rc-value'>%" + str(round(s["guven"] * 100)) + "</div>"
            "<div class='rc-sub'>Siniflandirma guveni</div>"
            "</div>"

            "</div>",
            unsafe_allow_html=True
        )

        # Departman kartı
        dept    = s["departman"]
        cfg     = DEPT_CONFIG.get(dept, {"renk": "#6B7280", "bg": "#1A1D27", "ikon": "📋", "aciklama": ""})
        cls     = "problem" if s["problem_var"] else "ok"

        st.markdown(
            "<div class='dept-card " + cls + " fade-up-2'>"
            "<div class='dept-icon' style='background:" + cfg["bg"] + "'>" + cfg["ikon"] + "</div>"
            "<div class='dept-info'>"
            "<div class='dept-label'>Yonlendirilecek Departman</div>"
            "<div class='dept-name' style='color:" + cfg["renk"] + "'>" + dept + "</div>"
            "<div class='dept-sub'>" + cfg["aciklama"] + "</div>"
            "</div>"
            "<div class='dept-guven'>"
            "<div class='guven-num' style='color:" + cfg["renk"] + "'>%" + str(round(s["guven"] * 100)) + "</div>"
            "<div class='guven-lbl'>Guven</div>"
            "</div>"
            "</div>",
            unsafe_allow_html=True
        )

        # Zero-shot grafik
        if s["zero_shot_skorlar"]:
            st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
            st.markdown("<div class='section-title fade-up-3'>📊 Departman Olasilik Dagilimi</div>", unsafe_allow_html=True)

            zs    = s["zero_shot_skorlar"]
            zs_df = pd.DataFrame({
                "Departman": list(zs.keys()),
                "Skor":      list(zs.values()),
            }).sort_values("Skor")

            renkler = [DEPT_CONFIG.get(d, {}).get("renk", "#6B7280") for d in zs_df["Departman"]]

            fig = go.Figure(go.Bar(
                x=zs_df["Skor"],
                y=zs_df["Departman"],
                orientation="h",
                marker=dict(
                    color=renkler,
                    line=dict(width=0),
                ),
                text=["%" + str(round(v * 100, 1)) for v in zs_df["Skor"]],
                textposition="outside",
                textfont=dict(color="#9CA3AF", size=12),
            ))
            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#13151F",
                paper_bgcolor="#13151F",
                height=260,
                margin=dict(l=0, r=60, t=10, b=10),
                xaxis=dict(range=[0, 1.1], showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, tickfont=dict(size=13, color="#D1D5DB")),
                bargap=0.35,
            )
            st.plotly_chart(fig, use_container_width=True)

        # Bilgi kutusu
        st.markdown(
            "<div class='info-box fade-up-3'>"
            "ℹ️ Bu analiz <b>VADER duygu analizi</b> ve <b>Zero-shot BART</b> modellerini birlestirir. "
            "Yildiz puani ve metin duygusu birlikte degerlendirilir."
            "</div>",
            unsafe_allow_html=True
        )

    elif btn:
        st.warning("Lutfen bir yorum metni girin.")

# ════════════════════════════════════════════════════════════════════════════
# SAYFA 2 — TOPLU CSV ANALİZİ
# ════════════════════════════════════════════════════════════════════════════
elif sayfa == "Toplu CSV Analizi":

    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>Batch Processing</div>
        <h1 class='hero-title'>Toplu <span>CSV</span> Analizi</h1>
        <p class='hero-sub'>CSV dosyasi yukle, tum yorumlari otomatik analiz et, filtrele ve indir.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='info-box'>CSV dosyanda <b>review_body</b> sutunu olmali. "
        "<b>star_rating</b> varsa daha dogru sonuc verir.</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    yuklenen = st.file_uploader("CSV dosyasi sec", type=["csv"], label_visibility="collapsed")

    if yuklenen:
        df = pd.read_csv(yuklenen)

        col1, col2, col3 = st.columns(3)
        col1.metric("Toplam Satir", f"{len(df):,}")
        col2.metric("Sutun Sayisi", str(df.shape[1]))
        col3.metric("Boyut", f"{yuklenen.size/1024:.1f} KB")

        with st.expander("Veriyi Onizle"):
            st.dataframe(df.head(5), use_container_width=True)

        max_s = st.slider(
            "Kac satir analiz edilsin?",
            10, min(500, len(df)), min(100, len(df))
        )

        if st.button("🚀 Analizi Baslat", type="primary", use_container_width=True):
            prog   = st.progress(0)
            durum  = st.empty()
            sonuclar = []
            df_a   = df.head(max_s).copy()
            toplam = len(df_a)

            for i, row in enumerate(df_a.itertuples()):
                m  = str(getattr(row, "review_body", getattr(row, "text", "")))
                sr = getattr(row, "star_rating", None)
                try:
                    sr = int(sr)
                except Exception:
                    sr = None
                sonuclar.append(analiz_et(m, sr, analyzer, classifier, zero_shot_ok))
                prog.progress((i + 1) / toplam)
                durum.markdown(
                    "<div style='font-size:12px;color:#6B7280'>Isleniyor: "
                    + str(i + 1) + " / " + str(toplam) + "</div>",
                    unsafe_allow_html=True
                )

            prog.empty()
            durum.empty()

            res = pd.concat(
                [df_a.reset_index(drop=True), pd.DataFrame(sonuclar)],
                axis=1
            )

            # Özet
            prob_sayi = int(res["problem_var"].sum())
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("Analiz Edilen", str(toplam))
            k2.metric("Problemli", str(prob_sayi))
            k3.metric("Sorunsuz", str(toplam - prob_sayi))
            k4.metric("Problem Orani", "%" + str(round(prob_sayi / toplam * 100, 1)))

            goster_cols = [c for c in ["review_body","departman","problem_var","guven","vader"] if c in res.columns]
            st.dataframe(res[goster_cols], use_container_width=True, height=380)

            st.download_button(
                "⬇️ Sonuclari Indir (CSV)",
                res.to_csv(index=False).encode("utf-8"),
                "review_analiz_sonuclari.csv",
                "text/csv",
                use_container_width=True,
            )

# ════════════════════════════════════════════════════════════════════════════
# SAYFA 3 — DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
elif sayfa == "Dashboard":

    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>Analytics</div>
        <h1 class='hero-title'>Analitik <span>Dashboard</span></h1>
        <p class='hero-sub'>Toplu analiz sonuclarini gorselleştir. Departman dagilimlari ve trend analizleri.</p>
    </div>
    """, unsafe_allow_html=True)

    f = st.file_uploader("Sonuc CSV yukle", type=["csv"], label_visibility="collapsed")

    if f:
        df     = pd.read_csv(f)
        toplam = len(df)
        prob   = int(df["problem_var"].sum()) if "problem_var" in df.columns else 0

        # Üst metrikler
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Toplam Yorum",   f"{toplam:,}")
        k2.metric("Problemli",      f"{prob:,}")
        k3.metric("Sorunsuz",       f"{toplam - prob:,}")
        k4.metric("Problem Orani",  "%" + str(round(prob / toplam * 100, 1)))

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown("<div class='section-title'>📊 Departman Dagilimi</div>", unsafe_allow_html=True)
            if "departman" in df.columns:
                d = df["departman"].value_counts().reset_index()
                d.columns = ["Departman", "Sayi"]
                renkler = [DEPT_CONFIG.get(dep, {}).get("renk", "#6B7280") for dep in d["Departman"]]
                fig = go.Figure(go.Bar(
                    x=d["Sayi"], y=d["Departman"],
                    orientation="h",
                    marker=dict(color=renkler, line=dict(width=0)),
                    text=d["Sayi"],
                    textposition="outside",
                    textfont=dict(color="#9CA3AF"),
                ))
                fig.update_layout(
                    template="plotly_dark",
                    plot_bgcolor="#13151F",
                    paper_bgcolor="#13151F",
                    height=320,
                    margin=dict(l=0, r=40, t=10, b=10),
                    xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                    yaxis=dict(showgrid=False, tickfont=dict(size=12, color="#D1D5DB")),
                    showlegend=False,
                    bargap=0.3,
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("<div class='section-title'>🎯 Problem Dagilimi</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Pie(
                labels=["Problemli", "Sorunsuz"],
                values=[prob, toplam - prob],
                hole=0.6,
                marker=dict(
                    colors=["#EF4444", "#10B981"],
                    line=dict(color="#0A0C13", width=3),
                ),
                textfont=dict(size=13),
            ))
            fig2.update_layout(
                template="plotly_dark",
                plot_bgcolor="#13151F",
                paper_bgcolor="#13151F",
                height=320,
                margin=dict(l=0, r=0, t=10, b=10),
                legend=dict(font=dict(color="#9CA3AF")),
                annotations=[dict(
                    text="%" + str(round(prob / toplam * 100, 0))[:-2],
                    x=0.5, y=0.5,
                    font=dict(size=28, color="#F9FAFB", family="Space Grotesk"),
                    showarrow=False
                )]
            )
            st.plotly_chart(fig2, use_container_width=True)

        # VADER dağılımı
        vader_col = next((c for c in ["vader", "VADER"] if c in df.columns), None)
        if vader_col:
            st.markdown("<div class='section-title'>📈 Duygu Skoru Dagilimi</div>", unsafe_allow_html=True)
            fig3 = go.Figure()
            fig3.add_trace(go.Histogram(
                x=df[vader_col],
                nbinsx=40,
                marker_color="#6366F1",
                marker_line=dict(width=0),
                opacity=0.8,
                name="VADER"
            ))
            fig3.add_vline(x=0, line_dash="dash", line_color="#F59E0B", line_width=1.5,
                           annotation_text="Notral sinir", annotation_font_color="#F59E0B")
            fig3.add_vline(x=-0.05, line_dash="dot", line_color="#EF4444", line_width=1,
                           annotation_text="Problem esigi", annotation_font_color="#EF4444")
            fig3.update_layout(
                template="plotly_dark",
                plot_bgcolor="#13151F",
                paper_bgcolor="#13151F",
                height=260,
                margin=dict(l=0, r=0, t=10, b=10),
                xaxis=dict(title="VADER Skoru", showgrid=False, zeroline=False),
                yaxis=dict(showgrid=False),
                showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.markdown(
            "<div style='text-align:center;padding:60px 20px'>"
            "<div style='font-size:48px;margin-bottom:16px'>📊</div>"
            "<div style='font-family:Space Grotesk;font-size:18px;font-weight:600;"
            "color:#E5E7EB;margin-bottom:8px'>Veri bekleniyor</div>"
            "<div style='font-size:14px;color:#6B7280'>"
            "Once Toplu CSV Analizi sayfasindan yorumlari analiz et,<br>"
            "indirdigin CSV dosyasini buraya yukle."
            "</div></div>",
            unsafe_allow_html=True
        )
