from __future__ import annotations

from typing import Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class DailyLeaf(BaseModel):
    pass
    model_config = ConfigDict(
        populate_by_name=True,
    )


class IntervalLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=65535, title="IntervalLeaf")]


class ManualLeaf(BaseModel):
    pass
    model_config = ConfigDict(
        populate_by_name=True,
    )


class TimeOfDayLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="Time-of-dayLeaf")]


class DailyCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    daily: Annotated[DailyLeaf, Field(None, alias="interfaces:daily")]
    time_of_day: Annotated[TimeOfDayLeaf, Field("1am", alias="interfaces:time-of-day")]


class IntervalCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    interval: Annotated[IntervalLeaf, Field(30, alias="interfaces:interval")]


class ManualCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    manual: Annotated[ManualLeaf, Field(None, alias="interfaces:manual")]


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
    )
    how: Annotated[
        Union[IntervalCase, DailyCase, ManualCase], Field(None, alias="interfaces:how")
    ]


if __name__ == "__main__":
    model = Model(  # type: ignore[call-arg]
        # <Initialize model here>
    )

    restconf_payload = model.model_dump_json(
        exclude_defaults=True, by_alias=True, indent=2
    )

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
