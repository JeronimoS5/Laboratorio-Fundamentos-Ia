## 1. Consumo de Recursos (Hardware)

Se ejecutaron dos modelos en Ollama (generalista y código) y un modelo en LM Studio. A continuación, el registro de los recursos observados en mi equipo (16 GB RAM) durante la inferencia:

| Entorno | Nombre del Modelo | Cuantización | RAM consumida (aprox) | Tiempo de respuesta / Velocidad |
| :--- | :--- | :--- | :--- | :--- |
| **Ollama** | `llama3.2` | Q4 (Nativo) | 649 MB | Inmediato / Fluido |
| **Ollama** | `qwen2.5-coder` | Q4 (Nativo) | 623 MB | Inmediato / Fluido |
| **LM Studio** | `llama3` | Q4_K_M | 650 MB | 88.17 tokens/segundo |