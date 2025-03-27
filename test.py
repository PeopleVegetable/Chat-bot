import requests

req = requests.post('http://127.0.0.1:20121/telegram', json={'message': 'Hi!'})

print(req)
