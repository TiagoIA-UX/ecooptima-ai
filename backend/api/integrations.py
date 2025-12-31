# Pontos de integração para APIs externas (IoT, clima, carbono, blockchain, etc)

import requests

# Exemplo: integração com API de clima

def get_weather(city, country_code, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather": data["weather"][0]["description"]
        }
    return None

# Exemplo: stub para integração com API de carbono

def get_carbon_offset(country_code, value):
    # Aqui você pode integrar com provedores de créditos de carbono
    return {
        "country": country_code,
        "offset": value * 0.1,  # Exemplo fictício
        "unit": "kgCO2"
    }
