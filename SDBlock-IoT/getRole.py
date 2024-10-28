
import os
import json
switch_id = 1
cmd = 'sudo curl -X GET http://localhost:8080/stats/role/'+ str(switch_id)
os.system(cmd)

