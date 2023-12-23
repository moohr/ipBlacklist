import os

import requests
def create_list(headers, account_id):
    url = "https://api.cloudflare.com/client/v4/" + "accounts/" + account_id + "/rules/lists"
    data = {
      "description": "IP blacklist automatically generated",
      "kind": "ip",
      "name": "openproxy"
    }
    r = requests.post(url, json=data, headers=headers)
    print(r.text + "post")
    if r.status_code == 200:
        return r.json()['result']['id']
    else:
        exit(1)


def get_list_id(headers, account_id):
    url = "https://api.cloudflare.com/client/v4/" + "accounts/" + account_id + "/rules/lists"
    resp = requests.get(url, headers=headers)
    lists = resp.json()['result']
    print(lists)
    for list in lists:
        if list['name'] == "openproxy":
            return list['id']
    return create_list(headers, account_id)


def update_list(headers, account_id, list_id, iplist):
    url = "https://api.cloudflare.com/client/v4/" + "accounts/" + account_id + "/rules/lists/"+list_id+"/items"
    data = []
    for ip in iplist:
        data.append({"ip": ip.strip()})
    print(data)
    resp = requests.put(url, json=data, headers=headers)
    print(resp.json())


def get_account_id(headers):
    print(headers)
    resp = requests.get("https://api.cloudflare.com/client/v4/" + "accounts", headers=headers)
    return resp.json()['result'][0]['id']


def upload_list(iplist):
    api_key = os.environ.get('CLOUDFLARE_API_KEY')
    api_email = os.environ.get('CLOUDFLARE_EMAIL')

    headers = {
        'Content-Type': 'application/json',
        'X-Auth-Email': api_email,
        'X-Auth-Key': api_key,
    }

    account_id = get_account_id(headers)
    list_id = get_list_id(headers, account_id)
    print(list_id)
    update_list(headers, account_id, list_id, iplist)
