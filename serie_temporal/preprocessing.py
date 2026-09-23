"""
Convierte la respuesta JSON de la API en un DataFrame limpio, validado y
ordenado cronológicamente.
"""
import pandas as pd


def json_a_dataframe(data: dict) -> pd.DataFrame:
    """Convierte el bloque 'daily' del JSON de Open-Meteo en un DataFrame."""
    daily = data["daily"]
    df = pd.DataFrame(daily)
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(columns={"time": "fecha"})
    return df


def validar_y_limpiar(df: pd.DataFrame, columna_objetivo: str = "temperature_2m_max") -> pd.DataFrame:
    """
    Valida tipos de dato, fechas, orden temporal y valores faltantes.

    Reglas aplicadas:
    1. La columna 'fecha' debe ser datetime.
    2. Las columnas numéricas se fuerzan a tipo numérico (valores no
       convertibles se marcan como NaN, nunca se descartan silenciosamente).
    3. Los registros se ordenan por fecha ascendente (nunca se debe usar
       información futura para predecir el pasado).
    4. Se detectan huecos en la serie (días faltantes) y se completan.
    5. Los valores faltantes se interpolan linealmente en el tiempo.
    """
    df = df.copy()

    assert pd.api.types.is_datetime64_any_dtype(df["fecha"]), "La columna 'fecha' debe ser datetime"
    for col in df.columns:
        if col != "fecha":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.sort_values("fecha").reset_index(drop=True)

    fechas_esperadas = pd.date_range(df["fecha"].min(), df["fecha"].max(), freq="D")
    faltantes = fechas_esperadas.difference(df["fecha"])
    if len(faltantes) > 0:
        df = df.set_index("fecha").reindex(fechas_esperadas).rename_axis("fecha").reset_index()

    n_faltantes_antes = int(df[columna_objetivo].isna().sum())
    df[columna_objetivo] = df[columna_objetivo].interpolate(method="linear", limit_direction="both")
    n_faltantes_despues = int(df[columna_objetivo].isna().sum())

    print(f"Registros totales tras validar: {len(df)}")
    print(f"Días con huecos detectados: {len(faltantes)}")
    print(f"Valores faltantes en '{columna_objetivo}' antes de interpolar: {n_faltantes_antes}")
    print(f"Valores faltantes después de interpolar: {n_faltantes_despues}")

    return df
