"""
Weather Tool
Gets weather information using Open-Meteo API (free, no API key required).
"""

import requests
from typing import Dict, Optional
from datetime import datetime


def get_weather(city: str = None, lat: float = None, lon: float = None) -> Dict[str, any]:
    """
    Get current weather for a location.
    Uses Open-Meteo API (free, no API key needed).
    
    Args:
        city: City name (will geocode to coordinates)
        lat: Latitude (optional, use with lon)
        lon: Longitude (optional, use with lat)
    
    Returns:
        Dictionary with weather data.
    """
    try:
        # If city provided, geocode it first
        if city and not (lat and lon):
            geo = _geocode_city(city)
            if not geo['success']:
                return geo
            lat = geo['lat']
            lon = geo['lon']
            location_name = geo['name']
        elif lat and lon:
            location_name = f"{lat}, {lon}"
        else:
            # Default to a location (could use IP-based location as fallback)
            return {
                'success': False,
                'message': 'Please provide a city name or coordinates'
            }
        
        # Get weather from Open-Meteo
        weather_url = 'https://api.open-meteo.com/v1/forecast'
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m,is_day',
            'timezone': 'auto'
        }
        
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data.get('current', {})
        
        # Convert weather code to description
        weather_desc = _weather_code_to_description(current.get('weather_code', 0))
        is_day = current.get('is_day', 1)
        
        return {
            'success': True,
            'location': location_name,
            'temperature': current.get('temperature_2m'),
            'temperature_unit': '°C',
            'humidity': current.get('relative_humidity_2m'),
            'wind_speed': current.get('wind_speed_10m'),
            'wind_unit': 'km/h',
            'condition': weather_desc,
            'is_day': bool(is_day),
            'message': f"{location_name}: {current.get('temperature_2m')}°C, {weather_desc}"
        }
        
    except requests.Timeout:
        return {
            'success': False,
            'message': 'Weather service timed out'
        }
    except requests.RequestException as e:
        return {
            'success': False,
            'message': f'Failed to get weather: {str(e)}',
            'error': str(e)
        }
    except Exception as e:
        return {
            'success': False,
            'message': f'Error: {str(e)}',
            'error': str(e)
        }


def get_weather_forecast(city: str, days: int = 3) -> Dict[str, any]:
    """
    Get weather forecast for upcoming days.
    
    Args:
        city: City name
        days: Number of days to forecast (1-7)
    
    Returns:
        Dictionary with forecast data.
    """
    try:
        days = max(1, min(7, days))
        
        # Geocode city
        geo = _geocode_city(city)
        if not geo['success']:
            return geo
        
        # Get forecast
        weather_url = 'https://api.open-meteo.com/v1/forecast'
        params = {
            'latitude': geo['lat'],
            'longitude': geo['lon'],
            'daily': 'temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max',
            'timezone': 'auto',
            'forecast_days': days
        }
        
        response = requests.get(weather_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        daily = data.get('daily', {})
        
        forecast = []
        for i in range(len(daily.get('time', []))):
            forecast.append({
                'date': daily['time'][i],
                'max_temp': daily['temperature_2m_max'][i],
                'min_temp': daily['temperature_2m_min'][i],
                'condition': _weather_code_to_description(daily['weather_code'][i]),
                'rain_chance': daily['precipitation_probability_max'][i]
            })
        
        return {
            'success': True,
            'location': geo['name'],
            'forecast': forecast,
            'message': f"{days}-day forecast for {geo['name']}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Failed to get forecast: {str(e)}',
            'error': str(e)
        }


def _geocode_city(city: str) -> Dict[str, any]:
    """
    Convert city name to coordinates using Open-Meteo Geocoding API.
    """
    try:
        geo_url = 'https://geocoding-api.open-meteo.com/v1/search'
        params = {
            'name': city,
            'count': 1
        }
        
        response = requests.get(geo_url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        results = data.get('results', [])
        if not results:
            return {
                'success': False,
                'message': f'City not found: {city}'
            }
        
        result = results[0]
        return {
            'success': True,
            'lat': result['latitude'],
            'lon': result['longitude'],
            'name': f"{result['name']}, {result.get('country', '')}"
        }
        
    except Exception as e:
        return {
            'success': False,
            'message': f'Geocoding failed: {str(e)}',
            'error': str(e)
        }


def _weather_code_to_description(code: int) -> str:
    """
    Convert WMO weather code to human-readable description.
    """
    weather_codes = {
        0: 'Clear sky',
        1: 'Mainly clear',
        2: 'Partly cloudy',
        3: 'Overcast',
        45: 'Foggy',
        48: 'Depositing rime fog',
        51: 'Light drizzle',
        53: 'Moderate drizzle',
        55: 'Dense drizzle',
        61: 'Slight rain',
        63: 'Moderate rain',
        65: 'Heavy rain',
        71: 'Slight snow',
        73: 'Moderate snow',
        75: 'Heavy snow',
        77: 'Snow grains',
        80: 'Slight rain showers',
        81: 'Moderate rain showers',
        82: 'Violent rain showers',
        85: 'Slight snow showers',
        86: 'Heavy snow showers',
        95: 'Thunderstorm',
        96: 'Thunderstorm with slight hail',
        99: 'Thunderstorm with heavy hail',
    }
    return weather_codes.get(code, 'Unknown')
