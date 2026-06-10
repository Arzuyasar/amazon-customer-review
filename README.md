# Amazon Customer Review — Şikayet Sınıflandırma

Amazon Electronics, Mobile Electronics ve Video Games kategorilerindeki müşteri yorumlarını şikayet türüne göre sınıflandıran NLP projesi.

## Dataset

| Kategori | Satır Sayısı |
|----------|-------------|
| Electronics | ~50k |
| Mobile Electronics | ~50k |
| Video Games | ~50k |
| **Toplam** | **~150k** |

## Sınıflar

| Sınıf | Açıklama |
|-------|----------|
| `problem_yok` | Şikayet içermeyen yorum |
| `ürün_kalitesi` | Ürün kalitesiyle ilgili şikayet |
| `ürün_dayanıklılığı` | Dayanıklılık ve uzun ömürle ilgili şikayet |
| `performans` | Performans ve hızla ilgili şikayet |
| `içerik_beklenti` | İçerik veya beklenti uyuşmazlığı |

## Proje Adımları

1. **EDA** — Veri keşfi ve görselleştirme
2. **Labeling** — SentenceTransformer (all-MiniLM) ile embedding, K-Means clustering ile otomatik etiketleme
3. **Preprocessing** — Metin temizleme ve encoding
4. **Baseline Model** — TF-IDF + Logistic Regression
5. **BERT Fine-tuning** — DistilBERT ile fine-tuning

## Sonuçlar

| Model | Accuracy | Macro F1 | Not |
|-------|----------|----------|-----|
| LR (class_weight=balanced) | 0.87 | 0.56 | `problem_yok` dominant, yanıltıcı |
| DistilBERT | 0.83 | 0.83 | Tüm sınıflarda dengeli |

> Macro F1 skoruna göre DistilBERT belirgin şekilde daha iyi performans göstermektedir.

## Kurulum

```bash
git clone https://github.com/Arzuyasar/amazon-customer-review.git
cd amazon-customer-review
pip install -r requirements.txt
```

> Veriler `.gitignore` kapsamındadır. Ekip Google Drive klasöründen erişebilir.

## Branch Stratejisi

`feature/* → PR → main`
