"""
Aplicación integradora — Componente 4: Vibe Coding + API + Series Temporales.

Obtiene datos climáticos reales de Manizales desde la API pública de
Open-Meteo, prepara la serie temporal, entrena un baseline y un modelo
predictivo, evalúa con MAE/RMSE y genera las gráficas del laboratorio.

Uso:
    python app.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

from api_client import obtener_clima_historico
from preprocessing import json_a_dataframe, validar_y_limpiar
from model import construir_features, dividir_train_test, entrenar_modelo, predecir
from evaluation import resumen_metricas

LATITUDE, LONGITUDE = 5.07, -75.52  # Manizales, Colombia
FECHA_INICIO, FECHA_FIN = "2023-01-01", "2024-12-31"
COLUMNA_OBJETIVO = "temperature_2m_max"
N_LAGS = 3


def main():
    print("1) Consultando la API pública de Open-Meteo (Manizales)...")
    data = obtener_clima_historico(
        latitude=LATITUDE, longitude=LONGITUDE,
        start_date=FECHA_INICIO, end_date=FECHA_FIN,
    )

    print("\n2) Preparando y validando la serie temporal...")
    df = json_a_dataframe(data)
    df = validar_y_limpiar(df, columna_objetivo=COLUMNA_OBJETIVO)

    plt.figure(figsize=(11, 4))
    plt.plot(df["fecha"], df[COLUMNA_OBJETIVO], color="#185FA5", linewidth=1)
    plt.title("Temperatura máxima diaria — Manizales")
    plt.xlabel("Fecha"); plt.ylabel("°C"); plt.tight_layout()
    plt.savefig("serie_temporal.png", dpi=130)
    plt.close()

    print("\n3) Construyendo variables (lags + estacionalidad) y dividiendo train/test...")
    df_feat = construir_features(df, COLUMNA_OBJETIVO, n_lags=N_LAGS)
    train, test = dividir_train_test(df_feat, proporcion_train=0.8)
    feature_cols = [f"lag_{i}" for i in range(1, N_LAGS + 1)] + ["estacional_sin", "estacional_cos"]
    print(f"   Entrenamiento: {len(train)} días | Prueba: {len(test)} días")

    print("\n4) Evaluando baseline (persistencia: hoy predice mañana)...")
    pred_baseline = test["lag_1"]
    metricas_baseline = resumen_metricas("Baseline (persistencia)", test[COLUMNA_OBJETIVO], pred_baseline)

    print("\n5) Entrenando modelo predictivo (regresión lineal con lags + estacionalidad)...")
    modelo = entrenar_modelo(train, COLUMNA_OBJETIVO, feature_cols)
    pred_modelo = predecir(modelo, test, feature_cols)
    metricas_modelo = resumen_metricas("Regresión lineal", test[COLUMNA_OBJETIVO], pred_modelo)

    plt.figure(figsize=(11, 4))
    plt.plot(test["fecha"], test[COLUMNA_OBJETIVO], label="Real", color="#2C2C2A", linewidth=1.4)
    plt.plot(test["fecha"], pred_baseline, label="Baseline (persistencia)", color="#993C1D", linestyle="--", linewidth=1.1)
    plt.plot(test["fecha"], pred_modelo, label="Regresión lineal", color="#0F6E56", linewidth=1.4)
    plt.title("Predicción vs. valores reales — conjunto de prueba")
    plt.xlabel("Fecha"); plt.ylabel("°C máx"); plt.legend(); plt.tight_layout()
    plt.savefig("prediccion_vs_real.png", dpi=130)
    plt.close()

    resumen = pd.DataFrame([metricas_baseline, metricas_modelo])
    resumen.to_csv("metricas.csv", index=False)

    print("\nResumen final:")
    print(resumen.to_string(index=False))
    print("\nGráficas guardadas: serie_temporal.png, prediccion_vs_real.png")
    print("Métricas guardadas: metricas.csv")


if __name__ == "__main__":
    main()
