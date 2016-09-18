import json
import requests
from time import sleep
from urllib.parse import urlencode

h_post = {
  'Accept-Language': 'en-us',
  'Connection': 'keep-alive',
  'Proxy-Connection': 'keep-alive',
  'Content-Type': 'application/x-www-form-urlencoded',
  'User-Agent': 'SWFC-U/n/4.3.14/[iPhone OS 9.3.3]/[iPad5,3]',
  'X-Unity-Version': '4.7.2f1'
}
# Insert values for your current swfc session
q = {
  'PHPSESSID': '',
  'opensocial_viewer_id': ''
}
data = {
  'version': 43,
  'division': 3,
  'section': 1,
  'turn': 1
}

url = 'http://amw.konaminet.jp/amw/naboo/api/guild/event/warship_combat/reload?' + urlencode(q)

with open('logs/law_battle.json', 'wb') as f:
  while True:
    r = requests.post(url, data=data, headers=h_post, allow_redirects=True)
    f.write(r.content)
    f.write('\n'.encode('utf-8'))
    sleep(0.5)
