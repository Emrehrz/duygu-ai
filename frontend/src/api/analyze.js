// src/api/chat.js
// Handles all requests to the chat backend

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function analyzeMessage(text) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    throw new Error('Failed to get response');
  }
  return response.json();
}

// Request:
// ```json
// {
//   "text": "Bugün kendimi çok mutlu hissediyorum!"
// }
// ```

// Response:
// ```json
// {
//   "valence": 0.8,
//   "arousal": 0.6,
//   "emotion": "happy",
//   "confidence": 0.3,
//   "provider": "local"
// }
// ```
