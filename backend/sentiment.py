from sentence_transformers import SentenceTransformer, util
import torch


class SentimentEngine:
    def __init__(self):
        # CPU-only inference
        print("Loading sentiment model...")
        self.model = SentenceTransformer(
            'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

        # emotion anchors
        self.anchors = {
            "happy": "Kendimi mutlu ve pozitif hissediyorum.",
            "sad": "içimde bir hüzün var, moralim bozuk.",
            "calm": "Sakin ve huzurlu hissediyorum",
            "energetic": "Enerjim yüksek ve motiveyim",
            "lonely": "Kendimi yalnız hissediyorum"
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

    def _compute_anchor_embeddings(self):
        embeddings = {}
        for emotion, text in self.anchors.items():
            embeddings[emotion] = self.model.encode(
                text, convert_to_tensor=True)
        return embeddings

    def analyze(self, user_text: str):
        # kullanici metnini embeddinge cevir
        user_embedding = self.model.encode(
            user_text, convert_to_tensor=True)

        # anchorlarla cosine similarity karsilastirmasi
        scores = {}
        for emotion, anchor_emb in self.anchor_embeddings.items():
            scores[emotion] = util.cos_sim(
                user_embedding, anchor_emb).item()

        # en yuksek skoru bul
        best_emotion = max(scores, key=scores.get)
        confidence = scores[best_emotion]

        # sonuclari valence/arousal a map et
        result = self.emotion_map[best_emotion].copy()
        result["emotion"] = best_emotion

        # confidence hesabi ( 2. en iyi ile fark veya direkt skor)
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            result["confidence"] = sorted_scores[0] - \
                sorted_scores[1]  # basit fark metrigi
        else:
            result["confidence"] = sorted_scores[0]  # tek anchor durumu
        result["provider"] = "local"

        return result
