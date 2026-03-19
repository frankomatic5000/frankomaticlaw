{
  "providers": {
    "minimax": {
      "baseUrl": "https://api.minimax.io/anthropic",
      "api": "anthropic-messages",
      "authHeader": true,
      "models": [
        {
          "id": "MiniMax-M2.5",
          "name": "MiniMax M2.5",
          "reasoning": true,
          "input": [
            "text"
          ],
          "cost": {
            "input": 0.3,
            "output": 1.2,
            "cacheRead": 0.03,
            "cacheWrite": 0.12
          },
          "contextWindow": 200000,
          "maxTokens": 8192,
          "api": "anthropic-messages"
        }
      ]
    },
    "ollama": {
      "baseUrl": "http://127.0.0.1:11434",
      "apiKey": "ollama-local",
      "api": "ollama",
      "models": [
        {
          "id": "kimi-k2.5:cloud",
          "name": "kimi-k2.5:cloud",
          "reasoning": true,
          "input": [
            "text",
            "image"
          ],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 262144,
          "maxTokens": 8192,
          "api": "ollama"
        }
      ]
    }
  }
}
