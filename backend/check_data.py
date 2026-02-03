import json
import matplotlib.pyplot as plt


def visualize_songs():
    with open('data/songs.json', 'r', encoding='utf-8') as f:
        songs = json.load(f)

    valences = [s['valence'] for s in songs]
    energies = [s['energy'] for s in songs]
    titles = [s['title'] for s in songs]

    plt.figure(figsize=(10, 8))

    # Eksenleri çiz
    plt.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
    plt.axvline(0, color='gray', linestyle='--', alpha=0.5)

    # Şarkıları nokta olarak koy
    plt.scatter(valences, energies, c='blue', alpha=0.6)

    # İsimleri yaz
    for i, title in enumerate(titles):
        plt.annotate(title, (valences[i], energies[i]), fontsize=8)

    plt.title("Şarkı Kataloğu Dağılımı")
    plt.xlabel("Valence (Negatif <-> Pozitif)")
    plt.ylabel("Energy (Düşük <-> Yüksek)")
    plt.grid(True, alpha=0.3)

    # Bölgeleri etiketle
    plt.text(0.8, 0.9, "MUTLU/COŞKULU", color='green', fontweight='bold')
    plt.text(-0.8, 0.9, "ÖFKELİ/GERGİN", color='red', fontweight='bold')
    plt.text(-0.8, 0.1, "ÜZGÜN/DEPRESİF", color='blue', fontweight='bold')
    plt.text(0.8, 0.1, "SAKİN/HUZURLU", color='orange', fontweight='bold')

    plt.xlim(-1.1, 1.1)
    plt.ylim(0, 1.1)
    # plt.show()
    plt.savefig("songs_catalog.png")  # Grafiği dosyaya kaydet


if __name__ == "__main__":
    try:
        visualize_songs()
    except ImportError:
        print("Matplotlib yüklü değil. 'pip install matplotlib' çalıştırın.")
