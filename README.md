# Componente 0 — Mapa mental: Fundamentos de modelos de IA

Representación visual que integra los conceptos esenciales de Inteligencia Artificial, conectando la teoría de modelos (LLM, SLM, VLM, código) con su funcionamiento técnico (tokens, cuantización, ventana de contexto) y la infraestructura necesaria para ejecutarlos.

## Estructura

/mapa_mental
└── index.html      # Mapa mental interactivo con la red de conceptos

## Decisiones tomadas por el equipo

- **Enfoque relacional:** Se diseñó el mapa para evidenciar dependencias (ej. cómo la arquitectura Transformer habilita los LLMs y cómo la RAM/VRAM limita la inferencia local) en lugar de presentar un glosario aislado.
- **Base teórica:** Los conceptos definidos aquí establecen el marco de referencia que el equipo utilizó para justificar la elección de parámetros y hardware en las ejecuciones prácticas posteriores.

---

# Componente 1 — Cartografía del ecosistema de modelos de IA

Matriz comparativa que evalúa modelos actuales en las categorías de texto, razonamiento, desarrollo de software, visión, voz y embeddings, justificando la elección de cada uno con base en restricciones técnicas reales.

## Estructura

/cartografia_modelos
└── modelos.csv     # Matriz técnica comparativa y justificación de uso

## Decisiones tomadas por el equipo (no solo por la IA)

- **Ausencia de un "mejor modelo" universal:** La recomendación de uso se analizó equilibrando cinco variables críticas: tarea, recursos disponibles, privacidad del dato, costo operativo y modalidad requerida.
- **Soberanía del dato frente a la nube:** Se justificó la elección de modelos locales open-weights (ej. Qwen2.5-Coder o Llama 3.1) para entornos donde el código o la información procesada es confidencial y el presupuesto de API es cero.
- **Uso estratégico de modelos Cloud:** Se reservó la recomendación de modelos en la nube (ej. Gemini Pro o Claude 3.5 Sonnet) exclusivamente para escenarios que demandan ventanas de contexto masivas o capacidades de razonamiento inviables para el hardware local estándar.
-
- # Componente 4 — Reto integrador: 

Aplicación en Python que consume datos históricos reales de temperatura para
Manizales desde la API pública de **Open-Meteo**, construye una serie
temporal, entrena un modelo baseline y un modelo predictivo, y evalúa el
resultado con MAE y RMSE.

## Cómo ejecutar

```bash
pip install -r requirements.txt
python app.py
```

Esto descarga los datos reales (2023-01-01 a 2024-12-31, Manizales), procesa
la serie y genera:

- `serie_temporal.png` — la serie histórica completa.
- `prediccion_vs_real.png` — predicción del baseline y del modelo contra los
  valores reales del conjunto de prueba.
- `metricas.csv` — MAE y RMSE de ambos modelos.

No requiere API key. Requiere conexión a internet.

## Estructura

```
/serie_temporal
├── api_client.py      # Llamada a la API pública de Open-Meteo
├── preprocessing.py    # JSON -> DataFrame, validación, limpieza
├── model.py             # Baseline (persistencia) + regresión lineal
├── evaluation.py        # MAE, RMSE
├── app.py                # Orquesta todo el pipeline
├── requirements.txt
└── README.md
```

## Relación con el ciclo de vida clásico del software

| Fase | Aplicación en este reto |
|---|---|
| **Requisitos** | La app debe predecir la temperatura máxima diaria de Manizales a partir de datos históricos reales, y demostrar mejora frente a un baseline ingenuo. |
| **Análisis** | Se revisó la documentación de la API de Open-Meteo: estructura del JSON (`daily.time`, `daily.temperature_2m_max`, etc.), variables disponibles, límites de fechas y que no requiere autenticación. |
| **Diseño** | Se dividió la solución en 4 módulos independientes (cliente API, preprocesamiento, modelo, evaluación) para que cada uno se pueda probar y explicar por separado, en vez de un solo script monolítico. |
| **Implementación** | Desarrollo asistido por Vibe Coding (ver sección siguiente), con revisión y ejecución humana de cada módulo. |
| **Pruebas** | Se validó el pipeline completo con un dataset sintético del mismo formato exacto que la API real (ver `evidence/`), confirmando que la limpieza de datos, el entrenamiento y las métricas funcionan antes de depender de la conexión a internet. |

## Decisiones tomadas por el equipo 

- **Elección de la API**: se eligió Open-Meteo (variable meteorológica) sobre
  una API financiera porque no requiere API key ni registro, lo que evita el
  riesgo de exponer secretos en el repositorio (regla explícita del
  laboratorio).
- **Baseline elegido**: persistencia (el valor de hoy predice el de mañana)
  en vez de media móvil, porque para temperatura diaria la persistencia es
  un baseline más exigente y estándar en la literatura de series
  temporales — si el modelo no le gana a la persistencia, no aporta valor.
- **Modelo predictivo**: regresión lineal sobre variables de rezago
  (lag 1-3) más componentes estacionales (seno/coseno del día del año) en
  vez de un modelo más complejo (ARIMA, LSTM), porque es apropiado para el
  nivel del curso, fácil de explicar por el equipo (requisito explícito del
  laboratorio) y ya mejora al baseline en las pruebas.
- **Manejo de datos faltantes**: se decidió interpolar linealmente en vez de
  eliminar filas, porque para una serie temporal climática eliminar días
  rompe la continuidad necesaria para las variables de rezago.
- **División train/test**: se respetó estrictamente el orden cronológico
  (80% más antiguo para entrenar, 20% más reciente para probar) — nunca se
  mezcló aleatoriamente, para no filtrar información futura al pasado.

## Cómo se usó la IA durante el desarrollo

Se usó Claude como asistente de Vibe Coding para escribir la primera versión
de cada módulo a partir de una especificación funcional dada por el equipo
(qué debía recibir, qué debía validar, qué debía devolver cada función). El
código generado fue:

1. Ejecutado localmente por el equipo con datos reales de la API.
2. Revisado línea por línea para poder explicar cada función.
3. Probado adicionalmente con un dataset sintético (ver `evidence/`) para
   verificar la lógica de limpieza y modelado de forma reproducible, sin
   depender de que la API estuviera disponible en ese momento.

## Nota sobre la carpeta `evidence/`

Las gráficas y métricas con sufijo `_DEMO` fueron generadas con un dataset
**sintético** (no real) que replica exactamente el formato de la API, usado
únicamente para verificar que el pipeline completo funciona de extremo a
extremo antes de depender de la conexión a internet. La evidencia oficial
para la entrega debe generarse ejecutando `python app.py`, que consulta la
API real y produce `serie_temporal.png`, `prediccion_vs_real.png` y
`metricas.csv` con datos verdaderos.
