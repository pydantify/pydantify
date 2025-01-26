from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class IndexLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=255, title="IndexLeaf")]
    """
    Each key in a keychain requires a unique identifier, the index value specifies this identifier
    """


class KeyListEntry(BaseModel):
    """
    List of keys in the keychain
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    index: Annotated[
        Optional[int], Field(alias="keychains:index", ge=0, le=255, title="IndexLeaf")
    ] = None
    """
    Each key in a keychain requires a unique identifier, the index value specifies this identifier
    """


class EnumerationEnum(Enum):
    isis = "isis"
    ospf = "ospf"


class EnumerationEnum2(Enum):
    none = "none"


class KeychainListEntry(BaseModel):
    """
    List of system keychains
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    name: Annotated[Optional[str], Field(alias="keychains:name", title="NameLeaf")] = (
        None
    )
    """
    The user configured name for the keychain
    """
    type: Annotated[
        Optional[EnumerationEnum], Field(alias="keychains:type", title="TypeLeaf")
    ] = None
    """
    Specifies the intended use of the keychain

     The type constrains the set of crypto algorithms that are available to use with each key in the keychain. It is also used to ensure that this keychain is only used by protocols for which it is intended.
    """
    active_key_for_send: Annotated[
        Optional[Union[EnumerationEnum2, IndexLeaf]],
        Field(alias="keychains:active-key-for-send", title="Active-key-for-sendLeaf"),
    ] = None
    """
    Provides the key index of the currently active Keychain key
    """
    key: Annotated[Optional[List[KeyListEntry]], Field(alias="keychains:key")] = None


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
    keychain: Annotated[
        Optional[List[KeychainListEntry]], Field(alias="keychains:keychain")
    ] = None


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
