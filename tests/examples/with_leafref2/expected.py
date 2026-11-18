from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, RootModel


class IndexLeaf(RootModel[int]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=255)]
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
    namespace: ClassVar[str | None] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-keychains"
    )
    prefix: ClassVar[str | None] = "keychains"
    index: Annotated[
        int,
        Field(
            ge=0,
            le=255,
            serialization_alias="keychains:index",
            validation_alias=AliasChoices("keychains:index", "index"),
        ),
    ]
    """
    Each key in a keychain requires a unique identifier, the index value specifies this identifier
    """


class EnumerationEnum(Enum):
    isis = "isis"
    ospf = "ospf"


class EnumerationEnum2(Enum):
    none = "none"


class KeychainTypeType(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum


class TypeLeaf(RootModel[KeychainTypeType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: KeychainTypeType
    """
    Specifies the intended use of the keychain

    The type constrains the set of crypto algorithms that are available to use with each key in the keychain. It is also used to ensure that this keychain is only used by protocols for which it is intended.
    """


class KeychainListEntry(BaseModel):
    """
    List of system keychains
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-keychains"
    )
    prefix: ClassVar[str | None] = "keychains"
    name: Annotated[
        str,
        Field(
            serialization_alias="keychains:name",
            validation_alias=AliasChoices("keychains:name", "name"),
        ),
    ]
    """
    The user configured name for the keychain
    """
    type: Annotated[
        TypeLeaf | None,
        Field(
            serialization_alias="keychains:type",
            validation_alias=AliasChoices("keychains:type", "type"),
        ),
    ] = None
    """
    Specifies the intended use of the keychain

     The type constrains the set of crypto algorithms that are available to use with each key in the keychain. It is also used to ensure that this keychain is only used by protocols for which it is intended.
    """
    active_key_for_send: Annotated[
        EnumerationEnum2 | IndexLeaf | None,
        Field(
            serialization_alias="keychains:active-key-for-send",
            validation_alias=AliasChoices(
                "keychains:active-key-for-send",
                "active_key_for_send",
                "active-key-for-send",
            ),
        ),
    ] = None
    """
    Provides the key index of the currently active Keychain key
    """
    key: Annotated[
        list[KeyListEntry] | None,
        Field(
            serialization_alias="keychains:key",
            validate_default=True,
            validation_alias=AliasChoices("keychains:key", "key"),
        ),
    ] = []


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
    namespace: ClassVar[str | None] = (
        "http://ultraconfig.com.au/ns/yang/ultraconfig-keychains"
    )
    prefix: ClassVar[str | None] = "keychains"
    keychain: Annotated[
        list[KeychainListEntry] | None,
        Field(
            serialization_alias="keychains:keychain",
            validate_default=True,
            validation_alias=AliasChoices("keychains:keychain", "keychain"),
        ),
    ] = []


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
