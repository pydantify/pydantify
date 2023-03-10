def restconf_patch_request(url: str, user_pw_auth: tuple[str, str], data: str):
    r"""Sends a restconf "PATCH" request to a network device

    :param url: e.g. `'https://sandbox.cisco.com/restconf/data/Cisco-IOS-XE-native:native/interface'`
    :param user_pw_auth: tuple of username & password, e.g. `("user", "pw")`
    :param data: restconf payload as generated by `Model.json(...)`

    :return: HTTP Request response
    """
    import requests

    response = requests.patch(
        url=url,
        auth=user_pw_auth,
        headers={
            "Accept": "application/yang-data+json",
            "Content-Type": "application/yang-data+json",
        },
        data=data,
        verify=False,
    )

    return response
