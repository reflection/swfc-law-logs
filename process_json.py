import json

actions = {}
charges = {}
reactions = {}

with open('logs/law_battle.json', 'r') as f:
  for line in f:
    d = json.loads(line)

    for h in d['history']:
      if h['action'] not in actions and 'date' in h:
        actions[h['action']] = d['base_info']['turn_resttime'] - h['date']

    c = d['action_result_turn_info']
    del c['vehicle_charge']
    c_json = json.dumps(c)
    if c_json not in charges:
      charges[c_json] = d['base_info']['turn_resttime']

out = []

with open('logs/law_results.json', 'r') as f:
  for line in f:
    d = json.loads(line)

    for h in d['history']:
      if h['action'] not in reactions and 'date' in h:
        reactions[h['action']] = h['date']

for action, ts in actions.items():
  action = action.replace('<color=#35FC00>', '')
  action = action.replace('<color=#FF7800>', '')
  action = action.replace('</color>', '')
  out.append((ts, 'action: {}'.format(action)))

for c_json, ts in charges.items():
  c = json.loads(c_json)
  out.append((ts, 'charges: hp: {}, main_cannon: {}, sub_cannon: {}, shield: {}'.format(c['hp_charge'], c['main_cannon_charge'], c['sub_cannon_charge'], c['shield_charge'])))

for action, ts in reactions.items():
  action = h['action']
  action = action.replace('<color=#35FC00>', '')
  action = action.replace('<color=#FF7800>', '')
  action = action.replace('</color>', '')
  out.append((ts, 'action: {}'.format(action)))

for ts, event in sorted(out, key=lambda x:-x[0]):
  print('{}:{:02d} left  {}'.format(int(ts / 60), ts % 60, event))
