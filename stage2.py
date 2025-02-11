import requests
from requests.auth import HTTPBasicAuth

import json

from env import config

headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"
orgs = requests.get(orgs_url, headers=headers)

for item in orgs.json():
    if item['name'] == "DevNet Sandbox":
        org_id = item['id']

getNetwork_url = f"{config['MERAKI_BASE_URL']}/organizations/{org_id}/networks"

networks = requests.get(getNetwork_url, headers=headers)

for item in networks.json():
    if item['name'] == "DevNet Sandbox ALWAYS ON":
        network_id = item['id']
        
getDevice_url = f"{config['MERAKI_BASE_URL']}/networks/{network_id}/devices"

devices = requests.get(getDevice_url, headers=headers)

device_list = []

for item in devices.json():
    device_dict = {}
    if 'name' in item:
        device_dict["name"] = item["name"]
    if 'type' in item:
        device_dict["type"] = item["model"]
    if 'mac' in item:
        device_dict["mac"] = item["mac"]
    if 'serial' in item:
        device_dict["serial"] = item["serial"]
    device_dict['category'] = "Meraki"
    device_list.append(device_dict)

with open("stage1.json", "w") as outfile:
    json.dump(device_list, outfile)




dnac_auth_url = f"{config['DNAC_BASE_URL']}/dna/system/api/v1/auth/token"

myToken = requests.post(dnac_auth_url, auth=HTTPBasicAuth(config['DNAC_USER'], config['DNAC_PASSWORD']))

header = {
    'x-auth-token': myToken.json()['Token']
}

getDevice_url = f"{config['DNAC_BASE_URL']}/dna/intent/api/v1/network-device"
devs = requests.get(getDevice_url, headers=header)

for item in devs.json()['response']:
    device_dict = {}
    if 'hostname' in item:
        device_dict["name"] = item["hostname"]
    if 'type' in item:
        device_dict["type"] = item["type"]
    if 'macAddress' in item:
        device_dict["mac"] = item["macAddress"]
    if 'serialNumber' in item:
        device_dict["serial"] = item["serialNumber"]
    device_dict['category'] = 'DNAC'
    device_list.append(device_dict)

with open("stage2.json", "w") as outfile:
    json.dump(device_list, outfile)