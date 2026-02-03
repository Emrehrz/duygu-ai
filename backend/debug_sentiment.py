from sentiment import SentimentEngine
import torch


def debug_text():
    print("Model yükleniyor...")
    engine = SentimentEngine()

    # Sorunlu metin
    text = "Dün gece hiç uyumadım, şu an uykum açılsın diye çok hareketli bir şeyler dinleyip dans etmek istiyorum."

    print(f"\nAnaliz Edilen Metin: '{text}'\n")
    print("-" * 50)
    print(f"{'DUYGU':<15} | {'SKOR (Benzerlik)':<20}")
    print("-" * 50)

    # 1. Kullanıcı metnini vektöre çevir
    user_embedding = engine.model.encode(text, convert_to_tensor=True)

    # 2. Tüm anchor'larla karşılaştır ve skorları yazdır
    scores = {}
    for emotion, anchor_emb in engine.anchor_embeddings.items():
        # Cosine Similarity
        score = torch.nn.functional.cosine_similarity(
            user_embedding, anchor_emb, dim=0).item()
        scores[emotion] = score
        print(f"{emotion.upper():<15} | {score:.4f}")

    print("-" * 50)
    best_emotion = max(scores, key=scores.get)
    print(f"SONUÇ: Model '{best_emotion.upper()}' seçti.")

    # İyileştirme Tavsiyesi
    if best_emotion == "calm" and scores.get("energetic", 0) < scores["calm"]:
        print("\nANALİZ: 'Uyku' kelimeleri modeli Calm tarafına çekiyor.")
        print(
            "ÇÖZÜM: Energetic anchor'ına 'uykusuzluk', 'uyanmak' gibi kelimeler eklenmeli.")


if __name__ == "__main__":
    debug_text()
