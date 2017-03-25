import json
import requests
from time import sleep
from urllib.parse import urlencode

h_get = {
  'Host': 'amw.s.konaminet.jp',
  'Accept-Language': 'en-us',
  'Connection': 'keep-alive',
  'Proxy-Connection': 'keep-alive',
  'Accept-Encoding': 'gzip, deflate',
  'Accept': '*/*'
}

# Insert values for your current swfc session
q = {
  'PHPSESSID': '',
  'opensocial_viewer_id': ''
}

url = 'https://amw.s.konaminet.jp/amw/naboo/api/guild/event/warship_combat/warship_combat_battle?' + urlencode(q)
with open('logs/law_sfs.json', 'wb') as f:
  r = requests.get(url, headers=h_get, allow_redirects=True)
  f.write(r.content)
