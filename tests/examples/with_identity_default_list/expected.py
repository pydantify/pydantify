from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class ServerProfileListEntry(BaseModel):
    """
    List of configured TLS server profiles
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    name: Annotated[Optional[str], Field(alias="ciphers:name")] = None
    """
    Name of the TLS server-profile
    """
    cipher_list: Annotated[Optional[List[str]], Field(alias="ciphers:cipher-list")] = [
        "ecdhe-ecdsa-aes256-gcm-sha384",
        "ecdhe-ecdsa-aes128-gcm-sha256",
        "ecdhe-rsa-aes256-gcm-sha384",
        "ecdhe-rsa-aes128-gcm-sha256",
    ]
    """
    List of ciphers to use when negotiating TLS 1.2 with clients

    TLS 1.3 cipher suites are always enabled:
        tls_aes_256_gcm_sha384, tls_aes_128_gcm_sha256, tls_chacha20_poly1305_sha256
    """


class TlsContainer(BaseModel):
    """
    Top-level container for TLS configuration and state
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    server_profile: Annotated[
        Optional[List[ServerProfileListEntry]], Field(alias="ciphers:server-profile")
    ] = None


class Model(BaseModel):
    """
    Initialize an instance of this class and serialize it to JSON; this results in a RESTCONF payload.

    ## Tips
    Initialization:
    - all values have to be set via keyword arguments
    - if a class contains only a `root` field, it can be initialized as follows:
        - `member=MyNode(root=<value>)`
        - `member=<value>`

    Serialziation:
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    tls: Annotated[Optional[TlsContainer], Field(alias="ciphers:tls")] = None


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.model_dump_json(
        exclude_defaults=True, by_alias=True, indent=2
    )

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
