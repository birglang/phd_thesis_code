
'''
# Add Flow
import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

dpid = 2
priority = 1
inport = 1
src = "ce:26:a1:70:6b:19"
dst = "5e:a9:a7:9d:35:42"
outport = 99

data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "in_port":%d,\n        "dl_src":"%s",\n\t"dl_dst":"%s"\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n}' % (dpid, priority, inport, src, dst, outport)
print(data)
response = requests.post('http://localhost:8080/stats/flowentry/add', headers=headers, data=data)
print(response)


# Modify Flow

'''

import requests

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
}
dpid = 2
priority = 1
inport = 1
src = "02:08:82:0b:d5:3e"
dst = "9a:12:db:bb:f9:15"
outport = 99

data = '{\n    "dpid": %d,\n    "table_id": 0,\n    "priority": %d,\n    "match":{\n        "dl_src":"%s",\n        "dl_dst":"%s"\n\n    },\n    "actions":[\n        {\n            "type":"OUTPUT",\n            "port": %d\n        }\n    ]\n }' % (dpid, priority, src, dst, outport)

response = requests.post('http://localhost:8080/stats/flowentry/modify', headers=headers, data=data)
print(response)



