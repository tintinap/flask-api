# Client Side

import requests
URL = 'http://127.0.0.1:5000/weather/2'
response = requests.get(URL)

message = response.json() 
print(message)