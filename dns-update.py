#!/usr/bin/python3

import json
import requests

API = "https://api.digitalocean.com/v2/"
API_KEY = "<API KEY>" # maks sure key has write
DOMAIN = '<DOMAIN>'
RECORD = ['<DNS RECORD']


headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(API_KEY)}

def getip():
    ip = requests.get('https://api.ipify.org').text
    return ip

def getrecordid(r, d):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(API_KEY)}
    api_url = '{0}domains/{1}/records'.format(API, d)

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        for record in data['domain_records']:
            if record['name'] == r:
                return record['id']
    else:
        return None

def getrecordip(id, d):
    api_url = '{0}domains/{1}/records/{2}'.format(API, d, id)
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        return data['domain_record']['data']
    else:
        return None

def setrecordip(id, d, ip):
    api_url = '{0}domains/{1}/records/{2}'.format(API, d, id)
    data = {'data': ip}
    response = requests.put(api_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        data = json.loads(response.content.decode('utf-8'))
        print(data)
        print('done')
    else:
        return None

if __name__ == '__main__':

    ip = getip()
    for record in RECORD:
        id = getrecordid(record, DOMAIN)
        currentip = getrecordip(id, DOMAIN)
        if currentip != ip:
            setrecordip(id, DOMAIN, ip)