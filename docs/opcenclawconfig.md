{
  "meta": {
    "lastTouchedVersion": "2026.3.13",
    "lastTouchedAt": "2026-03-19T19:46:32.437Z"
  },
  "wizard": {
    "lastRunAt": "2026-03-19T18:11:42.792Z",
    "lastRunVersion": "2026.3.13",
    "lastRunCommand": "configure",
    "lastRunMode": "local"
  },
  "auth": {
    "profiles": {
      "minimax:global": {
        "provider": "minimax",
        "mode": "api_key"
      },
      "ollama:default": {
        "provider": "ollama",
        "mode": "api_key"
      },
      "openrouter:default": {
        "provider": "openrouter",
        "mode": "api_key"
      }
    }
  },
  "models": {
    "mode": "merge",
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
            "maxTokens": 8192
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
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "minimax/MiniMax-M2.5",
        "fallbacks": [
          "minimax/MiniMax-M2.5",
          "ollama/kimi-k2.5:cloud"
        ]
      },
      "models": {
        "minimax/MiniMax-M2.5": {
          "alias": "Minimax"
        },
        "ollama/kimi-k2.5:cloud": {},
        "openrouter/auto": {
          "alias": "OpenRouter"
        }
      },
      "workspace": "/Users/frankomatic007/.openclaw/workspace"
    },
    "list": [
      {
        "id": "main"
      }
    ]
  },
  "tools": {
    "profile": "coding",
    "alsoAllow": [
      "ollama_web_search",
      "ollama_web_fetch"
    ],
    "web": {
      "search": {
        "enabled": false
      },
      "fetch": {
        "enabled": false
      }
    }
  },
  "commands": {
    "native": "auto",
    "nativeSkills": "auto",
    "restart": true,
    "ownerDisplay": "raw"
  },
  "session": {
    "dmScope": "per-channel-peer"
  },
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "boot-md": {
          "enabled": true
        },
        "bootstrap-extra-files": {
          "enabled": true
        },
        "command-logger": {
          "enabled": true
        },
        "session-memory": {
          "enabled": true
        }
      }
    }
  },
  "channels": {
    "discord": {
      "enabled": true,
      "token": "[REDACTED]",
      "groupPolicy": "allowlist",
      "streaming": "off",
      "guilds": {
        "1483230870155296849": {
          "channels": {
            "1483230871338225798": {
              "allow": true
            }
          }
        }
      }
    }
  },
  "gateway": {
    "port": 18789,
    "mode": "local",
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "[REDACTED]"
    },
    "tailscale": {
      "mode": "off",
      "resetOnExit": false
    },
    "nodes": {
      "denyCommands": [
        "camera.snap",
        "camera.clip",
        "screen.record",
        "contacts.add",
        "calendar.add",
        "reminders.add",
        "sms.send"
      ]
    }
  },
  "plugins": {
    "allow": [
      "openclaw-web-search",
      "discord"
    ],
    "entries": {
      "discord": {
        "enabled": true
      },
      "openclaw-web-search": {
        "enabled": true
      }
    },
    "installs": {
      "openclaw-web-search": {
        "source": "npm",
        "spec": "@ollama/openclaw-web-search",
        "installPath": "/Users/frankomatic007/.openclaw/extensions/openclaw-web-search"
      }
    }
  }
}
