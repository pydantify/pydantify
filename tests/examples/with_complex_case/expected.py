from __future__ import annotations

from typing import Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class DailyLeaf(BaseModel):
    pass
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )


class ManualLeaf(BaseModel):
    pass
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )


class DailyCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    daily: Annotated[Optional[DailyLeaf], Field(alias="interfaces:daily")] = None
    time_of_day: Annotated[
        Optional[str], Field(alias="interfaces:time-of-day", title="Time-of-dayLeaf")
    ] = "1am"


class IntervalCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    interval: Annotated[
        Optional[int],
        Field(alias="interfaces:interval", ge=0, le=65535, title="IntervalLeaf"),
    ] = 30


class ManualCase(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    manual: Annotated[Optional[ManualLeaf], Field(alias="interfaces:manual")] = None


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
    how: Annotated[
        Optional[Union[IntervalCase, DailyCase, ManualCase]],
        Field(alias="interfaces:how"),
    ] = None


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
