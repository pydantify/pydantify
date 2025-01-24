from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class EnumerationEnum(Enum):
    left = "left"
    right = "right"


class CellListEntry(BaseModel):
    """
    List of non-blank cells.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    coord: Annotated[
        Optional[int],
        Field(
            alias="turing-machine:coord",
            ge=-9223372036854775808,
            le=9223372036854775807,
            title="CoordLeaf",
        ),
    ] = None
    """
    Coordinate (index) of the tape cell.
    """
    symbol: Annotated[
        Optional[str],
        Field(
            alias="turing-machine:symbol",
            max_length=1,
            min_length=0,
            title="SymbolLeaf",
        ),
    ] = None
    """
    Symbol appearing in the tape cell.
    Blank (empty string) is not allowed here because the
    'cell' list only contains non-blank cells.
    """


class InputContainer(BaseModel):
    """
    Input parameters (arguments) of the transition rule.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    state: Annotated[
        int, Field(alias="turing-machine:state", ge=0, le=65535, title="StateLeaf2")
    ]
    """
    Current state of the control unit.
    """
    symbol: Annotated[
        str,
        Field(
            alias="turing-machine:symbol",
            max_length=1,
            min_length=0,
            title="SymbolLeaf2",
        ),
    ]
    """
    Symbol read from the tape cell.
    """


class OutputContainer(BaseModel):
    """
    Output values of the transition rule.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    state: Annotated[
        Optional[int],
        Field(alias="turing-machine:state", ge=0, le=65535, title="StateLeaf3"),
    ] = None
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """
    symbol: Annotated[
        Optional[str],
        Field(
            alias="turing-machine:symbol",
            max_length=1,
            min_length=0,
            title="SymbolLeaf3",
        ),
    ] = None
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """
    head_move: Annotated[
        Optional[EnumerationEnum],
        Field(alias="turing-machine:head-move", title="Head-moveLeaf"),
    ] = "right"
    """
    Move the head one cell to the left or right
    """


class TapeContainer(BaseModel):
    """
    The contents of the tape.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    cell: Annotated[
        Optional[List[CellListEntry]], Field(alias="turing-machine:cell")
    ] = None


class DeltaListEntry(BaseModel):
    """
    The list of transition rules.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    label: Annotated[
        Optional[str], Field(alias="turing-machine:label", title="LabelLeaf")
    ] = None
    """
    An arbitrary label of the transition rule.
    """
    input: Annotated[Optional[InputContainer], Field(alias="turing-machine:input")] = (
        None
    )
    output: Annotated[
        Optional[OutputContainer], Field(alias="turing-machine:output")
    ] = None


class TransitionFunctionContainer(BaseModel):
    """
    The Turing Machine is configured by specifying the
    transition function.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    delta: Annotated[
        Optional[List[DeltaListEntry]], Field(alias="turing-machine:delta")
    ] = None


class TuringMachineContainer(BaseModel):
    """
    State data and configuration of a Turing Machine.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    state: Annotated[
        int, Field(alias="turing-machine:state", ge=0, le=65535, title="StateLeaf")
    ]
    """
    Current state of the control unit.
    The initial state is 0.
    """
    head_position: Annotated[
        int,
        Field(
            alias="turing-machine:head-position",
            ge=-9223372036854775808,
            le=9223372036854775807,
            title="Head-positionLeaf",
        ),
    ]
    """
    Position of tape read/write head.
    """
    tape: Annotated[Optional[TapeContainer], Field(alias="turing-machine:tape")] = None
    transition_function: Annotated[
        Optional[TransitionFunctionContainer],
        Field(alias="turing-machine:transition-function"),
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
    turing_machine: Annotated[
        Optional[TuringMachineContainer], Field(alias="turing-machine:turing-machine")
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
