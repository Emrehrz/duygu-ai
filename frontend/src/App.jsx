import { useState, useRef, useEffect } from 'react';
import './App.css';
import { analyzeMessage } from './api/analyze';
import { getRecommendations } from './api/recommender';
import Particles from './components/Particles';

const isNetworkRelatedError = (error) => {
  if (!error) return false;
  if (error.code === 'SERVICE_UNAVAILABLE' || error.code === 'ECONNREFUSED') return true;
  if (error.name === 'TypeError') return true;
  const message = typeof error === 'string'
    ? error
    : (error.message || error.detail || '');
  if (typeof message !== 'string') return false;
  const lowerMsg = message.toLowerCase();
  return lowerMsg.includes('failed to fetch') ||
    lowerMsg.includes('networkerror') ||
    lowerMsg.includes('network request failed') ||
    lowerMsg.includes('connection refused') ||
    lowerMsg.includes('econnrefused');
};

// Yardımcı Bileşen: Track Card
const TrackCard = ({ track }) => (
  <div className="track-card">
    <div className="track-icon">🎵</div>
    <div className="track-info">
      <h4>{track.title}</h4>
      <p>{track.artist}</p>
    </div>
    <a className="track-link" href={track.youtube_url} target="_blank" rel="noopener noreferrer">
      ▶
    </a>
  </div>
);

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [inputError, setInputError] = useState(''); // Yeni state: input hatası
  const [isLoading, setIsLoading] = useState(false);
  const [hasStarted, setHasStarted] = useState(false); // UI Durumu
  const [isServiceUnavailable, setIsServiceUnavailable] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  const translateEmotion = (emotion) => {
    const translations = {
      happy: "mutlu",
      sad: "üzgün",
      calm: "sakin",
      energetic: "enerjik",
      lonely: "yalnız"
    };
    return translations[emotion] || emotion;
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async (e) => {
    e.preventDefault();
    const trimmed = input.trim();
    if (!trimmed || isLoading) return;

    // uzunluk kontrolü
    if (trimmed.length < 5) {
      setInputError('Az bir şey daha uzun olsun (min 5 karakter).');
      return;
    }
    if (trimmed.length > 80) {
      setInputError('Bence bir cümle için 80 karakter yeterli.');
      return;
    }
    if (!trimmed || isLoading) return;

    setInputError(''); // valid ise hatayı temizle
    setIsServiceUnavailable(false); // yeni denemede servis durumunu sıfırla

    // İlk mesaj atıldığında UI değişsin
    if (!hasStarted) setHasStarted(true);

    const userContent = input.trim();
    const userMessage = {
      role: 'user',
      type: 'text',
      content: userContent,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // 1. Analiz
      const analysisData = await analyzeMessage(userContent, messages);

      // Rate Limit Kontrolü: Backend'den hata objesi döndüyse yakala
      if (analysisData.error && analysisData.error.code === "RATE_LIMITED") {
        setMessages(prev => [...prev, {
          role: 'assistant',
          type: 'text',
          content: analysisData.error.detail,
          timestamp: new Date().toISOString()
        }]);
        return; // Akışı durdur (öneri yapmaya çalışma)
      }

      const assistantAnalysisMsg = {
        role: 'assistant',
        type: 'text',
        content: `Sizi ${translateEmotion(analysisData.data.emotion)} hissettiren bir durum sezdim. (Güven: %${Math.round(analysisData.data.confidence * 100)})`,
        timestamp: new Date().toISOString()
      };

           // tekrarlayan text ise donen mesaj net olsun ve oneri yapmasin
      if(analysisData.confidence ==1){
        const repeatMsg = {
          role: 'assistant',
          type: 'text',
          content: `Kendinizi ifade etme şekliniz bu mu gerçekten?`,
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, repeatMsg]);
        return; // öneri yapmadan çık
      }

      if(isServiceUnavailable){
        setMessages(prev => [...prev, {
          role: 'assistant',
          type: 'text',
          content: 'Şu an analiz servisine bağlanamıyorum, öneri yapamayacağım. Lütfen daha sonra tekrar deneyin.',
          timestamp: new Date().toISOString()
        }]);
        return; // öneri yapmadan çık
      }
      
      setMessages(prev => [...prev, assistantAnalysisMsg]);

      // 2. Öneri
      const recommendRequest = { valence: analysisData.data.valence, arousal: analysisData.data.arousal };
      const recommendation = await getRecommendations(recommendRequest);

      const playlistMsg = {
        role: 'assistant',
        type: 'playlist',
        tracks: recommendation.tracks,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, playlistMsg]);

    } catch (error) {
      
      if (isNetworkRelatedError(error)) {
        setIsServiceUnavailable(true);
        setMessages(prev => [...prev, {
          role: 'assistant',
          type: 'error',
          content: ' Demo geçici olarak durdurulmuştur. Ancak projenin tüm kodları ve nasıl çalıştığı açık kaynaklı olarak githubta!',
          link:"https://github.com/Emrehrz/duygu-ai",
          timestamp: new Date().toISOString()
        }]);
        return; 
      }

      const fallback =
        (typeof error === 'string' && error) ||
        error?.detail ||
        error?.message ||
        'Şu an bir sorun var, tekrar dener misin?';

      setMessages(prev => [...prev, {
        role: 'assistant',
        type: 'text',
        content: fallback,
        timestamp: new Date().toISOString()
      }]);
    }finally {
      setIsLoading(false);
    }
  }

  return (
      <div className={`app ${hasStarted ? 'chat-active' : ''}`} >
        
        {/* 1. Arka Plan: App div'inin içinde ama CSS ile fixed yaptık */}
        <div style={{ width: '100%', height: '100%', position: 'fixed', inset: 0, zIndex:10}}>

            <Particles
            particleCount={200}
            particleSpread={10}
            speed={0.1}
            particleBaseSize={100}
            moveParticlesOnHover={false}
            alphaParticles={false}
            disableRotation={false}
            pixelRatio={1}
        />
        </div>
        
        {/* 2. Ana İçerik Alanı (Z-Index: 11) */}
        <div className="content-wrapper">
          
          {/* Karşılama Ekranı */}
          <div className="welcome-container">
            <h1 className="logo">Duygu AI</h1>
            <p className="subtitle">Tek cümleyle nasıl hissettiğini anlat. Sana playlist hazırlayayım.</p>
          </div>

          {/* Mesaj Listesi */}
          <div className="messages-container">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                {/* <div className="avatar">
                  {msg.role === 'user' ? 'U' : 'AI'}
                </div> */}
                <div className="message-content">
                  {msg.type === 'text' && (
                    <div className="message-bubble">{msg.content}</div>
                  )}
                  {msg.type === 'playlist' && (
                    <div className="playlist-grid">
                      {msg.tracks.map((track, i) => (
                        <TrackCard key={i} track={track} />
                      ))}
                    </div>
                  )} { msg.type === 'error' && (
                    <div className="error-message">
                      {msg.content}
                      {msg.link && (
                        <a href={msg.link} target="_blank" rel="noopener noreferrer">
                          Github
                        </a>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message assistant">
                <div className="avatar">AI</div>
                <div className="message-bubble">
                  Düşünüyor...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Alanı */}
          <div className="input-wrapper">
            <form className="input-container" onSubmit={sendMessage}>
              <input
                className="message-input"
                placeholder="İçim kıpır kıpır..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
                autoFocus
              />
              <button type="submit" className="send-button" disabled={!input.trim() || isLoading}>
                ➤
              </button>
            </form>
              {inputError && (
          <div className="input-error-text">
            {inputError}
          </div>
        )}
          </div>


        </div>
      </div>
    );
}

export default App;