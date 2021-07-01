import os
import time
import requests

while(True):
    os.system("python -m py2pddl.parse climate_planner.py")

    data = {'domain': open('domain.pddl', 'r').read(),
            'problem': open('problem.pddl', 'r').read()}

    responce = requests.post('http://solver.planning.domains/solve', json=data).json()

    for act in responce['result']['plan']:
        print(str(act['name']))

    time.sleep(10)

