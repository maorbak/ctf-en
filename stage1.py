import requests
from requests.auth import HTTPBasicAuth

from env import config

headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"
resp = requests.get(orgs_url, headers=headers)

org_id = resp.json()[0]['id']

getNetwork_url = f"{config['MERAKI_BASE_URL']}/organizations/{org_id}/networks"

networks = requests.get(getNetwork_url, headers=headers)

#print(resp.json())
#print("Organization: " + str(resp.json()[0]) + "\n")

for item in networks.json():
    if item['name'] == "DevNet Sandbox ALWAYS ON":
        network_id = item['id']
        
getDevice_url = f"{config['MERAKI_BASE_URL']}/networks/{network_id}/devices"

devices = requests.get(getDevice_url, headers=headers)

#print(devices.json())

counter = 1

for item in devices.json():
    print('----------', "\n")
    print('Device number ', str(counter), "\n")
    if 'name' in item:
        print("Name: " + item['name'] + "\n")
    if 'type' in item:
        print("Type: " + item['type'] + "\n")
    if 'mac' in item:
        print("Mac address: " + item['mac'] + "\n")
    if 'serial' in item:
        print("Serial: " + item['serial'] + "\n")
    counter = counter + 1