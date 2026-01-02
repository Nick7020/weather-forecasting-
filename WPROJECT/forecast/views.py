import requests
from django.shortcuts import render
from datetime import datetime

def index(request):
    API_KEY = '6db9cc3577bf668402cbcc2145ccc0a3'
    url = 'http://api.openweathermap.org/data/2.5/forecast?q={}&units=metric&appid=' + API_KEY

    forecast_list, chart_temps, chart_humidity, chart_labels = [], [], [], []
    current_weather, city_name = None, ""

    if request.method == 'POST':
        city_name = request.POST.get('city')
        try:
            response = requests.get(url.format(city_name)).json()
            if response.get('cod') == "200":
                current = response['list'][0]
                current_weather = {
                    'temp': round(current['main']['temp']),
                    'condition': current['weather'][0]['main'].lower(), 
                    'desc': current['weather'][0]['description'].lower(), 
                    'icon': current['weather'][0]['icon'],
                    'hum': current['main']['humidity'], 
                    'wind': current['wind']['speed'], 
                    'pres': current['main']['pressure'],
                }
                for i, item in enumerate(response['list'][:10]):
                    chart_temps.append(item['main']['temp'])
                    chart_humidity.append(item['main']['humidity'])
                    chart_labels.append(f"Pt {i+1}")
                for item in response['list'][::8]:
                    forecast_list.append({
                        'day': datetime.fromtimestamp(item['dt']).strftime('%A'),
                        'temp': round(item['main']['temp']),
                        'condition': item['weather'][0]['main'].lower(),
                        'desc': item['weather'][0]['description'].lower(),
                    })
            else:
                current_weather = {'error': 'Location not identified.'}
        except:
            current_weather = {'error': 'Network issue.'}

    return render(request, 'forecast/index.html', {
        'current': current_weather, 'forecast': forecast_list, 
        'city': city_name, 'chart_temps': chart_temps, 
        'chart_humidity': chart_humidity, 'chart_labels': chart_labels
    })