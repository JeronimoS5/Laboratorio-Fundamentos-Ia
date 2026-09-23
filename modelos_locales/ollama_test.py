import requests
import time

def consumir_api_local():
    # URL por defecto de la API local de Ollama
    url = "http://localhost:11434/api/generate"
    
    # El payload que le enviamos al modelo
    payload = {
        "model": "llama3.2", # O el modelo exacto que bajaste en Ollama
        "prompt": "Menciona 3 lenguajes de programación populares para backend. Sé muy breve.",
        "stream": False 
    }
    
    print("Conectando con la API local de Ollama...")
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() 
        
        data = response.json()
        end_time = time.time()
        
        print("\n--- RESPUESTA GENERADA DESDE PYTHON ---")
        print(data["response"])
        print("---------------------------------------")
        print(f"Tiempo de inferencia API: {round(end_time - start_time, 2)} segundos")
        
    except Exception as e:
        print(f"Error al conectar: {e}")

if __name__ == "__main__":
    consumir_api_local()