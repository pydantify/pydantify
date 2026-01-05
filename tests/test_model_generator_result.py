from __future__ import annotations

from typing import Annotated, ClassVar

from pydantic import BaseModel, ConfigDict, Field, RootModel


class MockModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    prefix: ClassVar = 'if'


class MockRootModel(RootModel[MockModel]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[MockModel, Field(title='MockRootModel')]
