from __future__ import annotations

from typing import Annotated, List

from pydantic import BaseModel, ConfigDict, Field


class InterfaceContainer(BaseModel):
    """
    Just a simple example of a container.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: str = "http://ultraconfig.com.au/ns/yang/ultraconfig-interface"
    prefix: str = "if"
    primary: Annotated[
        List[None],
        Field(alias="interface:primary", max_length=1, min_length=1),
    ] = None
    """
    primary IP
    """


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
    namespace: str = "http://ultraconfig.com.au/ns/yang/ultraconfig-interface"
    prefix: str = "if"
    interface: Annotated[InterfaceContainer, Field(alias="interface:interface")] = None


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
