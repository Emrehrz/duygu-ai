# Duygu AI

Duygu AI, React tabanlı bir frontend ve FastAPI tabanlı bir backend kullanan, uçtan uca bir yapay zeka sohbet uygulaması örneğidir. Amaç; modern bir UI ile API tabanlı bir AI servisinin entegrasyonunu göstermektir.

## 🚀 Özellikler

- 💬 Gerçek zamanlıya yakın sohbet arayüzü
- 🎨 Modern ve responsive arayüz (desktop & mobile)
- 🤖 Backend üzerinden AI destekli cevap üretimi
- ⚡ Hızlı geliştirme ortamı (Vite + FastAPI + Uvicorn)
- 📡 HTTP API üzerinden ayrık frontend/backend mimarisi

## 🛠️ Teknoloji Yığını

**Frontend**
- React 18
- Vite
- Modern CSS / animasyonlu arayüz

**Backend**
- FastAPI
- Python 3.8+
- Uvicorn

## 🧱 Mimari Genel Bakış

- Frontend, tarayıcıda çalışan tek sayfa uygulamasıdır (SPA).
- Backend, JSON tabanlı HTTP API sağlar (FastAPI).
- Frontend, kullanıcı mesajlarını backend'e gönderir; backend bu mesajları işler ve AI cevabını geri döndürür.
- Geliştirme sırasında servisler ayrı portlarda çalışır:
  - Backend: `http://localhost:8000`
  - Frontend: `http://localhost:5173`

## 📦 Kurulum ve Çalıştırma

Aşağıdaki adımlar proje kök dizininde (`duygu-ai/`) çalıştırılmak üzere tasarlanmıştır.

### 1. Backend Kurulumu

1. Backend dizinine geçin:

```bash
cd backend
```

2. Sanal ortam oluşturun ve aktifleştirin:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Python bağımlılıklarını yükleyin:

```bash
pip install -r requirements.txt
```

4. Backend sunucusunu başlatın:

```bash
python main.py
# veya proje içinde tanımlı ise:
# uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend API şu adreste çalışıyor olacaktır: `http://localhost:8000`.

### 2. Frontend Kurulumu

1. Yeni bir terminal açın ve proje köküne dönün, ardından frontend dizinine geçin:

```bash
cd frontend
```

2. Node bağımlılıklarını yükleyin:

```bash
npm install
```

3. Geliştirme sunucusunu çalıştırın:

```bash
npm run dev
```

Frontend geliştirme sunucusu şu adreste çalışıyor olacaktır: `http://localhost:5173`.

## 🎯 Kullanım

1. Backend'i `http://localhost:8000` üzerinde çalışır halde tutun.
2. Frontend geliştirme sunucusunu `http://localhost:5173` üzerinde başlatın.
3. Tarayıcınızdan `http://localhost:5173` adresine gidin.
4. Mesajınızı yazıp gönderin; yanıtlar backend üzerinden AI modeli/servisinden alınır.

## ⚙️ Yapılandırma ve Ortam Değişkenleri

Backend ve frontend tarafında, kullanmak istediğiniz AI servislerine göre bazı ortam değişkenleri gerekebilir (ör. bir LLM API anahtarı, base URL vb.).

Örnek yaklaşım (öneri):

- Backend: `.env` dosyasında
  - `AI_API_KEY=...`
  - `AI_API_BASE_URL=...`
- Frontend: `.env` dosyasında
  - `VITE_API_BASE_URL=http://localhost:8000`

Gerçek projede kullandığınız değişkenleri backend ve frontend README dosyalarında daha detaylı tanımlayabilirsiniz.

## 📚 API Dokümantasyonu

Backend çalışır durumda iken aşağıdaki uç noktalardan otomatik üretilen API dokümantasyonuna erişebilirsiniz:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Sohbet uç noktaları (endpoint) ve istek/yanıt şemaları burada ayrıntılı olarak görüntülenebilir.

## 🏗️ Proje Dizini

```ini
duygu-ai/
├── backend/
│   ├── main.py           # FastAPI uygulaması, API uç noktaları
│   ├── requirements.txt  # Python bağımlılıkları
│   └── README.md         # Backend'e özel dokümantasyon (ayrıntılı ayarlar, endpoint'ler vb.)
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Ana sohbet bileşeni
│   │   ├── App.css       # Stil ve animasyonlar
│   │   └── main.jsx      # Uygulama giriş noktası
│   ├── package.json      # Node bağımlılıkları ve script'ler
│   └── README.md         # Frontend'e özel dokümantasyon (bileşen yapısı, theming vb.)
└── README.md             # Projenin genel dokümantasyonu (bu dosya)
```

## 🧪 Geliştirme ve Test

- Backend için isteğe bağlı olarak pytest veya FastAPI test araçları ile testler ekleyebilirsiniz.
- Frontend için React Testing Library veya Vitest/Jest kullanılabilir.
- Lint araçları (ör. `flake8`, `black`, `eslint`, `prettier`) entegre edilerek kod kalitesi artırılabilir.

## 🚢 Dağıtım (Deployment)

Projeyi production ortamına almak için tipik yaklaşımlar:

- Backend için:
  - Uvicorn/Gunicorn ile FastAPI uygulamasını bir reverse proxy (NGINX vb.) arkasında çalıştırmak
- Frontend için:
  - `npm run build` ile statik dosyaları üretmek
  - Üretilen build çıktısını bir statik dosya sunucusunda (NGINX, CDN, vb.) barındırmak

Detaylı deployment adımlarını kendi hedef ortamınıza göre backend ve frontend README dosyalarında özelleştirebilirsiniz.

## 🤝 Katkıda Bulunma

Katkılarınızı memnuniyetle karşılıyoruz. Önerilen süreç:

1. Bir issue açarak geliştirme/iyileştirme fikrinizi tartışın.
2. Yeni bir branch açın (örn. `feature/improve-ui`, `fix/api-timeout`).
3. Değişiklikleri yapın ve uygun ise testleri ekleyin/güncelleyin.
4. Açıklayıcı bir açıklama ile pull request gönderin.

## 📝 Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Ayrıntılar için `LICENSE` dosyasına veya alt projelerde belirtilen lisans bilgilerine bakabilirsiniz.