from sentence_transformers import SentenceTransformer, util
import torch
import torch.nn.functional as F

from config import settings


class SentimentEngine:
    def __init__(self):
        # CPU-only inference
        print("Loading sentiment model...")
        self.model = SentenceTransformer(settings.sentiment_model_name)

        # emotion anchors
        # GÜNCELLENMİŞ EYLEM ODAKLI ANCHORLAR
        self.anchors = {
            "happy": "Yüzüm gülüyor, hayattan keyif alıyorum, neşeli, memnun, pozitif ve sevinçliyim",

            "sad": "İçimde derin bir hüzün var, moralim çok bozuk, ağlamaklı, kederliyim ve mutsuzum",

            "calm": "Sakinleşmek, dinlenmek, yorgunluğumu atmak, huzur bulmak, sessizlik, gevşemek, acelem yok, rahatlamak, uzanmak",

            "energetic": "Enerji doluyum, yerimde duramıyorum, dans etmek, koşmak, zıplamak, çok hareketliyim, tempo istiyorum, modum yüksek, fişek gibiyim",

            "lonely": "Kimsesizim, terk edilmiş gibi hissediyorum, yanımda birini arıyorum ama yok, dışlanmışım, yalnızım"
        }

        # Emotion Mapping (Valence/Arousal)
        self.emotion_map = {
            "happy": {"valence": 0.8, "arousal": 0.6},
            "sad": {"valence": -0.7, "arousal": 0.3},
            "calm": {"valence": 0.2, "arousal": 0.2},
            "energetic": {"valence": 0.6, "arousal": 0.9},
            "lonely": {"valence": -0.6, "arousal": 0.4}
        }

        # anchorlarin embeddinglerini onceden hesapla
        self.anchor_embeddings = self._compute_anchor_embeddings()
        print("Model ve anchorlar hazir")

    def _is_repetitive(self, text: str) -> bool:
        # Basit tekrar kontrolü: Metindeki karakterlerin %80'inden fazlası aynı mı?
        if len(text) == 0:
            return False
        most_common_char = max(set(text), key=text.count)
        repetition_ratio = text.count(most_common_char) / len(text)
        return repetition_ratio > 0.4

    def _compute_anchor_embeddings(self):
        embeddings = {}
        for emotion, text in self.anchors.items():
            embeddings[emotion] = self.model.encode(
                text, convert_to_tensor=True)
        return embeddings

    def analyze(self, user_text: str):
        # Tekrarlayan metin kontrolü
        if self._is_repetitive(user_text):
            return {
                "valence": 0.0,
                "arousal": 0.0,
                "confidence": 1.0,
                "emotion": "neutral",
                "provider": "local"
            }

        # 1. Kullanıcı metnini embedding'e çevir
        user_embedding = self.model.encode(user_text, convert_to_tensor=True)

        # 2. Skorları topla (Raw Scores)
        raw_scores = {}
        for emotion, anchor_emb in self.anchor_embeddings.items():
            # Cosine Similarity (-1 ile 1 arası değer üretir)
            raw_scores[emotion] = util.cos_sim(
                user_embedding, anchor_emb).item()

        # 3. SOFTMAX UYGULAMA (Skorları %'ye çevirme)
        # Tensor'a çeviriyoruz
        score_values = torch.tensor(list(raw_scores.values()))

        # Temperature Scaling: Skorlar birbirine çok yakınsa farkı açmak için
        # değerleri bir katsayı ile çarpıyoruz (örn: 10).
        # Bu, kazananı daha belirgin yapar.
        probabilities = F.softmax(score_values * 10, dim=0)

        # Duyguları ve yeni yüzdeleri eşleştir
        emotions = list(raw_scores.keys())
        prob_dict = {emotions[i]: probabilities[i].item()
                     for i in range(len(emotions))}

        # En yüksek skoru bul
        best_emotion = max(prob_dict, key=prob_dict.get)
        confidence = prob_dict[best_emotion]

        # 4. Sonuçları Valence/Arousal'a map et
        result = self.emotion_map[best_emotion].copy()
        result["emotion"] = best_emotion
        result["confidence"] = confidence  # Artık 0.0 ile 1.0 arası bir yüzde
        result["provider"] = "local"

        return result
