import json
import sys
from math import radians, cos, sin, asin, sqrt

def read_console_args():
    return sys.argv[1:]

def alert_message(*messages):
    for message in messages:
        print(message)
    return

def load_data(filepath):
    parsed_json = None
    json_file = open(filepath, 'r')
    parsed_json = json.loads(json_file.read())
    json_file.close()                
    return parsed_json
    

def get_biggest_bar(data):
    result = "" 
    the_biggest_bars = [[None, 0]] # Name, seats
    max_seats = 0
    current_seats = 0
    for bar in data:
        current_seats = bar["Cells"]["SeatsCount"]
        max_seats = the_biggest_bars[0][1]
        bar_name = bar["Cells"]["Name"]
        if(current_seats >= max_seats):
            if(current_seats != max_seats):
                the_biggest_bars = []
            the_biggest_bars.append([bar_name,current_seats])
    result += "Самый большой бар Москвы: "
    for bar in the_biggest_bars:
        result += "\n -" + bar[0] + " " + str(bar[1]) + " мест"
    return result


def get_smallest_bar(data):
    result = "" 
    the_smallest_bars = [[None, 9999]] # Name, seats
    min_seats = 0
    current_seats = 0
    for bar in data:
        current_seats = bar["Cells"]["SeatsCount"]
        min_seats = the_smallest_bars[0][1]
        bar_name = bar["Cells"]["Name"]
        if (current_seats <= min_seats):
            if(current_seats != min_seats):
                the_smallest_bars = []
            the_smallest_bars.append([bar_name, current_seats])
    result += "Самый маленький бар Москвы: "
    for bar in the_smallest_bars:
        result += "\n -" + bar[0] + " " + str(bar[1]) + " мест"
    return result

def get_closest_bar(data, latitude, longitude):
    if not latitude_is_valid(latitude) or not longitude_is_valid(longitude):
        raise Exception

    min_distance = 384401
    nearest_bar = None
    current_distance = 0
    for bar in data:
        bar_pos_lon = bar["Cells"]["geoData"]["coordinates"][0]
        bar_pos_lat = bar["Cells"]["geoData"]["coordinates"][1]
        current_distance = calculate_distance(bar_pos_lat, bar_pos_lon , \
            latitude, longitude)
        if(current_distance < min_distance):
            min_distance = current_distance
            nearest_bar = bar["Cells"]["Name"] + \
            "\nАдрес: " + bar["Cells"]["Address"] + \
            "\nРасстояние :" + str(round(current_distance, 3)) + " км"
    return nearest_bar

def calculate_distance(start_latitude, start_longitude, end_latitude, end_longitude):
    if not latitude_is_valid(start_latitude) or \
    not latitude_is_valid(end_latitude) or \
    not longitude_is_valid(start_longitude) or \
    not longitude_is_valid(end_longitude):
        raise Exception

    earth_radius = 6367
    start_longitude, start_latitude, end_longitude, end_latitude = \
    map(radians, [start_longitude, start_latitude, \
        end_longitude, end_latitude]) # convert decimal degrees to radians 
    longitude_difference = end_longitude - start_longitude 
    latitude_difference = end_latitude - start_latitude 
    haversine_formula  = 2 * asin(sqrt(sin(latitude_difference / 2)**2 + \
        cos(start_latitude) * cos(end_latitude) * sin(longitude_difference / 2)**2))
    return haversine_formula * earth_radius

def latitude_is_valid(latitude):
    if (type(latitude) == float) and (latitude >= -90) and (latitude <= 90):
        return True
    else:
        return False

def longitude_is_valid(longitude):
    if (type(longitude) == float) and (longitude >= -180) and (longitude <= 180):
        return True
    else:
        return False

def get_user_coordinates():
    longitude = None
    latitude = None
    alert_message("Введите широту и долготу через пробел: ")
    coordinates = input().split(" ")
    latitude = float(coordinates[0])
    longitude = float(coordinates[1])
    if not latitude_is_valid(latitude) or not longitude_is_valid(longitude):
        raise Exception
    return latitude, longitude    


if __name__ == '__main__':
    parameters = read_console_args()
    try:
        if len(parameters) != 2:
            raise Exception
        filepath = parameters[0]
        argument = parameters[1]
        data = load_data(filepath)
    except Exception:
        alert_message("""Для работы скрипта необходимы два аргумента, переданные через пробел:
1) Валидный адрес JSON файла с данными о барах Москвы для анализа. 
2) Параметр '-bars' для поиска самого большого и маленького баров 
 или '-search' для поиска ближайшего бара по вводимым координатам.""")
    else:
        if argument == "-bars":
            the_smallest_bars = get_smallest_bar(data)
            the_biggest_bars = get_biggest_bar(data)
            alert_message(the_smallest_bars, the_biggest_bars)

        elif argument == "-search":
            alert_message("Поиск ближайшего бара. Введите текущие координаты.")
            while True:
                try:
                    latitude, longitude = get_user_coordinates()
                except Exception:
                    alert_message("Введите корректные данные!")
                else:
                    break
            try:
                closest_bar = get_closest_bar(data, latitude, longitude)
            except Exception:
                alert_message("Произошла ошибка при попытке поиска ближайшего бара.")
            else:
                alert_message("\nБлижайший бар: ", closest_bar)
        
        else:
            alert_message("Скрипт работает только с аргументами '-bars' или '-search'.")