
import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

data = '{\n    "dpid": 1,\n    "role": "MASTER"\n }'

response = requests.post('http://localhost:8080/stats/role', headers=headers, data=data)
print(response)

