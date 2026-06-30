<div align="center">

# ReviewLens

### Amazon Müşteri Yorumları İçin Hibrit Yapay Zeka Sınıflandırma Sistemi

[![Canlı Demo](https://img.shields.io/badge/🚀_Canlı_Demo-Streamlit-1D9E75?style=for-the-badge)](https://amazon-customer-review-hibrit.streamlit.app)
[![HuggingFace](https://img.shields.io/badge/🤗_Model-HuggingFace-FFD21E?style=for-the-badge)](https://huggingface.co/arcasoyece/amazon-review-classifier)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

*Bir müşteri yorumunun şikayet içerip içermediğini tespit eder — içeriyorsa ilgili departmana otomatik olarak yönlendirir.*

</div>

---

## Ne Yapıyor?

ReviewLens iki aşamalı bir problemi çözüyor:

1. **Problem var mı?** — Her yorumu problemli / problemsiz olarak sınıflandır
2. **Hangi departman?** — Şikayeti doğru ekibe yönlendir (Teknik Destek, Lojistik, Ürün Yönetimi vb.)

---

## Mimari — 3 Paralel Modül

### Modül 1 — TF-IDF + Klasik Makine Öğrenmesi (Baseline)

> Hızlı ve yorumlanabilir bir baseline oluşturmak için anahtar kelime tabanlı sınıflandırma.

- **200.000 yorum** 3 ürün kategorisinden örneklendi
- Etiket kuralı: `star_rating ≤ 3` → problemli, `4–5` → problemsiz
- `TfidfVectorizer(max_features=5000, ngram_range=(1,2))`
- 5 model karşılaştırıldı:

| Model | Accuracy | Macro F1 | Problem Recall |
|-------|----------|----------|----------------|
| **Logistic Regression** ✅ | 0.87 | 0.84 | **0.85** |
| Naive Bayes | 0.86 | 0.79 | 0.53 |
| Linear SVM | 0.89 | 0.85 | 0.72 |
| Random Forest | 0.87 | 0.82 | 0.62 |
| XGBoost | 0.88 | 0.82 | 0.62 |

> **Logistic Regression seçildi** — en yüksek Problem Recall değeriyle gerçek şikayetleri en az kaçıran model.

---

### Modül 2 — Anlamsal Etiketleme + DistilBERT (Derin Öğrenme)

> Manuel etiketleme yapılmadan 7 şikayet kategorisinde fine-tune edilmiş transformer modeli.

**Etiketleme pipeline'ı (533K satır, sıfır manuel etiket):**

```
SentenceTransformer(all-MiniLM-L6-v2)
        ↓
    PCA(n=50)
        ↓
MiniBatchKMeans(k=7)
        ↓
  Keyword düzeltmesi
        ↓
  labeled_data.csv
```

**7 Kategori:**

| Kategori | Satır Sayısı | Departman |
|----------|-------------|-----------|
| `problem_yok` | 376.495 | Arşiv |
| `teknik_sorun` | 87.295 | Teknik Destek |
| `urun_kalitesi` | 56.938 | Kalite Kontrol |
| `kargo_teslimat` | 6.303 | Lojistik |
| `urun_dayaniklilik` | 3.120 | Ürün Geliştirme |
| `satici` | 2.883 | Satıcı İlişkileri |
| `icerik_beklenti` | 646 | Pazarlama |

**DistilBERT v2 sonuçları (fine-tuned, class-weighted):**

| Metrik | Skor |
|--------|------|
| Doğruluk | **%92** (0.917) |
| Macro F1 | 0.84 |
| ROC-AUC | 0.954 |

```
Model: arcasoyece/amazon-review-classifier (HuggingFace Hub)
```

---

### Modül 3 — VADER + Kural Motoru (Gerçek Zamanlı Yönlendirme)

> Gerçek zamanlı duygu analizi ve departman yönlendirmesi için hızlı 3 katmanlı pipeline.

```
Müşteri Yorumu
      ↓
  VADER Duygu Skoru  (-1.0 → +1.0)
      ↓
  Keyword Kuralları  →  Departman Ataması + Güven Skoru
      ↓  (güven < 0.45 ise)
  Zero-shot Fallback  (facebook/bart-large-mnli)
      ↓
  Departman Yönlendirmesi
```

**VADER istatistikleri (n=200.000):** ortalama=0.468 · std=0.513 · medyan=0.659

**Şikayet dağılımı (50.022 problemli yorum):**

| Departman | Yorum Sayısı |
|-----------|-------------|
| Genel Şikayet | 21.039 |
| Yazılım Ekibi | 12.373 |
| Ürün Yönetimi | 6.797 |
| Teknik Destek | 6.111 |
| Lojistik | 1.910 |
| Müşteri Hizmetleri | 1.792 |

**Binary problem tespitinde model karşılaştırması:**

| Model | ROC-AUC | Doğruluk |
|-------|---------|----------|
| **DistilBERT** ✅ | **0.954** | %90.9 |
| Logistic Regression | 0.938 | %89.1 |

---

## Hibrit Sistem — Canlı Uygulama

> Modül 2 + Modül 3'ü tek bir production pipeline'ında birleştiriyor.

```
Kural motoru trafiğin ~%75'ini anında işler.
DistilBERT yalnızca düşük güvenli durumlarda devreye girer.
```

**Neden hibrit?**

| | Sadece Kural | Sadece BERT | Hibrit ✅ |
|--|-----------|-----------|-----------|
| Hız | ✅ Hızlı | ❌ Yavaş | ✅ Hızlı |
| Nüans | ❌ Sınırlı | ✅ Derin | ✅ Derin |
| Yorumlanabilirlik | ✅ Şeffaf | ❌ Kara kutu | ✅ Şeffaf |
| GPU maliyeti | ✅ Yok | ❌ Her istek | ✅ Sadece gerektiğinde |

---

## Canlı Uygulama

🔗 **[amazon-customer-review-hibrit.streamlit.app](https://amazon-customer-review-hibrit.streamlit.app)**

Özellikler:
- Tek yorum analizi (metin + yıldız puanı → departman + güven skoru + karar kaynağı)
- Toplu CSV yükleme ve analiz
- Departman dağılım grafikleriyle dashboard

---

## Teknoloji Yığını

| Katman | Araçlar |
|--------|---------|
| NLP / ML | HuggingFace Transformers, DistilBERT, VADER, SentenceTransformers, scikit-learn, XGBoost |
| Zero-shot | facebook/bart-large-mnli |
| Veri | pandas, NumPy, MiniBatchKMeans, PCA |
| Eğitim | Google Colab (GPU), class-weighted loss |
| Deployment | Streamlit Cloud, HuggingFace Hub, GitHub |

---

## Kurulum

```bash
git clone https://github.com/Arzuyasar/amazon-customer-review.git
cd amazon-customer-review
pip install -r requirements.txt
streamlit run reviewlens_hybrid.py
```

> **Veri:** Ham CSV dosyaları repoya dahil değildir (`.gitignore`). Paylaşılan Google Drive klasöründen indirilebilir.

---

## Proje Yapısı

```
amazon-customer-review/
├── reviewlens_hybrid.py        # Ana Streamlit uygulaması (hibrit sistem)
├── notebooks/
│   ├── relabeling.ipynb        # Etiketleme pipeline'ı (Modül 2)
│   └── bert_finetuning.ipynb   # DistilBERT eğitimi (v1 → v2)
├── data/
│   └── labeled_data_full.csv   # 533K etiketli satır
├── model/
│   ├── model.pkl               # Logistic Regression (Modül 1)
│   └── vectorizer.pkl          # TF-IDF vektörleştirici
└── requirements.txt
```

---

<div align="center">

Grup NLP Projesi — 2024/2025

</div>
