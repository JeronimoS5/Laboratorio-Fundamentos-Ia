"""
Cliente de la API histórica de clima de Open-Meteo.
No requiere API key. Documentación oficial:
https://open-meteo.com/en/docs/historical-weather-api
"""
import requests

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def obtener_clima_historico(latitude, longitude, start_date, end_date,
                             daily_vars=("temperature_2m_max", "temperature_2m_min", "precipitation_sum"),
                             timezone="America/Bogota"):
    """
    Consulta la API pública de Open-Meteo y devuelve el JSON crudo con la
    serie temporal diaria solicitada para una ubicación y rango de fechas.

    Parameters
    ----------
    latitude, longitude : float
        Coordenadas del lugar a consultar.
    start_date, end_date : str
        Fechas en formato 'YYYY-MM-DD'.
    daily_vars : tuple[str]
        Variables diarias a solicitar (ver documentación de la API).
    timezone : str
        Zona horaria para las marcas de tiempo devueltas.

    Returns
    -------
    dict
        Respuesta JSON de la API, con la forma:
        {"daily": {"time": [...], "temperature_2m_max": [...], ...}, ...}
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join(daily_vars),
        "timezone": timezone,
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    # Ejemplo: Manizales, Colombia
    data = obtener_clima_historico(
        latitude=5.07, longitude=-75.52,
        start_date="2023-01-01", end_date="2024-12-31",
    )
    print("Días descargados:", len(data["daily"]["time"]))
    print("Primeros registros:", data["daily"]["time"][:5])
