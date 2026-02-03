// src/api/recommender.js
// Handles all requests to the recommender backend

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export async function getRecommendations(input) {
  const response = await fetch(`${API_BASE}/recommend`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(input),
  });
  if (!response.ok) {
    throw new Error('Failed to fetch recommendations');
  }
  return response.json();
}


// ### Example: Recommend Endpoint

// Request:
// ```json
// {
//   "valence": 0.8,
//   "arousal": 0.6
// }
// ```

// Response:
// ```json
// {
//   "tracks": [
//     {"title": "Song 1", "artist": "Artist A", "score": 0.92},
//     {"title": "Song 2", "artist": "Artist B", "score": 0.89}
//   ]
// }
// ```