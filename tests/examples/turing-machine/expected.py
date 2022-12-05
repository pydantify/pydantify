from __future__ import annotations

from enum import Enum
from typing import Annotated, List

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

    coord: CoordLeaf
    """
    Coordinate (index) of the tape cell.
    """
    symbol: SymbolLeaf
    """
    Symbol appearing in the tape cell.
    Blank (empty string) is not allowed here because the
    'cell' list only contains non-blank cells.
    """


class TapeContainer(BaseModel):
    """
    The contents of the tape.
    """

    cell: List[CellListEntry]


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

    state: StateLeaf2
    """
    Current state of the control unit.
    """
    symbol: SymbolLeaf2
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

    state: StateLeaf3
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """
    symbol: SymbolLeaf3
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """
    head_move: Annotated[HeadMoveLeaf, Field(alias='head-move')] = 'right'
    """
    Move the head one cell to the left or right
    """


class DeltaListEntry(BaseModel):
    """
    The list of transition rules.
    """

    label: LabelLeaf
    """
    An arbitrary label of the transition rule.
    """
    input: InputContainer
    output: OutputContainer


class TransitionFunctionContainer(BaseModel):
    """
    The Turing Machine is configured by specifying the
    transition function.
    """

    delta: List[DeltaListEntry]


class TuringMachineContainer(BaseModel):
    """
    State data and configuration of a Turing Machine.
    """

    state: StateLeaf
    """
    Current state of the control unit.
    The initial state is 0.
    """
    head_position: Annotated[HeadPositionLeaf, Field(alias='head-position')]
    """
    Position of tape read/write head.
    """
    tape: TapeContainer
    transition_function: Annotated[TransitionFunctionContainer, Field(alias='transition-function')]


class TuringMachineModule(BaseModel):
    """
    Data model for the Turing Machine.
    """

    turing_machine: Annotated[TuringMachineContainer, Field(alias='turing-machine')]


class Model(BaseModel):
    turing_machine: Annotated[TuringMachineModule, Field(alias='turing-machine')]


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
