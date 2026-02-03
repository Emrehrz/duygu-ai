import json
import random
import os


class RecommendationEngine:
    def __init__(self, data_path="data/songs.json"):
        print("Loading recommendation catalog... ", data_path)
        # JSON dosyasını yükle
        with open(data_path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def recommend(self, target_valence: float, target_arousal: float, limit=5):
        scored_songs = []

        for song in self.catalog:
            # 1. Ranking Formula
            # score = 0.45 * (1 - |s.v - u.v|) + 0.35 * (1 - |s.e - u.a|) ...

            valence_dist = abs(song["valence"] - target_valence)
            energy_dist = abs(song["energy"] - target_arousal)

            # Diversity penalty MVP'de basit tutulabilir veya şimdilik 0 kabul edilebilir.
            # Formülün ana kısmını uygulayalım:
            score = (0.45 * (1 - valence_dist)) + (0.35 * (1 - energy_dist))

            # Şarkı objesine skoru ekle (orijinal veriyi bozmadan)
            song_with_score = song.copy()
            song_with_score["score"] = round(score, 2)
            scored_songs.append(song_with_score)

        # Skora göre büyükten küçüğe sırala
        scored_songs.sort(key=lambda x: x["score"], reverse=True)

        # 2. Diversity Rules (Filtreleme)
        # Max 1 song per artist, Max 2 songs per genre
        final_list = []
        artist_counts = {}
        genre_counts = {}

        # Top 10-20 aday arasından filtreleyerek seçelim
        # Hepsine bakıyoruz çünkü katalog küçük
        candidates = scored_songs

        for song in candidates:
            artist = song["artist"]
            genre = song["genre"]

            # Kurallar
            if artist_counts.get(artist, 0) >= 1:
                continue
            if genre_counts.get(genre, 0) >= 2:
                continue

            # Ekle
            final_list.append(song)
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

            # Yeterli sayıya ulaştıysak dur (Top 10 aday havuzu oluşturuyoruz önce)
            if len(final_list) >= 10:
                break

        # 3. Final Selection: Random 5 from top candidates
        # Eğer liste 5'ten kısaysa hepsini döndür
        if len(final_list) > limit:
            return random.sample(final_list, limit)
        return final_list
