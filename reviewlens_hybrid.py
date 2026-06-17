import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import torch

st.set_page_config(
    page_title="ReviewLens — Amazon Review Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #080A12; overflow-x: hidden; }

/* Streamlit'in kendi app kapsayıcıları varsayılan olarak beyaz/açık renkli geliyor —
   bunları da koyu temaya dahil ediyoruz, aksi halde sayfa arka planı kısmen açık görünür */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stBottomBlockContainer"],
.main { background-color: #080A12 !important; }
[data-testid="stHeader"], [data-testid="stToolbar"] { background: transparent !important; }

section[data-testid="stSidebar"] { background: linear-gradient(180deg, #0D0F1A 0%, #10121E 100%); border-right: 1px solid #1A1D2E; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* Native Streamlit bileşenleri (text area, dosya yükleyici, metrik, dataframe, expander,
   select, slider, radio, buton) — koyu temaya uyumlu hale getiriliyor, tasarım değişmiyor */
[data-testid="stTextArea"] textarea { background-color: #0D0F1A !important; color: #E2E8F0 !important; border: 1px solid #1A1D2E !important; }
[data-testid="stTextArea"] textarea::placeholder { color: #475569 !important; }
[data-testid="stFileUploaderDropzone"] { background-color: #0D0F1A !important; border: 1px dashed #2A2D42 !important; }
[data-testid="stFileUploaderDropzone"] *, [data-testid="stFileUploaderDropzoneInstructions"] * { color: #94A3B8 !important; }
[data-testid="stMetric"] { background-color: #0D0F1A; border: 1px solid #1A1D2E; border-radius: 12px; padding: 14px 18px; }
[data-testid="stMetricValue"] { color: #F1F5F9 !important; }
[data-testid="stMetricLabel"] { color: #64748B !important; }
[data-testid="stDataFrame"], [data-testid="stDataFrame"] > div { background-color: #0D0F1A !important; }
[data-testid="stExpander"] { background-color: #0D0F1A !important; border: 1px solid #1A1D2E !important; border-radius: 10px; }
[data-testid="stExpander"] summary { color: #E2E8F0 !important; }
div[data-baseweb="select"] > div { background-color: #0D0F1A !important; border-color: #1A1D2E !important; color: #E2E8F0 !important; }
div[data-baseweb="popover"] li { background-color: #0D0F1A !important; color: #E2E8F0 !important; }
.stSlider [data-baseweb="slider"] div { background-color: #1A1D2E; }
label, .stRadio label, .stMarkdown, p, span { color: #94A3B8; }
.stButton button { background: linear-gradient(135deg,#6366F1,#8B5CF6) !important; color: #fff !important; border: none !important; }
hr { border-color: #1A1D2E !important; }
[data-testid="stAlert"] { background-color: #0D0F1A !important; }

.logo-wrap { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
.logo-icon { width: 36px; height: 36px; background: linear-gradient(135deg, #6366F1, #8B5CF6); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; box-shadow: 0 0 16px rgba(99,102,241,0.4); }
.logo-text { font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; background: linear-gradient(135deg, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

.hero { background: linear-gradient(135deg, #0D1128 0%, #0A0C16 40%, #130D20 100%); border: 1px solid #1E2235; border-radius: 20px; padding: 36px 40px; margin-bottom: 24px; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -80px; right: -60px; width: 350px; height: 350px; background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%); pointer-events: none; }
.hero::after { content: ''; position: absolute; bottom: -60px; left: 30%; width: 250px; height: 250px; background: radial-gradient(circle, rgba(139,92,246,0.07) 0%, transparent 70%); pointer-events: none; }
.hero-badge { display: inline-flex; align-items: center; gap: 6px; background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25); color: #818CF8; font-size: 11px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; padding: 5px 12px; border-radius: 99px; margin-bottom: 16px; }
.hero-title { font-family: 'Space Grotesk', sans-serif; font-size: 36px; font-weight: 700; color: #F1F5F9; margin: 0 0 10px 0; line-height: 1.15; }
.hero-title span { background: linear-gradient(135deg, #818CF8 0%, #C084FC 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-sub { font-size: 14px; color: #64748B; margin: 0 0 24px 0; line-height: 1.7; max-width: 480px; }
.hero-stats { display: flex; gap: 32px; }
.hero-stat .num { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #E2E8F0; }
.hero-stat .lbl { font-size: 11px; color: #475569; margin-top: 2px; letter-spacing: .04em; }

.sec-label { font-size: 11px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: #334155; margin-bottom: 8px; }

.res-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 20px 0 16px; }
.res-card { background: #0D0F1A; border: 1px solid #1A1D2E; border-radius: 14px; padding: 20px 22px; position: relative; overflow: hidden; transition: border-color .2s; }
.res-card:hover { border-color: #2A2D42; }
.res-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; border-radius: 14px 14px 0 0; }
.res-card.red::before   { background: linear-gradient(90deg, #EF4444, #F87171); }
.res-card.green::before { background: linear-gradient(90deg, #10B981, #34D399); }
.res-card.blue::before  { background: linear-gradient(90deg, #6366F1, #818CF8); }
.res-card.amber::before { background: linear-gradient(90deg, #F59E0B, #FCD34D); }

.rc-lbl { font-size: 10px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: #334155; margin-bottom: 10px; }
.rc-val { font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #F1F5F9; margin-bottom: 4px; line-height: 1; }
.rc-sub { font-size: 12px; color: #475569; margin-top: 6px; }
.rc-icon { position: absolute; top: 16px; right: 16px; font-size: 20px; opacity: 0.4; }

.dept-wrap { background: #0D0F1A; border: 1px solid #1A1D2E; border-radius: 16px; padding: 24px 28px; margin: 16px 0; display: flex; align-items: center; gap: 20px; position: relative; overflow: hidden; }
.dept-wrap.problem { border-left: 3px solid #EF4444; }
.dept-wrap.ok      { border-left: 3px solid #10B981; }
.dept-icon-wrap { width: 52px; height: 52px; border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
.dept-info .dept-lbl { font-size: 10px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: #334155; margin-bottom: 5px; }
.dept-info .dept-name { font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 700; line-height: 1.1; }
.dept-info .dept-desc { font-size: 13px; color: #475569; margin-top: 4px; }
.dept-right { margin-left: auto; text-align: right; flex-shrink: 0; }
.dept-pct { font-family: 'Space Grotesk', sans-serif; font-size: 32px; font-weight: 700; line-height: 1; }
.dept-pct-lbl { font-size: 11px; color: #475569; margin-top: 4px; }

.source-pill { display: inline-flex; align-items: center; gap: 5px; background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.25); color: #A5B4FC; font-size: 10px; font-weight: 600; letter-spacing: .04em; padding: 3px 10px; border-radius: 99px; margin-left: 10px; vertical-align: middle; }
.source-pill.bert { background: rgba(192,132,252,0.12); border-color: rgba(192,132,252,0.25); color: #D8B4FE; }

.prog-wrap { margin-top: 14px; }
.prog-label { display: flex; justify-content: space-between; font-size: 11px; color: #475569; margin-bottom: 6px; }
.prog-bar-bg { height: 6px; background: #1A1D2E; border-radius: 99px; overflow: hidden; }
.prog-bar-fill { height: 100%; border-radius: 99px; transition: width .6s ease; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2235 30%, #1E2235 70%, transparent); margin: 22px 0; }

.info-box { background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.15); border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #6366F1; margin-top: 16px; line-height: 1.6; }
.conflict-box { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); border-radius: 10px; padding: 12px 16px; font-size: 13px; color: #FCD34D; margin-top: 16px; line-height: 1.6; }

.sb-section { font-size: 10px; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; color: #1E293B; margin: 22px 0 10px; }
.sb-status { display: flex; align-items: center; justify-content: space-between; font-size: 12px; color: #475569; margin-bottom: 8px; padding: 8px 10px; background: #0A0C14; border-radius: 8px; border: 1px solid #1A1D2E; }
.sb-dot-green { color: #10B981; font-weight: 600; }
.sb-dot-red   { color: #EF4444; font-weight: 600; }
.sb-dept-row { display: flex; align-items: center; gap: 8px; padding: 6px 8px; border-radius: 8px; margin-bottom: 4px; transition: background .15s; }
.sb-dept-row:hover { background: #0D0F1A; }
.sb-dept-name { font-size: 12px; color: #64748B; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
.fade-1 { animation: fadeUp .35s ease forwards; }
.fade-2 { animation: fadeUp .35s .08s ease both; }
.fade-3 { animation: fadeUp .35s .16s ease both; }
</style>
""", unsafe_allow_html=True)

# ── KEYWORD KURALLARI (hızlı, birincil katman) ──
PROBLEM_KELIMELERI_DEPT = {
    "Teknik Destek": ["broken","defect","malfunction","not working","stopped working","hardware",
        "damage","cracked","dead","faulty","repair","doesnt work","doesn't work","stopped","fell apart",
        "freeze","freezing","stuck","unresponsive","corrupt","overheating","battery dead","screen cracked",
        "no power","wont turn on","no sound","physical damage","worst hardware","terrible hardware"],
    "Yazilim Ekibi": ["software","app","crash","crashing","bug","update","glitch","error","install",
        "compatible","firmware","driver","reboot","bluetooth","wifi","sync","patch","reinstall","lag",
        "slow","not loading","wont open","keeps closing","login issue","sign in","timeout",
        "authentication","server","connection issue","worst app","terrible app","app not working"],
    "Lojistik": ["delivery","shipping","package","arrived","shipment","damaged box","missing","lost",
        "never received","wrong item","not delivered","still waiting","stolen","opened box","repackaged",
        "weeks late","days late","late delivery","delayed","delay","customs","package damaged",
        "worst delivery","terrible delivery","never arrived","wrong address","package lost"],
    "Musteri Hizmetleri": ["customer service","support","refund","warranty","response","replied","contact",
        "ignored","rude","unhelpful","representative","call center","exchange","complaint","no reply",
        "not responding","escalate","manager","supervisor","promised","lied","scam","fraud","dispute",
        "return policy","never called","worst service","terrible service","seller","vendor","sold by",
        "third party","not as advertised","fake","counterfeit"],
    "Urun Yonetimi": ["design","quality","cheap","material","size","color","uncomfortable","usability",
        "confusing","misleading","overpriced","build quality","poorly made","flimsy","smell","cheap plastic",
        "breaks easily","not as described","different from photo","not worth","false advertising",
        "wrong color","wrong size","terrible product","poor quality","bad quality","low quality",
        "waste of money","disappointing product","broke after","stopped working after","died after",
        "wore out","lasted only","months later","weeks later","no longer works","quit working"],
}
GENEL_PROBLEM = ["terrible","awful","horrible","worst","useless","disappointed","waste","regret",
    "never again","do not buy","avoid","zero stars","one star","not happy","very bad","really bad",
    "extremely bad","issue","problem","fail","failed","failure","cannot","unable","keeps",
    "still not fixed","still not working"]
POZITIF_IFADELER = {
    "Lojistik": ["fast delivery","quick delivery","great delivery","perfect delivery","amazing delivery",
        "excellent delivery","speedy delivery","fast shipping","quick shipping","free shipping","on time",
        "arrived on time","arrived quickly","delivered fast","great packaging","perfect packaging","well packaged"],
    "Musteri Hizmetleri": ["great service","excellent service","amazing service","helpful service",
        "great support","excellent support","amazing support","helpful support","great customer service",
        "excellent customer service","fast response","quick response","very helpful","very responsive"],
    "Yazilim Ekibi": ["great app","excellent app","amazing app","works perfectly","works great","no bugs",
        "runs smoothly","great software","easy to use","user friendly"],
    "Teknik Destek": ["works perfectly","works great","no issues","great hardware","excellent build",
        "solid build","excellent quality","perfect condition","no problems"],
}

DEPT_CFG = {
    "Teknik Destek":      {"renk":"#60A5FA","bg":"rgba(96,165,250,0.1)","ikon":"🔧","desc":"Donanim & arizalar"},
    "Yazilim Ekibi":      {"renk":"#4ADE80","bg":"rgba(74,222,128,0.1)","ikon":"💻","desc":"Yazilim & uygulama sorunlari"},
    "Lojistik":           {"renk":"#FCD34D","bg":"rgba(252,211,77,0.1)","ikon":"📦","desc":"Kargo & teslimat sorunlari"},
    "Musteri Hizmetleri": {"renk":"#F87171","bg":"rgba(248,113,113,0.1)","ikon":"🤝","desc":"Musteri iliskileri & iade"},
    "Urun Yonetimi":      {"renk":"#C084FC","bg":"rgba(192,132,252,0.1)","ikon":"📊","desc":"Urun tasarimi & kalite"},
    "Arsiv (Olumlu)":     {"renk":"#34D399","bg":"rgba(52,211,153,0.1)","ikon":"✅","desc":"Olumlu yorum — arsivlendi"},
}

# BERT'in 7 kategorisini bu 5 departmana eşler (fallback katmanı)
BERT_LABEL_TO_DEPT = {
    "problem_yok": "Arsiv (Olumlu)",
    "ürün_kalitesi": "Urun Yonetimi",
    "ürün_dayanıklılığı": "Urun Yonetimi",
    "teknik_sorun": "Teknik Destek",
    "içerik_beklenti": "Urun Yonetimi",
    "kargo_teslimat": "Lojistik",
    "satıcı": "Musteri Hizmetleri",
}

RULE_CONFIDENCE_THRESHOLD = 0.45  # bu eşiğin altında BERT'e devredilir

# ── MODEL YÜKLEME ──
@st.cache_resource
def load_bert():
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    tokenizer = AutoTokenizer.from_pretrained("arcasoyece/amazon-review-classifier")
    model = AutoModelForSequenceClassification.from_pretrained("arcasoyece/amazon-review-classifier")
    return tokenizer, model

@st.cache_resource
def load_vader():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    return SentimentIntensityAnalyzer()

# ── KURAL TABANLI KATMAN ──
def metin_problemi_var_mi(metin):
    metin_lower = str(metin).lower()
    if any(k in metin_lower for k in GENEL_PROBLEM):
        return True
    for kelimeler in PROBLEM_KELIMELERI_DEPT.values():
        if any(k in metin_lower for k in kelimeler):
            return True
    return False

def kural_dept(metin):
    metin_lower = str(metin).lower()
    skorlar = {}
    for dept, kelimeler in PROBLEM_KELIMELERI_DEPT.items():
        eslesme = sum(1 for k in kelimeler if k in metin_lower)
        genel = sum(1 for k in GENEL_PROBLEM if k in metin_lower)
        skorlar[dept] = eslesme + genel * 0.3

    for dept, pozitif_kelimeler in POZITIF_IFADELER.items():
        pozitif_var = any(k in metin_lower for k in pozitif_kelimeler)
        negatif_var = any(k in metin_lower for k in PROBLEM_KELIMELERI_DEPT.get(dept, []))
        if pozitif_var and not negatif_var:
            skorlar[dept] = 0

    en_iyi = max(skorlar, key=skorlar.get)
    max_skor = skorlar[en_iyi]
    if max_skor == 0:
        return {"departman": None, "guven": 0.0}
    guven = round(min(0.45 + max_skor * 0.10, 0.95), 2)
    return {"departman": en_iyi, "guven": guven}

# ── BERT KATMANI (fallback) ──
def bert_predict(metin):
    tokenizer, model = load_bert()
    id2label = model.config.id2label
    inputs = tokenizer(metin, return_tensors="pt", truncation=True, max_length=128, return_token_type_ids=False)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=-1)[0]
    top_id = probs.argmax().item()
    label = id2label[top_id]
    return {"departman": BERT_LABEL_TO_DEPT.get(label, "Urun Yonetimi"), "guven": probs[top_id].item(), "label": label}

# ── HİBRİT ANALİZ ──
def analiz_et(metin, star):
    analyzer = load_vader()
    vader = analyzer.polarity_scores(str(metin))["compound"]
    sv = star if star else (1 if vader < -0.3 else 4)
    teknik = metin_problemi_var_mi(metin)

    if vader > 0.5:
        ps = 0.0
    elif vader < -0.3:
        ps = 1.0
    elif teknik and vader > 0.1:
        ps = 0.0
    elif teknik and vader <= 0.1:
        ps = 1.0
    else:
        ps = int(sv <= 3) * 0.4 + int(vader < -0.05) * 0.6

    prob = ps >= 0.5
    source = "Kural Tabanlı"

    if prob:
        kr = kural_dept(metin)
        if kr["guven"] < RULE_CONFIDENCE_THRESHOLD or kr["departman"] is None:
            br = bert_predict(metin)
            dept, guven, source = br["departman"], br["guven"], "BERT Modeli"
            if dept == "Arsiv (Olumlu)":
                prob = False
        else:
            dept, guven = kr["departman"], kr["guven"]
    else:
        dept, guven, source = "Arsiv (Olumlu)", 1.0, "VADER + Kural"

    conflict = (star or 0) >= 4 and prob

    return {
        "problem_var": prob, "vader": round(vader, 3), "prob_skor": round(ps, 2),
        "departman": dept, "guven": guven, "source": source, "conflict": conflict,
    }

# ── SIDEBAR ──
with st.sidebar:
    st.markdown(
        "<div class='logo-wrap'><div class='logo-icon'>🔍</div>"
        "<div class='logo-text'>ReviewLens</div></div>"
        "<div style='font-size:12px;color:#334155;margin-bottom:24px'>Amazon Review Intelligence</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div class='sb-section'>Navigasyon</div>", unsafe_allow_html=True)
    sayfa = st.radio("", ["Tek Yorum Analizi", "Toplu CSV Analizi", "Dashboard"], label_visibility="collapsed")

    st.markdown("<div class='sb-section'>Sistem Durumu</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='sb-status'>VADER Sentiment <span class='sb-dot-green'>● Aktif</span></div>"
        "<div class='sb-status'>Kural Motoru <span class='sb-dot-green'>● Aktif</span></div>"
        "<div class='sb-status'>DistilBERT (fallback) <span class='sb-dot-green'>● Aktif</span></div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='sb-section'>Departmanlar</div>", unsafe_allow_html=True)
    for dept, cfg in DEPT_CFG.items():
        st.markdown(
            "<div class='sb-dept-row'><span style='font-size:15px'>" + cfg["ikon"] + "</span>"
            "<span class='sb-dept-name'>" + dept + "</span>"
            "<span style='margin-left:auto;width:8px;height:8px;border-radius:50%;background:" + cfg["renk"] + ";display:inline-block;opacity:0.6'></span></div>",
            unsafe_allow_html=True
        )

# ════════════════════════════════════════════════════════════════
# SAYFA 1 — TEK YORUM ANALİZİ
# ════════════════════════════════════════════════════════════════
if sayfa == "Tek Yorum Analizi":

    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>✦ Hybrid AI Review Analysis</div>
        <h1 class='hero-title'>Yorum <span>Analiz</span> Motoru</h1>
        <p class='hero-sub'>Musteri yorumlarini hibrit yapay zeka ile saniyeler icinde analiz et.
        Kural tabanli hizli tarama, belirsiz durumlarda DistilBERT devreye girer.</p>
        <div class='hero-stats'>
            <div class='hero-stat'><div class='num'>5</div><div class='lbl'>Departman</div></div>
            <div class='hero-stat'><div class='num'>3</div><div class='lbl'>NLP Katmani</div></div>
            <div class='hero-stat'><div class='num'>~1s</div><div class='lbl'>Analiz Suresi</div></div>
            <div class='hero-stat'><div class='num'>533K</div><div class='lbl'>Egitim Verisi</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1], gap="medium")
    with col1:
        st.markdown("<div class='sec-label'>Musteri Yorumu</div>", unsafe_allow_html=True)
        metin = st.text_area("", placeholder="Yorumu buraya yapistirin...", height=180, label_visibility="collapsed")
    with col2:
        st.markdown("<div class='sec-label'>Yildiz Puani</div>", unsafe_allow_html=True)
        star = st.select_slider("", options=[1,2,3,4,5], value=3, label_visibility="collapsed")
        renk_map = {1:"#EF4444",2:"#F97316",3:"#F59E0B",4:"#84CC16",5:"#10B981"}
        lbl_map = {1:"Cok Kotu",2:"Kotu",3:"Orta",4:"Iyi",5:"Mukemmel"}
        st.markdown(
            "<div style='text-align:center;padding:12px 0'>"
            "<div style='font-size:30px;margin-bottom:6px'>" + "⭐"*star + "</div>"
            "<div style='font-size:13px;font-weight:600;color:" + renk_map[star] + ";letter-spacing:.04em'>" + lbl_map[star] + "</div></div>",
            unsafe_allow_html=True
        )
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        btn = st.button("🔍  Analiz Et", use_container_width=True, type="primary")

    if btn and metin.strip():
        with st.spinner("Analiz ediliyor..."):
            s = analiz_et(metin, star)

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        durum_cls = "red" if s["problem_var"] else "green"
        durum_txt = "⚠️  Problemli" if s["problem_var"] else "✅  Sorunsuz"
        vader_cls = "red" if s["vader"]<-0.05 else "green" if s["vader"]>0.05 else "amber"

        st.markdown(
            "<div class='res-grid fade-1'>"
            "<div class='res-card " + durum_cls + "'><span class='rc-icon'>🎯</span>"
            "<div class='rc-lbl'>Durum</div><div class='rc-val'>" + durum_txt + "</div>"
            "<div class='rc-sub'>Problem skoru: " + str(s["prob_skor"]) + "</div></div>"
            "<div class='res-card " + vader_cls + "'><span class='rc-icon'>🧠</span>"
            "<div class='rc-lbl'>Duygu Skoru (VADER)</div><div class='rc-val'>" + str(s["vader"]) + "</div>"
            "<div class='rc-sub'>-1.0 negatif &nbsp;·&nbsp; +1.0 pozitif</div></div>"
            "<div class='res-card blue'><span class='rc-icon'>⚡</span>"
            "<div class='rc-lbl'>Siniflandirma Guveni</div><div class='rc-val'>%" + str(round(s["guven"]*100)) + "</div>"
            "<div class='rc-sub'>Karar kaynagi: " + s["source"] + "</div></div></div>",
            unsafe_allow_html=True
        )

        dept = s["departman"]
        cfg = DEPT_CFG.get(dept, {"renk":"#6B7280","bg":"#1A1D27","ikon":"📋","desc":""})
        cls = "problem" if s["problem_var"] else "ok"
        guven_pct = round(s["guven"] * 100)
        pill_cls = "bert" if s["source"] == "BERT Modeli" else ""

        st.markdown(
            "<div class='dept-wrap " + cls + " fade-2'>"
            "<div class='dept-icon-wrap' style='background:" + cfg["bg"] + "'>" + cfg["ikon"] + "</div>"
            "<div class='dept-info'>"
            "<div class='dept-lbl'>Yonlendirilecek Departman <span class='source-pill " + pill_cls + "'>" + s["source"] + "</span></div>"
            "<div class='dept-name' style='color:" + cfg["renk"] + "'>" + dept + "</div>"
            "<div class='dept-desc'>" + cfg["desc"] + "</div>"
            "<div class='prog-wrap'><div class='prog-label'><span>Guven</span><span>" + str(guven_pct) + "%</span></div>"
            "<div class='prog-bar-bg'><div class='prog-bar-fill' style='width:" + str(guven_pct) + "%;background:" + cfg["renk"] + "'></div></div></div>"
            "</div><div class='dept-right'><div class='dept-pct' style='color:" + cfg["renk"] + "'>%" + str(guven_pct) + "</div>"
            "<div class='dept-pct-lbl'>Guven</div></div></div>",
            unsafe_allow_html=True
        )

        if s["conflict"]:
            st.markdown(
                "<div class='conflict-box fade-3'>⚠️ &nbsp;" + str(star) + " yildiz verilmis ama sikayet tespit edildi — review dikkatle incelenmeli.</div>",
                unsafe_allow_html=True
            )

        st.markdown(
            "<div class='info-box fade-3'>ℹ️ &nbsp;Bu analiz once <b>VADER duygu analizi + kural tabanli anahtar kelime taramasi</b> kullanir. "
            "Kural motoru net bir sonuca varamazsa (dusuk guven), <b>DistilBERT</b> (533k yorumla fine-tuned) devreye girer ve nihai karari verir.</div>",
            unsafe_allow_html=True
        )

    elif btn:
        st.warning("Lutfen bir yorum metni girin.")

# ════════════════════════════════════════════════════════════════
# SAYFA 2 — TOPLU CSV
# ════════════════════════════════════════════════════════════════
elif sayfa == "Toplu CSV Analizi":

    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>✦ Batch Processing</div>
        <h1 class='hero-title'>Toplu <span>CSV</span> Analizi</h1>
        <p class='hero-sub'>CSV yukle, tum yorumlari hibrit motorla analiz et, filtrele ve rapor olarak indir.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div class='info-box'>CSV dosyanda <b>review_body</b> sutunu olmali. <b>star_rating</b> varsa daha dogru sonuc verir.</div>",
        unsafe_allow_html=True
    )
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    yuklenen = st.file_uploader("CSV dosyasi sec", type=["csv"], label_visibility="collapsed")

    if yuklenen:
        try:
            df = pd.read_csv(yuklenen, encoding="utf-8")
        except UnicodeDecodeError:
            yuklenen.seek(0)
            df = pd.read_csv(yuklenen, encoding="latin-1")

        c1,c2,c3 = st.columns(3)
        c1.metric("Toplam Satir", f"{len(df):,}")
        c2.metric("Sutun Sayisi", str(df.shape[1]))
        c3.metric("Dosya Boyutu", f"{yuklenen.size/1024:.1f} KB")

        with st.expander("Veriyi Onizle"):
            st.dataframe(df.head(5), use_container_width=True)

        max_s = st.slider("Kac satir analiz edilsin?", 10, min(5000, len(df)), min(200, len(df)))

        if st.button("🚀  Analizi Baslat", type="primary", use_container_width=True):
            prog = st.progress(0)
            durum_el = st.empty()
            sonuclar = []
            df_a = df.head(max_s).copy()
            toplam = len(df_a)

            for i, row in enumerate(df_a.itertuples()):
                m = str(getattr(row, "review_body", getattr(row, "text", "")))
                sr = getattr(row, "star_rating", None)
                try: sr = int(sr)
                except: sr = None
                sonuclar.append(analiz_et(m, sr))
                prog.progress((i+1)/toplam)
                durum_el.markdown(
                    "<div style='font-size:12px;color:#475569'>Isleniyor: " + str(i+1) + " / " + str(toplam) + "</div>",
                    unsafe_allow_html=True
                )

            prog.empty(); durum_el.empty()
            res = pd.concat([df_a.reset_index(drop=True), pd.DataFrame(sonuclar)], axis=1)

            prob_n = int(res["problem_var"].sum())
            k1,k2,k3,k4 = st.columns(4)
            k1.metric("Analiz Edilen", str(toplam))
            k2.metric("Problemli", str(prob_n))
            k3.metric("Sorunsuz", str(toplam-prob_n))
            k4.metric("Problem Orani", "%" + str(round(prob_n/toplam*100,1)))

            cols = [c for c in ["review_body","departman","problem_var","guven","vader","source"] if c in res.columns]
            st.dataframe(res[cols], use_container_width=True, height=380)
            st.download_button(
                "⬇️  Raporu Indir (CSV)", res.to_csv(index=False).encode("utf-8"),
                "review_analiz_raporu.csv", "text/csv", use_container_width=True
            )

# ════════════════════════════════════════════════════════════════
# SAYFA 3 — DASHBOARD
# ════════════════════════════════════════════════════════════════
elif sayfa == "Dashboard":

    st.markdown("""
    <div class='hero'>
        <div class='hero-badge'>✦ Analytics Dashboard</div>
        <h1 class='hero-title'>Analitik <span>Dashboard</span></h1>
        <p class='hero-sub'>Analiz sonuclarini gorselleştir. Departman dagilimlari ve duygu analizi.</p>
    </div>
    """, unsafe_allow_html=True)

    f = st.file_uploader("Sonuc CSV yukle", type=["csv"], label_visibility="collapsed")

    if f:
        try:
            df = pd.read_csv(f, encoding="utf-8")
        except UnicodeDecodeError:
            f.seek(0)
            df = pd.read_csv(f, encoding="latin-1")

        # ÖNCEKİ HATA: bu sayfa sadece "Toplu CSV Analizi"ndan indirilmiş,
        # icinde zaten problem_var/departman sutunu olan bir rapor CSV'si bekliyordu.
        # Ham bir yorum CSV'si yuklendiginde bu sutunlar bulunamadigi icin
        # "prob = 0" varsayilana duserek dashboard hep "Problemli: 0" gosteriyordu.
        # Simdi sutunlar yoksa analiz otomatik olarak burada calistiriliyor.
        if "problem_var" not in df.columns or "departman" not in df.columns:
            metin_col = next((c for c in ["review_body", "text", "yorum", "comment"] if c in df.columns), None)
            if metin_col is None:
                st.error(
                    "Bu CSV'de hazır analiz sonucu (problem_var / departman) yok ve analiz "
                    "edilebilecek bir yorum sütunu da bulunamadı (review_body / text / yorum / comment). "
                    "Lütfen 'Toplu CSV Analizi' sayfasından indirdiğin raporu, ya da bu sütun adlarından "
                    "birini içeren ham yorum verisini yükle."
                )
                st.stop()

            max_s = min(5000, len(df))
            st.info(f"Bu CSV'de hazır analiz sonucu bulunmadığı için ilk {max_s} yorum otomatik olarak analiz ediliyor...")
            df_a = df.head(max_s).copy()
            prog = st.progress(0)
            sonuclar = []
            for i, row in enumerate(df_a.itertuples()):
                m = str(getattr(row, metin_col))
                sr = getattr(row, "star_rating", None)
                try: sr = int(sr)
                except: sr = None
                sonuclar.append(analiz_et(m, sr))
                prog.progress((i + 1) / max_s)
            prog.empty()
            df = pd.concat([df_a.reset_index(drop=True), pd.DataFrame(sonuclar)], axis=1)

        # problem_var, CSV'den "True"/"False" string, "TRUE"/"FALSE" (orn. Excel'den gecmisse) ya
        # da 1/0 olarak geri gelebilir — hepsini guvenli sekilde boolean'a ceviriyoruz, aksi halde
        # .sum() yanlis ya da sifir sonuc verip "problemler gosterilmiyor" hatasina yol acabiliyordu.
        df["problem_var"] = df["problem_var"].apply(
            lambda v: str(v).strip().lower() in ("true", "1", "1.0", "yes")
        )

        toplam = len(df)
        prob = int(df["problem_var"].sum())

        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Toplam Yorum", f"{toplam:,}")
        k2.metric("Problemli", f"{prob:,}")
        k3.metric("Sorunsuz", f"{toplam-prob:,}")
        k4.metric("Problem Orani", "%" + str(round(prob/toplam*100,1)))

        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2, gap="medium")

        with col1:
            st.markdown("<div class='sec-label'>Departman Dagilimi</div>", unsafe_allow_html=True)
            if "departman" in df.columns:
                d = df["departman"].value_counts().reset_index()
                d.columns = ["Departman","Sayi"]
                renkler = [DEPT_CFG.get(dep,{}).get("renk","#6B7280") for dep in d["Departman"]]
                fig = go.Figure(go.Bar(
                    x=d["Sayi"], y=d["Departman"], orientation="h",
                    marker=dict(color=renkler, line=dict(width=0)),
                    text=d["Sayi"], textposition="outside", textfont=dict(color="#64748B"),
                ))
                fig.update_layout(
                    template="plotly_dark", plot_bgcolor="#0D0F1A", paper_bgcolor="#0D0F1A",
                    height=320, margin=dict(l=0,r=40,t=8,b=8),
                    xaxis=dict(showgrid=False,showticklabels=False,zeroline=False),
                    yaxis=dict(showgrid=False,tickfont=dict(size=12,color="#94A3B8")),
                    showlegend=False, bargap=0.3,
                )
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("<div class='sec-label'>Problem Dagilimi</div>", unsafe_allow_html=True)
            fig2 = go.Figure(go.Pie(
                labels=["Problemli","Sorunsuz"], values=[prob, toplam-prob], hole=0.62,
                marker=dict(colors=["#EF4444","#10B981"], line=dict(color="#080A12",width=3)),
                textfont=dict(size=13, color="#94A3B8"),
            ))
            fig2.update_layout(
                template="plotly_dark", plot_bgcolor="#0D0F1A", paper_bgcolor="#0D0F1A",
                height=320, margin=dict(l=0,r=0,t=8,b=8), legend=dict(font=dict(color="#64748B")),
                annotations=[dict(text="%" + str(round(prob/toplam*100,1)), x=0.5, y=0.5,
                    font=dict(size=26, color="#F1F5F9", family="Space Grotesk"), showarrow=False)]
            )
            st.plotly_chart(fig2, use_container_width=True)

        vader_col = next((c for c in ["vader","VADER"] if c in df.columns), None)
        if vader_col:
            st.markdown("<div class='sec-label'>Duygu Skoru Dagilimi</div>", unsafe_allow_html=True)
            fig3 = go.Figure()
            fig3.add_trace(go.Histogram(x=df[vader_col], nbinsx=40, marker_color="#6366F1", marker_line=dict(width=0), opacity=0.85))
            fig3.add_vline(x=0, line_dash="dash", line_color="#F59E0B", line_width=1.5, annotation_text="Notral", annotation_font_color="#F59E0B", annotation_position="top right")
            fig3.add_vline(x=-0.05, line_dash="dot", line_color="#EF4444", line_width=1, annotation_text="Problem esigi", annotation_font_color="#EF4444", annotation_position="top left")
            fig3.update_layout(
                template="plotly_dark", plot_bgcolor="#0D0F1A", paper_bgcolor="#0D0F1A",
                height=260, margin=dict(l=0,r=0,t=16,b=8),
                xaxis=dict(title="VADER Skoru", showgrid=False, zeroline=False, color="#64748B"),
                yaxis=dict(showgrid=False, color="#64748B"), showlegend=False,
            )
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.markdown(
            "<div style='text-align:center;padding:70px 20px'>"
            "<div style='font-size:52px;margin-bottom:18px;filter:grayscale(0.3)'>📊</div>"
            "<div style='font-family:Space Grotesk;font-size:20px;font-weight:600;color:#E2E8F0;margin-bottom:8px'>Veri bekleniyor</div>"
            "<div style='font-size:14px;color:#475569;line-height:1.7'>Toplu CSV Analizi sayfasindan yorumlari analiz et,<br>indirdigin CSV'yi buraya yukle.</div></div>",
            unsafe_allow_html=True
        )