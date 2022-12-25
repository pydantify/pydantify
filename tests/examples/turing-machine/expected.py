from __future__ import annotations

from enum import Enum
from typing import Annotated, List, Optional

from pydantic import BaseModel, Field


class StateIndexType(BaseModel):
    __root__: Annotated[int, Field(ge=0, le=65535)]
    """
    Type for indexing states of the control unit.
    """


class StateLeaf(BaseModel):
    __root__: StateIndexType
    """
    Current state of the control unit.
    The initial state is 0.
    """


class CellIndexType(BaseModel):
    __root__: Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775808)]
    """
    Type for indexing tape cells.
    """


class HeadPositionLeaf(BaseModel):
    __root__: CellIndexType
    """
    Position of tape read/write head.
    """


class CoordLeaf(BaseModel):
    __root__: CellIndexType
    """
    Coordinate (index) of the tape cell.
    """


class TapeSymbolType(BaseModel):
    __root__: Annotated[str, Field(max_length=1, min_length=0)]
    """
    Type of symbols appearing in tape cells.
    A blank is represented as an empty string where necessary.
    """


class SymbolLeaf(BaseModel):
    __root__: TapeSymbolType
    """
    Symbol appearing in the tape cell.
    Blank (empty string) is not allowed here because the
    'cell' list only contains non-blank cells.
    """


class CellListEntry(BaseModel):
    """
    List of non-blank cells.
    """

    coord: Annotated[Optional[CoordLeaf], Field(alias="turing-machine:coord")] = None
    """
    Coordinate (index) of the tape cell.
    """
    symbol: Annotated[Optional[SymbolLeaf], Field(alias="turing-machine:symbol")] = None
    """
    Symbol appearing in the tape cell.
    Blank (empty string) is not allowed here because the
    'cell' list only contains non-blank cells.
    """


class TapeContainer(BaseModel):
    """
    The contents of the tape.
    """

    cell: Annotated[List[CellListEntry], Field(alias="turing-machine:cell")]


class LabelLeaf(BaseModel):
    __root__: str
    """
    An arbitrary label of the transition rule.
    """


class StateLeaf2(BaseModel):
    __root__: StateIndexType
    """
    Current state of the control unit.
    """


class SymbolLeaf2(BaseModel):
    __root__: TapeSymbolType
    """
    Symbol read from the tape cell.
    """


class InputContainer(BaseModel):
    """
    Input parameters (arguments) of the transition rule.
    """

    state: Annotated[StateLeaf2, Field(alias="turing-machine:state")]
    """
    Current state of the control unit.
    """
    symbol: Annotated[SymbolLeaf2, Field(alias="turing-machine:symbol")]
    """
    Symbol read from the tape cell.
    """


class StateLeaf3(BaseModel):
    __root__: StateIndexType
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """


class SymbolLeaf3(BaseModel):
    __root__: TapeSymbolType
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """


class EnumerationEnum(Enum):
    """
    An enumeration.
    """

    int_0 = 0
    int_1 = 1


class HeadDirType(BaseModel):
    __root__: EnumerationEnum
    """
    Possible directions for moving the read/write head, one cell
    to the left or right (default).
    """


class HeadMoveLeaf(BaseModel):
    __root__: HeadDirType
    """
    Move the head one cell to the left or right
    """


class OutputContainer(BaseModel):
    """
    Output values of the transition rule.
    """

    state: Annotated[Optional[StateLeaf3], Field(alias="turing-machine:state")] = None
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """
    symbol: Annotated[
        Optional[SymbolLeaf3], Field(alias="turing-machine:symbol")
    ] = None
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """
    head_move: Annotated[
        HeadMoveLeaf, Field(alias="turing-machine:head-move")
    ] = "right"
    """
    Move the head one cell to the left or right
    """


class DeltaListEntry(BaseModel):
    """
    The list of transition rules.
    """

    label: Annotated[Optional[LabelLeaf], Field(alias="turing-machine:label")] = None
    """
    An arbitrary label of the transition rule.
    """
    input: Annotated[
        Optional[InputContainer], Field(alias="turing-machine:input")
    ] = None
    output: Annotated[
        Optional[OutputContainer], Field(alias="turing-machine:output")
    ] = None


class TransitionFunctionContainer(BaseModel):
    """
    The Turing Machine is configured by specifying the
    transition function.
    """

    delta: Annotated[List[DeltaListEntry], Field(alias="turing-machine:delta")]


class TuringMachineContainer(BaseModel):
    """
    State data and configuration of a Turing Machine.
    """

    state: Annotated[StateLeaf, Field(alias="turing-machine:state")]
    """
    Current state of the control unit.
    The initial state is 0.
    """
    head_position: Annotated[
        HeadPositionLeaf, Field(alias="turing-machine:head-position")
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
    - if a class contains only a `__root__` field, it can be initialized as follows:
        - `member=MyNode(__root__=<value>)`
        - `member=<value>`

    Serialziation:
    - use `exclude_defaults=True` to
    - use `by_alias=True` to ensure qualified names are used ()
    """

    turing_machine: Annotated[
        Optional[TuringMachineContainer], Field(alias="turing-machine:turing-machine")
    ] = None


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True)

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
