import requests
import json
import sys
import csv
import os

def get_weather(log = False):
    '''
        Fetches weather data from OpenWeatherMap API.
        Parameters:
            `log` : `bool`
                Logs the data if `True`
        Returns:
            `None`
                Prints the weather data in a pretty format
    '''
    # Your OpenWeather API key
    city = input("Enter the city name: ")
    file_name = None

    api_key = '08776f011101db64cb3fce99543db7d8'  # Replace with your API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    
    # Building the complete URL
    complete_url = base_url + "q=" + city + "&appid=" + api_key + "&units=metric"
    
    # Sending the GET request
    response = requests.get(complete_url)
    
    # Convert the response to JSON
    data = response.json()

    if log:
        file_name = data['sys']['country']+ "/" + f"{city}.csv"

    ## print(data)
    
    # Check if the city was found
    if data["cod"] != "404":
        lat, lon = data["coord"]["lat"], data["coord"]["lon"]
        main_data = data["main"]
        weather_data = data["weather"][0]
        
        # Extracting information
        temperature = main_data["temp"]
        pressure = main_data["pressure"]
        humidity = main_data["humidity"]
        description = weather_data["description"]
        
        # Displaying the weather information
        print(f"Weather in {city} ({lat} lattitude, {lon} longitude):")
        print(f"Temperature: {temperature}°C")
        print(f"Pressure: {pressure} hPa")
        print(f"Humidity: {humidity}%")
        print(f"Description: {description}")
        if log:
            if not os.path.exists(os.curdir + "/" + data['sys']['country']):
                os.mkdir(os.curdir + "/" + data['sys']['country'])
            if os.path.exists(os.curdir + "/" + file_name):
                with open(file_name, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([temperature, pressure, humidity, description])
                    del writer
            else:
                file = open(file_name, 'w', newline='')
                writer = csv.writer(file)
                writer.writerow(["Temperature", "Pressure", "Humidity", "Description"])
                writer.writerow([temperature, pressure, humidity, description])
                del writer
    else:
        print("City not found!")

if __name__ == "__main__":
    if ("--log" in sys.argv or "-l" in sys.argv) and len(sys.argv) == 2:
        get_weather(log = True)
    elif ("--help" in sys.argv or "-h" in sys.argv) and len(sys.argv) == 2:
        print('''Usage: python weather.py [city name] [options] 
        Available options:
            * --help, -h : print this help menu
            * --log, -l  : log this data into a CSV file
            ''')
    elif len(sys.argv) == 1:
        get_weather()
    else:
        raise Exception("Incorrect syntax. Check the usage with --help or -h")
