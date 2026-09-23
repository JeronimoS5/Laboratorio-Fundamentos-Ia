"""
Baseline (persistencia) y modelo predictivo (regresión lineal con variables
de rezago y estacionalidad anual) para la serie temporal.
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression


def construir_features(df: pd.DataFrame, columna_objetivo: str, n_lags: int = 3) -> pd.DataFrame:
    """Crea variables de rezago (lags) y componentes estacionales (día del año)."""
    df = df.copy()
    for lag in range(1, n_lags + 1):
        df[f"lag_{lag}"] = df[columna_objetivo].shift(lag)

    dia_del_anio = df["fecha"].dt.dayofyear
    df["estacional_sin"] = np.sin(2 * np.pi * dia_del_anio / 365.25)
    df["estacional_cos"] = np.cos(2 * np.pi * dia_del_anio / 365.25)

    df = df.dropna().reset_index(drop=True)
    return df


def dividir_train_test(df: pd.DataFrame, proporcion_train: float = 0.8):
    """
    División train/test respetando el orden temporal: el conjunto de
    entrenamiento es siempre pasado respecto al conjunto de prueba.
    """
    corte = int(len(df) * proporcion_train)
    train = df.iloc[:corte].reset_index(drop=True)
    test = df.iloc[corte:].reset_index(drop=True)
    return train, test


def entrenar_modelo(train: pd.DataFrame, columna_objetivo: str, feature_cols: list) -> LinearRegression:
    """Entrena el modelo predictivo (regresión lineal) sobre el conjunto de entrenamiento."""
    modelo = LinearRegression()
    modelo.fit(train[feature_cols], train[columna_objetivo])
    return modelo


def predecir(modelo: LinearRegression, df: pd.DataFrame, feature_cols: list) -> np.ndarray:
    return modelo.predict(df[feature_cols])
