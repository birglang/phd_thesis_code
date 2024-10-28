import requests

response = requests.delete('http://localhost:8080/stats/flowentry/clear/1')
print(response)
