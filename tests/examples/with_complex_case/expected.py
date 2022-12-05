from __future__ import annotations

from typing import Annotated, Union

from pydantic import BaseModel, Field


class IntervalLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=0, le=65535)]


class IntervalCase(BaseModel):
    interval: IntervalLeaf = 30


class DailyLeaf(BaseModel):
    __root__: str = ''


class TimeOfDayLeaf(BaseModel):
    __root__: str


class DailyCase(BaseModel):
    daily: DailyLeaf
    time_of_day: Annotated[TimeOfDayLeaf, Field(alias='time-of-day')] = '1am'


class ManualLeaf(BaseModel):
    __root__: str = ''


class ManualCase(BaseModel):
    manual: ManualLeaf


class InterfacesModule(BaseModel):
    """
    Example demonstarating leafref nodes
    """

    how: Union[IntervalCase, DailyCase, ManualCase]


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
