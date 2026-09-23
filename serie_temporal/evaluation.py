"""
Métricas de evaluación para comparar predicción vs. valores reales.
"""
import numpy as np


def mae(y_real, y_pred) -> float:
    """Error absoluto medio."""
    return float(np.mean(np.abs(np.array(y_real) - np.array(y_pred))))


def rmse(y_real, y_pred) -> float:
    """Raíz del error cuadrático medio."""
    return float(np.sqrt(np.mean((np.array(y_real) - np.array(y_pred)) ** 2)))


def resumen_metricas(nombre: str, y_real, y_pred) -> dict:
    """Calcula MAE y RMSE, los imprime y los devuelve como diccionario."""
    resultado = {"modelo": nombre, "MAE": round(mae(y_real, y_pred), 3), "RMSE": round(rmse(y_real, y_pred), 3)}
    print(f"{nombre:28s} | MAE = {resultado['MAE']:.3f}  | RMSE = {resultado['RMSE']:.3f}")
    return resultado
