import json
from math import radians, cos, sin, asin

def load_data(filepath):
    try:
        json_file = open(filepath, 'r')
    except:
        while True:
            print("Ошибка при загрузке файла.")
            try:
                filepath = input("Введите корректный адрес файла: \n")
                json_file = open(filepath, 'r')
            except Exception:
                continue
            else:
                print("Файл загружен успешно.\n")
                break
    parsed_json = json.loads(json_file.read())
    json_file.close()
    return parsed_json

def get_biggest_bar(data):
    result = "" 
    the_biggest_bars = [["none", 0]]
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
    result += "Самый большой бар: "
    for bar in the_biggest_bars:
        result += "\n -" + bar[0] + " " + str(bar[1]) + " мест"
    return result

def get_smallest_bar(data):
    result = "" 
    the_smallest_bars = [["none", 9999]]
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
    result += "Самый маленький бар: "
    for bar in the_smallest_bars:
        result += "\n -" + bar[0] + " " + str(bar[1]) + " мест"
    return result

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(a**0.5) 
    km = 6367 * c
    return km

def get_closest_bar(data, longitude, latitude):
    min_distance = 384401
    nearest_bar = "none"
    current_distance = 0
    for bar in data:
        bar_pos_lat = bar["Cells"]["geoData"]["coordinates"][0]
        bar_pos_lon = bar["Cells"]["geoData"]["coordinates"][1]
        current_distance = calculate_distance(bar_pos_lon, bar_pos_lat, \
            longitude, latitude)
        if(current_distance < min_distance):
            min_distance = current_distance
            nearest_bar = bar["Cells"]["Name"] + \
            "\nАдрес: " + bar["Cells"]["Address"] + \
            "\nРасстояние :" + str(round(current_distance, 3)) + " км"
    return nearest_bar

def get_user_coordinates():
    print("\nВвод gps-координат.")
    while True:
        try:
            input_coords = \
            input("Введите gps-координаты в формате '[широта], [долгота]': \n").split(",")
            result_longitude = float(input_coords[0].strip())
            result_latitude = float(input_coords[1].strip())
        except Exception:
            print ("Некорректный ввод, попробуйте ещё раз.")
        else:
            break
    return result_longitude,result_latitude

filepath = 'bars.json'
data = load_data(filepath)
print(get_biggest_bar(data))
print(get_smallest_bar(data))
longitude, latitude = get_user_coordinates()
print("Ближайший бар: ", get_closest_bar(data, longitude, latitude))
