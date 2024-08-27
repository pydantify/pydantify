from __future__ import annotations

from enum import Enum
from typing import List

from pydantic import BaseModel, ConfigDict, Field, RootModel
from typing_extensions import Annotated


class CellIndexType(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775807)]
    """
    Type for indexing tape cells.
    """


class CoordLeaf(RootModel[CellIndexType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[CellIndexType, Field(title="CoordLeaf")]
    """
    Coordinate (index) of the tape cell.
    """


class HeadPositionLeaf(RootModel[CellIndexType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[CellIndexType, Field(title="Head-positionLeaf")]
    """
    Position of tape read/write head.
    """


class LabelLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(title="LabelLeaf")]
    """
    An arbitrary label of the transition rule.
    """


class StateIndexType(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[int, Field(ge=0, le=65535)]
    """
    Type for indexing states of the control unit.
    """


class StateLeaf(RootModel[StateIndexType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[StateIndexType, Field(title="StateLeaf")]
    """
    Current state of the control unit.
    The initial state is 0.
    """


class StateLeaf2(RootModel[StateIndexType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[StateIndexType, Field(title="StateLeaf2")]
    """
    Current state of the control unit.
    """


class StateLeaf3(RootModel[StateIndexType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[StateIndexType, Field(title="StateLeaf3")]
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """


class TapeSymbolType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[str, Field(max_length=1, min_length=0)]
    """
    Type of symbols appearing in tape cells.
    A blank is represented as an empty string where necessary.
    """


class EnumerationEnum(Enum):
    integer_0 = 0
    integer_1 = 1


class HeadDirType(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: EnumerationEnum
    """
    Possible directions for moving the read/write head, one cell
    to the left or right (default).
    """


class HeadMoveLeaf(RootModel[HeadDirType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[HeadDirType, Field(title="Head-moveLeaf")]
    """
    Move the head one cell to the left or right
    """


class SymbolLeaf(RootModel[TapeSymbolType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[TapeSymbolType, Field(title="SymbolLeaf")]
    """
    Symbol appearing in the tape cell.
    Blank (empty string) is not allowed here because the
    'cell' list only contains non-blank cells.
    """


class SymbolLeaf2(RootModel[TapeSymbolType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[TapeSymbolType, Field(title="SymbolLeaf2")]
    """
    Symbol read from the tape cell.
    """


class SymbolLeaf3(RootModel[TapeSymbolType]):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    root: Annotated[TapeSymbolType, Field(title="SymbolLeaf3")]
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """


class CellListEntry(BaseModel):
    """
    List of non-blank cells.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    coord: Annotated[CoordLeaf, Field(None, alias="turing-machine:coord")]
    symbol: Annotated[SymbolLeaf, Field(None, alias="turing-machine:symbol")]


class InputContainer(BaseModel):
    """
    Input parameters (arguments) of the transition rule.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    state: Annotated[StateLeaf2, Field(alias="turing-machine:state")]
    symbol: Annotated[SymbolLeaf2, Field(alias="turing-machine:symbol")]


class OutputContainer(BaseModel):
    """
    Output values of the transition rule.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    state: Annotated[StateLeaf3, Field(None, alias="turing-machine:state")]
    symbol: Annotated[SymbolLeaf3, Field(None, alias="turing-machine:symbol")]
    head_move: Annotated[HeadMoveLeaf, Field("right", alias="turing-machine:head-move")]


class TapeContainer(BaseModel):
    """
    The contents of the tape.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    cell: Annotated[List[CellListEntry], Field(alias="turing-machine:cell")]


class DeltaListEntry(BaseModel):
    """
    The list of transition rules.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    label: Annotated[LabelLeaf, Field(None, alias="turing-machine:label")]
    input: Annotated[InputContainer, Field(None, alias="turing-machine:input")]
    output: Annotated[OutputContainer, Field(None, alias="turing-machine:output")]


class TransitionFunctionContainer(BaseModel):
    """
    The Turing Machine is configured by specifying the
    transition function.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    delta: Annotated[List[DeltaListEntry], Field(alias="turing-machine:delta")]


class TuringMachineContainer(BaseModel):
    """
    State data and configuration of a Turing Machine.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )
    state: Annotated[StateLeaf, Field(alias="turing-machine:state")]
    head_position: Annotated[
        HeadPositionLeaf, Field(alias="turing-machine:head-position")
    ]
    tape: Annotated[TapeContainer, Field(None, alias="turing-machine:tape")]
    transition_function: Annotated[
        TransitionFunctionContainer,
        Field(None, alias="turing-machine:transition-function"),
    ]


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
    turing_machine: Annotated[
        TuringMachineContainer, Field(None, alias="turing-machine:turing-machine")
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
