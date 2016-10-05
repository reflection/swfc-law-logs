import json

actions = {}
charges = {}
boards = 0

with open('logs/law_battle.json', 'r') as f:
  for line in f:
    d = json.loads(line)

    for h in d['history']:
      if h['action'].find('charged') > -1:
        continue
      if h['action'].find('launch') > -1:
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

    if int(d['abordage_cnt']) > boards:
      boards = int(d['abordage_cnt'])

out = []
legion = ''
opponent = ''
combat_logs = []

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

    for c in d['combat_log']:
      if c['is_owner']:
        combat_logs.append('Legion: {}'.format(' '.join(c['texts'])))
      else:
        combat_logs.append('Opponent: {}'.format(' '.join(c['texts'])))

for action, ts in actions.items():
  action = action.replace('<color=#35FC00>', '')
  action = action.replace('<color=#FF7800>', '')
  action = action.replace('</color>', '')
  out.append((ts, '{}'.format(action)))

for ts, event in sorted(out, key=lambda x:-x[0]):
  print('{}:{:02d} - {}'.format(int(ts / 60), ts % 60, event))

print('total boards: {}\n\n'.format(boards))
print('{} vs {} combat logs'.format(legion, opponent))
for c in combat_logs:
  print(c)
  print('\n')
