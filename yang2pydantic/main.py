#!/usr/bin/env python

import json
from datamodel_code_generator.parser.jsonschema import JsonSchemaParser, Parser


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


def convert(data: json):
    from genson import SchemaBuilder
    builder = SchemaBuilder()
    builder.add_object(data)
    schema = builder.to_schema()
    parser: Parser = JsonSchemaParser(
        source=json.dumps(schema),
        base_class="pydantic.BaseModel",
    )
    return parser.parse()


def main():
    input = 'input.json'
    output = f'{__package__}/out.py'
    with open(input) as f:
        a = json.load(f)
        b = convert(a)
        with open(output, "w+") as fout:
            fout.write(b)


if __name__ == "__main__":
    main()
