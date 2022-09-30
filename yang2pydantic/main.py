#!/usr/bin/env python

import json


def fetch(address: str, port: int) -> json:
    import requests
    from requests.auth import HTTPBasicAuth
    USER = 'arista'
    PASS = 'arista'
    headers = {'Content-Type': 'application/yang-data+json', 'Accept': 'application/yang-data+json'}
    api_call = f"https://{address}:{port}/restconf/data/openconfig-interfaces:interfaces/interface=Ethernet1/state"
    result: requests.Response = requests.get(api_call, auth=HTTPBasicAuth(USER, PASS), headers=headers, verify=False)
    result.raise_for_status()
    return result.json()


def main():
    from .run import run
    run()


if __name__ == "__main__":
    main()
