import requests

name = input('Введите имя')
while True:
    text = input()
    data = {
        "name": name,
        "text": text
    }
    responce = requests.post("http://127.0.0.1:8080/send", json=data)