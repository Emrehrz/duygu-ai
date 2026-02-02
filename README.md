# Duygu AI

An AI-powered chat application demo with a React frontend and FastAPI backend.

## 🚀 Features

- 💬 Real-time chat interface
- 🎨 Modern, responsive UI design
- 🤖 AI-powered responses
- ⚡ Fast and efficient
- 📱 Mobile-friendly

## 🛠️ Tech Stack

**Frontend:**
- React 18
- Vite
- Modern CSS with animations

**Backend:**
- FastAPI
- Python 3.8+
- Uvicorn

## 📦 Installation & Setup

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
python main.py
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 🎯 Usage

1. Start the backend server first (on port 8000)
2. Start the frontend development server (on port 5173)
3. Open your browser and navigate to `http://localhost:5173`
4. Start chatting with Duygu AI!

## 📚 API Documentation

Once the backend is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🏗️ Project Structure

```
duygu-ai/
├── backend/
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Python dependencies
│   └── README.md         # Backend documentation
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main chat component
│   │   ├── App.css       # Styles
│   │   └── main.jsx      # Entry point
│   ├── package.json      # Node dependencies
│   └── README.md         # Frontend documentation
└── README.md             # This file
```

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📝 License

MIT
