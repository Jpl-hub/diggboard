import datetime

import requests

data = {
'start_datetime':'2025-04-09T15:30:00Z',
# 'end_datetime':'2025-04-09T15:30:00Z',
}
res = requests.post('http://127.0.0.1:9898/api/index', json=data)
print(res.json())