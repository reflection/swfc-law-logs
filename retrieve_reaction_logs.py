import json
import requests
from time import sleep
from urllib.parse import urlencode

h_post = {
  'Accept-Language': 'en-us',
  'Connection': 'keep-alive',
  'Proxy-Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'SWFC-U/w/5.3.11/[iPhone OS 9.3.3]/[iPad5,3]',
  'X-Unity-Version': '5.3.7p4'
}
# Insert values for your current swfc session
q = {
  'PHPSESSID': '',
  'opensocial_viewer_id': ''
}
data = {
  'version': 52,
  'division': 1,
  'section': 1,
  'turn': 1
}

url = 'https://amw.s.konaminet.jp/amw/naboo/api/guild/event/warship_combat/init?' + urlencode(q)

with open('logs/law_results.json', 'wb') as f:
  while True:
    r = requests.post(url, data=data, headers=h_post, allow_redirects=True)
    f.write(r.content)
    f.write('\n'.encode('utf-8'))
    sleep(0.5)
