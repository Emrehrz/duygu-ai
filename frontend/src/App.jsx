import { useState, useRef, useEffect } from 'react';
import './App.css';
import { analyzeMessage } from './api/analyze';
import { getRecommendations } from './api/recommender';
import Particles from './components/Particles';

// Yardımcı Bileşen: Track Card
const TrackCard = ({ track }) => (
  <div className="track-card">
    <div className="track-icon">🎵</div>
    <div className="track-info">
      <h4>{track.title}</h4>
      <p>{track.artist}</p>
    </div>
    <div className="track-score">%{Math.round(track.score * 100)}</div>
  </div>
);

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasStarted, setHasStarted] = useState(false); // UI Durumu
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

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
      console.log("this is analysisData", analysisData);
      const assistantAnalysisMsg = {
        role: 'assistant',
        type: 'text',
        content: `Sizi ${analysisData.emotion} hissettiren bir durum sezdim. (Güven: %${Math.round(analysisData.confidence * 100)})`,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantAnalysisMsg]);

      // 2. Öneri
      const recommendRequest = { valence: analysisData.valence, arousal: analysisData.arousal };
      const recommendation = await getRecommendations(recommendRequest);

      const playlistMsg = {
        role: 'assistant',
        type: 'playlist',
        tracks: recommendation.tracks,
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, playlistMsg]);

    } catch (error) {
      console.error(error);
      setMessages(prev => [...prev, {
        role: 'assistant',
        type: 'text',
        content: "Üzgünüm, bir bağlantı hatası oluştu.",
        timestamp: new Date().toISOString()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

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
                placeholder="Örn: İşten yeni geldim ve biraz yorgunum."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                disabled={isLoading}
                autoFocus
              />
              <button type="submit" className="send-button" disabled={!input.trim() || isLoading}>
                ➤
              </button>
            </form>
          </div>

        </div>
      </div>
    );
}

export default App;