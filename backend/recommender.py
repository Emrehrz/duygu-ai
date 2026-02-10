import json
import random
import os
import math

from config import settings


class RecommendationEngine:
    def __init__(self, data_path: str | None = None):
        path = data_path or settings.songs_path
        print("Loading recommendation catalog... ", path)
        # JSON dosyasını yükle
        with open(path, "r", encoding="utf-8") as f:
            self.catalog = json.load(f)

    def recommend(self, target_valence: float, target_arousal: float, limit=5):
        scored_songs = []

        for song in self.catalog:
            s_valence = song["valence"]
            s_energy = song["energy"]
            # Tempo verisi yoksa medium varsay
            s_tempo = song.get("tempo", "medium").lower()

            # 1. ÖKLİD MESAFESİ (Temel Benzerlik)
            distance = math.sqrt(
                ((s_valence - target_valence) ** 2) +
                ((s_energy - target_arousal) ** 2)
            )
            similarity = 1 / (1 + distance)

            # --- KURAL 1: DUYGU YÖNÜ KONTROLÜ (Mood Consistency) ---
            # Kullanıcı Mutlu (Valence > 0.5) ama Şarkı Negatif/Karanlık (Valence < 0.4)
            # Örnek: "Od" şarkısı (V:0.3) burada yakalanıp cezalandırılacak.
            if target_valence > 0.5 and s_valence < 0.4:
                similarity *= 0.5  # Skoru yarıya indir (Büyük Ceza)

            # Kullanıcı Üzgün (Valence < -0.2) ama Şarkı Çok Neşeli (Valence > 0.2)
            if target_valence < -0.2 and s_valence > 0.2:
                similarity *= 0.6

            # --- KURAL 2: TEMPO UYUMU (Tempo Matching) ---
            # Yüksek Enerji / Mutlu Mod -> Hızlı Tempo İster
            if target_arousal > 0.6:
                if s_tempo == "high":
                    similarity *= 1.15  # %15 Bonus (Ödül)
                elif s_tempo == "low":
                    similarity *= 0.7  # %30 Ceza

            # Düşük Enerji / Sakin Mod -> Yavaş Tempo İster
            elif target_arousal < 0.4:
                if s_tempo == "low":
                    similarity *= 1.15  # Ödül
                elif s_tempo == "high":
                    similarity *= 0.7  # Ceza

            song_with_score = song.copy()
            song_with_score["score"] = similarity
            scored_songs.append(song_with_score)

        # Skora göre büyükten küçüğe sırala
        scored_songs.sort(key=lambda x: x["score"], reverse=True)

        # 3. Çeşitlilik Kuralları (Diversity)
        final_list = []
        artist_counts = {}
        genre_counts = {}

        # En iyi 30 şarkı arasından seçim yap (Havuzu genişlettik)
        candidates = scored_songs[:30]

        for song in candidates:
            artist = song["artist"]
            genre = song["genre"]

            # Max 1 şarkı/sanatçı, Max 2 şarkı/tür
            if artist_counts.get(artist, 0) >= 1:
                continue
            if genre_counts.get(genre, 0) >= 2:
                continue

            final_list.append(song)
            artist_counts[artist] = artist_counts.get(artist, 0) + 1
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

            if len(final_list) >= limit:
                break

        # Eğer filtreler yüzünden liste dolmadıysa, kalanlardan rastgele ekle
        if len(final_list) < limit:
            remaining = [s for s in candidates if s not in final_list]
            needed = limit - len(final_list)
            final_list.extend(remaining[:needed])

        return final_list
