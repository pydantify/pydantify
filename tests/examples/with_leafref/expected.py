from __future__ import annotations

from typing import Annotated, List

from pydantic import BaseModel, Field


class TestLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=0, le=255)]
    """
    Test node
    """


class NameLeaf(BaseModel):
    __root__: str
    """
    Interface name
    """


class IpLeaf(BaseModel):
    __root__: str
    """
    Interface IP
    """


class InterfacesListEntry(BaseModel):
    """
    List of configured device interfaces
    """

    test: TestLeaf
    """
    Test node
    """
    name: NameLeaf
    """
    Interface name
    """
    ip: IpLeaf
    """
    Interface IP
    """


class MgmtInterfaceLeaf(BaseModel):
    __root__: NameLeaf
    """
    Dedicated management interface
    """


class InterfacesModule(BaseModel):
    """
    Example demonstarating leafref nodes
    """

    interfaces: List[InterfacesListEntry]
    mgmt_interface: Annotated[MgmtInterfaceLeaf, Field(alias='mgmt-interface')]
    """
    Dedicated management interface
    """


class Model(BaseModel):
    interfaces: InterfacesModule


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True)

    print(f'Generated output: {restconf_payload}')

    # Send config to network device:
    # from pydantify.utility import restconf_put_request
    # restconf_put_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
