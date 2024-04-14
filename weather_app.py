import requests
import json
import sys

#api_key='4ebc12f2c2438fdb9cf3b6b7a92b6586'
#'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

def main():
    city = user_input()
    information=get_api_info(city) #mtliani informaciis dicts damibrunebs
    readable_information = get_readable_information(information)
    get_location_url = generate_map_url(city)
    temperature(information, city, get_location_url)
    tenianoba(information)
    weather_description(information)
    print(f'Location on map: {get_location_url}')  # This line remains here
    
def user_input():
    city=input('Enter the city: ').title().lstrip()
    return city


def temperature(information,city, get_location_url,):
        try:
            temperature = information.get('main') #main-shia temperature, amitom amovighot main
            temp=temperature.get('temp') #aq mere mainidan amovighe temperature
            temp_in_celsius = kelvin_to_celsius(temp) #gardaqmnili temperature
            print(f'Temperature in {city} is : {temp_in_celsius:.1f}^C.')
        except:
            print(f'not this kind of city or cant be get info. Visit map for suggestions: {get_location_url}')
            again_location_input()


def again_location_input():
    again_input = input('Do you want to try another location? (yes/no): ')
    if again_input.lower() == 'yes':
        main()
    else:
        sys.exit(1) #1 radgan error araa da ise vtishav amitom statusad 1 unda iyos
        

def tenianoba(information):
    try:
        humidity = information.get('main')
        h = humidity.get('humidity')
        print(f'Humidity is: {h} %.')
    except AttributeError:
        pass

def weather_description(information):
    try:
        weather_description = information.get('weather') #aq amindis lists vigheb
        description = weather_description[0]#aq listidan dicts vigheb
        get_info = description.get('description') #aq amindis agweras vigeb

        get_wind_dict = information.get('wind')
        get_wind_speed = get_wind_dict.get('speed')
        print(f'Weather description: {get_info}\nwind speed: {get_wind_speed} m/sec.') #vbewhdav aghweril aminds
    except:
        pass

def get_readable_information(info):
    return json.dumps(info, indent = 4)

def kelvin_to_celsius(K): #kelvinebidan gardavqmnat celsiusebshi
    C = K - 273.15
    return C

def get_api_info(city):
    api_key = '4ebc12f2c2438fdb9cf3b6b7a92b6586'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200 and data.get('cod') == 200:  #shevamowmot tu citys ipovis
        return data
    else:
        return None  # daabrunebs nones tu citys ver ipovis

def generate_map_url(location_name):
    base_url = "https://www.openstreetmap.org/search?"
    params = {
        "query": location_name,
    }
    url = base_url + "&".join([f"{key}={value}" for key, value in params.items()])
    return url

if __name__=='__main__':
    main()

# def get_api_info(city): #info-s amogheba
#     api_key = '4ebc12f2c2438fdb9cf3b6b7a92b6586'
#     url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
#     info = requests.get(url)
#     return info.json() #daabrunebs mtliani informaciis dicts.