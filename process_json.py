import re
import json

actions = {}
charges = {}
num_boards = 0

with open('logs/law_battle.json', 'r') as f:
  for line in f:
    d = json.loads(line)

    for h in d['history']:
      if h['action'].find('charged') > -1:
        continue
      if h['action'].find('issued an order') > -1:
        continue
      if h['action'].find('initiated') > -1:
        continue

      action = h['action']
      idx = action.find('... (Received')
      if idx > -1:
        action = action[:idx]
      idx = action.find('successful!')
      if idx > -1:
        action = action[:idx+10]
      if action not in actions and 'date' in h:
        actions[action] = d['base_info']['turn_resttime'] - h['date']

    if int(d['abordage_cnt']) > num_boards:
      num_boards = int(d['abordage_cnt'])

boards = []
launches = {
  '5': {},
  '2': {},
  '1': {},
  '0': {}
}
targets = {}
legion = ''
opponent = ''
off_wins = 0
off_losses = 0

with open('logs/law_results.json', 'r') as f:
  for line in f:
    d = json.loads(line)

    legion = d['my_guild_info']['name']
    opponent = d['enemy_guild_info']['guild_info']['name']

    for h in d['history']:
      action = h['action']
      idx = action.find('... (Received')
      if idx > -1:
        action = action[:idx]
      idx = action.find('!')
      if idx > -1:
        action = action[:idx]

      if action not in actions and 'date' in h:
        actions[action] = h['date']

for action, ts in actions.items():
  action = action.replace('<color=#35FC00>', '')
  action = action.replace('<color=#FF7800>', '')
  action = action.replace('</color>', '')
  add_idx = action.find('preparing to launch')
  sub_idx = action.find('cancelled launching')
  if add_idx + sub_idx > -2:
    add = False
    sub = False
    if add_idx > -1:
      add = True
      idx = add_idx
    else:
      sub = True
      idx = sub_idx

    sf = action[idx+20:-1]
    minute = int(ts / 60)
    if minute >= 3:
      minute = '5'
    else:
      minute = str(minute)
    if sf not in launches[minute]:
      launches[minute][sf] = 0

    if sub:
      launches[minute][sf] -= 1
    else:
      launches[minute][sf] += 1
  else:
    m = re.search('targeting the (.+?),', action)
    if m:
      target = m.group(1)
      if target not in targets:
        targets[target] = 0
      targets[target] += 1

    m = re.search('action (.+)', action)
    if m:
      res = m.group(1)
      if res == 'was successful':
        off_wins += 1
      else:
        off_losses += 1

    boards.append((ts, '{}'.format(action)))


print('{} vs {} Boarding Logs'.format(legion, opponent))
for ts, event in sorted(boards, key=lambda x:-x[0]):
  print('{}:{:02d} - {}'.format(int(ts / 60), ts % 60, event))
print('')
print('Total Boards - {}  * Not all may be captured in logs'.format(num_boards))
print('Targets - {}'.format(', '.join(['{}: {}'.format(target, num) for target, num in targets.items()])))
print('Logs - Wins: {}  Losses: {}  Win %: {:.2f}'.format(off_wins, off_losses, (off_wins / (off_wins + off_losses)) * 100))
print('')
print('{} vs {} Starfighter Logs'.format(legion, opponent))
print('5:00 to 3:00 - {}'.format(', '.join(['{}: {}'.format(sf, num) for sf, num in launches['5'].items()])))
print('2:59 to 2:00 - {}'.format(', '.join(['{}: {}'.format(sf, num) for sf, num in launches['2'].items()])))
print('1:59 to 1:00 - {}'.format(', '.join(['{}: {}'.format(sf, num) for sf, num in launches['1'].items()])))
print('0:59 to 0:00 - {}'.format(', '.join(['{}: {}'.format(sf, num) for sf, num in launches['0'].items()])))
