import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Smile, Laugh, Zap, Heart, Trophy, Mic, MicOff, Volume2, VolumeX, Sparkles } from 'lucide-react';
import './index.css';

const MOODS = [
  { id: 'happy', label: 'Happy', icon: Smile, color: '#fbbf24', glow: 'rgba(251, 191, 36, 0.3)' },
  { id: 'funny', label: 'Funny', icon: Laugh, color: '#ec4899', glow: 'rgba(236, 72, 153, 0.3)' },
  { id: 'aggressive', label: 'Aggressive', icon: Zap, color: '#ef4444', glow: 'rgba(239, 68, 68, 0.3)' },
  { id: 'motivational', label: 'Motivational', icon: Heart, color: '#10b981', glow: 'rgba(16, 185, 129, 0.3)' },
  { id: 'sports', label: 'Sports', icon: Trophy, color: '#3b82f6', glow: 'rgba(59, 130, 246, 0.3)' },
];

const API_BASE = 'http://localhost:8000';
const USER_ID = 'user_123';

function App() {
  const [currentMood, setCurrentMood] = useState(MOODS[0]);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isMuted, setIsMuted] = useState(false);
  const [digest, setDigest] = useState(null);
  const [detectedMood, setDetectedMood] = useState(null);
  
  const messagesEndRef = useRef(null);
  const recognitionRef = useRef(null);

  useEffect(() => {
    fetchHistory();
    initSpeechRecognition();
  }, []);

  useEffect(() => {
    scrollToBottom();
    // Randomize background positions on message for morphing effect
    const root = document.documentElement;
    root.style.setProperty('--x1', `${Math.random() * 40}%`);
    root.style.setProperty('--y1', `${Math.random() * 40}%`);
    root.style.setProperty('--x3', `${60 + Math.random() * 40}%`);
    root.style.setProperty('--y3', `${60 + Math.random() * 40}%`);
  }, [messages]);

  const initSpeechRecognition = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setIsListening(false);
      };
      recognitionRef.current.onend = () => setIsListening(false);
    }
  };

  const toggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      setIsListening(true);
      recognitionRef.current?.start();
    }
  };

  const speakText = (text, moodId) => {
    if (isMuted) return;
    const utterance = new SpeechSynthesisUtterance(text);
    // Adjust pitch/rate based on mood
    if (moodId === 'aggressive') { utterance.rate = 1.3; utterance.pitch = 0.8; }
    else if (moodId === 'happy') { utterance.pitch = 1.2; utterance.rate = 1.1; }
    else if (moodId === 'motivational') { utterance.rate = 0.9; utterance.pitch = 1.1; }
    
    window.speechSynthesis.speak(utterance);
  };

  const fetchHistory = async () => {
    try {
      const resp = await axios.get(`${API_BASE}/history/${USER_ID}`);
      setMessages(resp.data);
    } catch (err) { console.error("Failed to fetch history", err); }
  };

  const handleSend = async (forcedInput = null) => {
    const text = forcedInput || input;
    if (!text.trim() || loading) return;

    const userMessage = { role: 'user', content: text, mood: currentMood.id };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);
    setDetectedMood(null);

    try {
      const resp = await axios.post(`${API_BASE}/chat`, {
        user_id: USER_ID,
        mood: currentMood.id,
        message: text
      });
      
      setMessages(prev => [...prev, resp.data]);
      if (resp.data.summary) setDigest(resp.data.summary);
      if (resp.data.detected_mood && resp.data.detected_mood !== currentMood.id) {
        setDetectedMood(resp.data.detected_mood);
      }
      
      speakText(resp.data.content, currentMood.id);
    } catch (err) {
      console.error("Chat failed", err);
    } finally {
      setLoading(false);
    }
  };

  const applyDetectedMood = () => {
    const moodObj = MOODS.find(m => m.id === detectedMood);
    if (moodObj) {
      setCurrentMood(moodObj);
      setDetectedMood(null);
    }
  };

  const scrollToBottom = () => { messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' }); };

  return (
    <div className="app-container" style={{
      '--accent-color': currentMood.color,
      '--accent-glow': currentMood.glow
    }}>
      <div className="sidebar glass-card">
        <h2>Buddy AI 2.0</h2>
        <div className="mood-list">
          {MOODS.map(mood => (
            <button key={mood.id} className={`mood-btn ${currentMood.id === mood.id ? 'active' : ''}`} onClick={() => setCurrentMood(mood)}>
              <mood.icon size={20} /> {mood.label}
            </button>
          ))}
        </div>
        
        {detectedMood && (
          <div style={{ marginTop: 'auto', padding: '15px', background: 'rgba(255,255,255,0.05)', borderRadius: '15px', border: '1px solid var(--glass-border)' }}>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginBottom: '8px' }}>Detected Mood: <strong style={{ color: 'var(--accent-color)' }}>{detectedMood}</strong></p>
            <button onClick={applyDetectedMood} className="mood-btn active" style={{ padding: '8px 12px', fontSize: '0.8rem', justifyContent: 'center' }}>
              Switch to {detectedMood}?
            </button>
          </div>
        )}
      </div>

      <div className="chat-container glass-card">
        <div className="chat-header">
          <div>
            <h3><currentMood.icon size={24} color={currentMood.color} /> {currentMood.label} Mode</h3>
          </div>
          <div className="status-indicator">
            {digest && <span className="digest-tag"><Sparkles size={12} style={{ display: 'inline', marginRight: '4px' }} /> Context Active</span>}
            <div className="status-dot"></div>
            {loading ? 'Thinking...' : 'Ready'}
          </div>
        </div>

        <div className="messages-area">
          {messages.length === 0 && (
            <div style={{ textAlign: 'center', color: 'var(--text-secondary)', marginTop: '40px' }}>
              <Sparkles size={48} style={{ opacity: 0.3, marginBottom: '20px' }} />
              <p>Hello! I'm your AI companion. Pick a mood and let's talk.</p>
            </div>
          )}
          
          {messages.map((msg, idx) => (
            <React.Fragment key={idx}>
              {idx > 0 && idx % 6 === 0 && digest && (
                <div className="digest-banner">Digest: {digest}</div>
              )}
              <div className={`message ${msg.role}`}>
                {msg.content}
              </div>
            </React.Fragment>
          ))}
          <div ref={messagesEndRef} />
        </div>

        <div className="input-area">
          <button className={`icon-btn ${isListening ? 'active' : ''}`} onClick={toggleListening} title="Voice Input">
            {isListening ? <MicOff size={22} /> : <Mic size={22} />}
          </button>
          
          <input 
            type="text" 
            className="chat-input" 
            placeholder={isListening ? "Listening..." : "Speak or type your heart out..."}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSend()}
          />

          <button className="icon-btn" onClick={() => setIsMuted(!isMuted)} title="Toggle Audio Reply">
            {isMuted ? <VolumeX size={22} /> : <Volume2 size={22} />}
          </button>

          <button className="icon-btn send-btn" onClick={() => handleSend()} disabled={loading}>
            <Send size={22} />
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
