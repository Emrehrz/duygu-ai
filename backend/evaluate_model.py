from sentiment import SentimentEngine
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

# test veri seti (golden dataset)
# dogru kabul edilen veriler
# farkli zorluk seviyerinde ornekler ekleyelim

test_data = [
    # HAPPY
    ("Bugün harika bir gün, içim kıpır kıpır", "happy"),
    ("Sınavdan yüz aldım çok sevinçliyim", "happy"),
    ("Güneş açtı, modum yerine geldi", "happy"),

    # SAD
    ("Hiçbir şey yapmak istemiyorum, çok mutsuzum", "sad"),
    ("Kalbim kırık, ağlamak istiyorum", "sad"),
    ("Haberlere baktıkça moralim bozuluyor", "sad"),

    # CALM
    ("Kahvemi aldım, sessizliğin tadını çıkarıyorum", "calm"),
    ("Şu an her şey yolunda, acelem yok", "calm"),
    ("Deniz kenarında oturup dalgaları izliyorum", "calm"),

    # ENERGETIC
    ("Koşuya çıkmak için sabırsızlanıyorum", "energetic"),
    ("Yerimde duramıyorum, dans etmek istiyorum", "energetic"),
    ("Bu işi bitirmek için tam gaz çalışıyorum", "energetic"),

    # LONELY
    ("Evde tek başınayım, kimse beni aramıyor", "lonely"),
    ("Kalabalıklar içinde yapayalnız hissediyorum", "lonely"),
    ("Keşke yanımda konuşacak biri olsa", "lonely"),

    # ZORLAYICI / KARIŞIK ÖRNEKLER (Edge Cases)
    # Negatif kelime var ama anlam pozitif
    ("Bugün hava biraz kapalı ama ben iyiyim", "calm"),
    ("Çok yorgunum ama spor yapmam lazım", "energetic"),  # Yorgunluk vs Enerji
    # Yalnız kelimesi var ama duygu Calm
    ("Yalnız kalmak bazen huzur veriyor", "calm"),
]


def run_evaluation():
    print("Evaluating Sentiment Engine...")
    engine = SentimentEngine()

    print(
        f"\nToplam {len(test_data)} test örneği üzerinde değerlendirme yapılıyor...\n")

    y_true = []  # olması gerekenler
    y_pred = []  # modelin tahminleri
    errors = []  # hatali tahminler

    for text, expected in test_data:
        # modeli calistir
        result = engine.analyze(text)
        predicted = result["emotion"]
        confidence = result["confidence"]

        y_true.append(expected)
        y_pred.append(predicted)

        # hata varsa kaydet
        if predicted != expected:
            errors.append({
                "text": text,
                "expected": expected,
                "predicted": predicted,
                "confidence": round(confidence, 2)
            })

        # ----- sonuc raporu ----
        print("-" * 50)
        print("Test sonuclari")
        print("-" * 50)

        # sklearn ile detayli rapor ( precision, recall, f1-score)
        # zero_division parametresi uyarilari engeller
        report = classification_report(y_true, y_pred, zero_division=0)
        print(report)

        # hata analizi
        if errors:
            print("\nHATALI TAHMİNLER (Nerelerde yanıldık?):")
            for err in errors:
                print(f"❌ Metin: '{err['text']}'")
                print(
                    f"   Beklenen: {err['expected']} | Tahmin: {err['predicted']} (Güven: {err['confidence']})")
                print("-" * 30)

        else:
            print("\n✅ TEBRİKLER! Tüm testleri başarıyla geçtin.")


if __name__ == "__main__":
    run_evaluation()
