import subprocess
import os
import requests
import time

FNULL = open(os.devnull, 'w')
se = open("se.txt", "w")
so = open("so.txt", "w")

proc = subprocess.Popen(["python", "flask_prep.py"], stderr=se, stdout=so)

print("STARTING proc pid: ", proc.pid)

for i in range(20):
    try:
        time.sleep(1)
        requests.get("http://localhost:5113/started")
        time.sleep(4)
        break
    except Exception as e:
        print(f"ERROR: ({type(e)}) -  {e}")
