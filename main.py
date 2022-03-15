import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
from time import sleep


def get_url(url):   # открываем удаленный URL
    for _ in range(60):
        try:
            texturl = requests.get(url)
        except requests.exceptions.ConnectionError:
            print(-1, 'Connection Error')
            sleep(10)
        else:
            break
    soup = BeautifulSoup(texturl.text, 'lxml')
    return soup


#Парсим данные с удаленных датчиков
current_parameters = []
url = 'http://87.103.192.122'
soup = get_url(url)
for tag in soup.find_all('div'):
    if not(":" in tag.text):
        current_parameters.append(float(tag.text))

#Парсим текущую погоду на улице с сайта RP5
url = 'https://rp5.ru/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B5%D0%BC%D0%B5%D1%80%D0%BE%D0%B2%D0%B5'
soup = get_url(url)
for tag in soup.find_all('span',style="display: block;"):
    current_parameters.append(float(tag.text[:-3]))

#Текущие значения параметров считаны с датчиков
print(current_parameters)

current_date = datetime.now()


#Открываем файл, считываем станые данные
with open('data.json') as json_file:
    data = json.load(json_file)
print(datetime.now())
print(data['Parameters'][0]['Temperature'])
print(data['Parameters'][1]['Humidity'])
print(data['Parameters'][2]['Pressure'])
print(data['Date'])

#Обновляем данные
data['Parameters'][0]['Temperature'].append(current_parameters[0])
data['Parameters'][0]['Temperature'].pop(0)

data['Parameters'][1]['Humidity'].append(current_parameters[1])
data['Parameters'][1]['Humidity'].pop(0)

data['Parameters'][2]['Pressure'].append(round(current_parameters[2]*0.00750062,2))
data['Parameters'][2]['Pressure'].pop(0)

data['Parameters'][3]['Outdoor'].append(current_parameters[3])
data['Parameters'][3]['Outdoor'].pop(0)

data['Date'].append((current_date+timedelta(hours=7)).isoformat())
data['Date'].pop(0)

#Открываем файл, сохраняем данные
with open('data.json', 'w') as outfile:
    json.dump(data, outfile)



