from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar, List

from pydantic import BaseModel, ConfigDict, Field, RootModel


class CellIndexType(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775807)]
    """
    Type for indexing tape cells.
    """


class CoordLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775807)]
    """
    Coordinate (index) of the tape cell.
    """


class HeadPositionLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=-9223372036854775808, le=9223372036854775807)]
    """
    Position of tape read/write head.
    """


class LabelLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: str
    """
    An arbitrary label of the transition rule.
    """


class StateIndexType(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=65535)]
    """
    Type for indexing states of the control unit.
    """


class StateLeaf(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=65535)]
    """
    Current state of the control unit.
    The initial state is 0.
    """


class StateLeaf2(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=65535)]
    """
    Current state of the control unit.
    """


class StateLeaf3(RootModel[int]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[int, Field(ge=0, le=65535)]
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """


class TapeSymbolType(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=1, min_length=0)]
    """
    Type of symbols appearing in tape cells.
    A blank is represented as an empty string where necessary.
    """


class EnumerationEnum(Enum):
    left = 'left'
    right = 'right'


class HeadDirType(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: EnumerationEnum
    """
    Possible directions for moving the read/write head, one cell
    to the left or right (default).
    """


class HeadMoveLeaf(RootModel[HeadDirType]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: HeadDirType
    """
    Move the head one cell to the left or right
    """


class SymbolLeaf(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=1, min_length=0)]
    """
    Symbol appearing in the tape cell.
    Blank (empty string) is not allowed here because the
    'cell' list only contains non-blank cells.
    """


class SymbolLeaf2(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=1, min_length=0)]
    """
    Symbol read from the tape cell.
    """


class SymbolLeaf3(RootModel[str]):
    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    root: Annotated[str, Field(max_length=1, min_length=0)]
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
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    coord: Annotated[
        int,
        Field(
            alias='turing-machine:coord',
            ge=-9223372036854775808,
            le=9223372036854775807,
        ),
    ]
    """
    Coordinate (index) of the tape cell.
    """
    symbol: Annotated[
        str, Field(alias='turing-machine:symbol', max_length=1, min_length=0)
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
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    state: Annotated[int, Field(alias='turing-machine:state', ge=0, le=65535)]
    """
    Current state of the control unit.
    """
    symbol: Annotated[
        str, Field(alias='turing-machine:symbol', max_length=1, min_length=0)
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
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    state: Annotated[int, Field(alias='turing-machine:state', ge=0, le=65535)] = None
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """
    symbol: Annotated[
        str, Field(alias='turing-machine:symbol', max_length=1, min_length=0)
    ] = None
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """
    head_move: Annotated[
        HeadMoveLeaf,
        Field(
            default_factory=lambda: HeadMoveLeaf('right'),
            alias='turing-machine:head-move',
        ),
    ]


class TapeContainer(BaseModel):
    """
    The contents of the tape.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    cell: Annotated[
        List[CellListEntry], Field(default_factory=list, alias='turing-machine:cell')
    ]


class DeltaListEntry(BaseModel):
    """
    The list of transition rules.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    label: Annotated[str, Field(alias='turing-machine:label')]
    """
    An arbitrary label of the transition rule.
    """
    input: Annotated[InputContainer, Field(alias='turing-machine:input')] = None
    output: Annotated[OutputContainer, Field(alias='turing-machine:output')] = None


class TransitionFunctionContainer(BaseModel):
    """
    The Turing Machine is configured by specifying the
    transition function.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    delta: Annotated[
        List[DeltaListEntry], Field(default_factory=list, alias='turing-machine:delta')
    ]


class TuringMachineContainer(BaseModel):
    """
    State data and configuration of a Turing Machine.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    state: Annotated[int, Field(alias='turing-machine:state', ge=0, le=65535)]
    """
    Current state of the control unit.
    The initial state is 0.
    """
    head_position: Annotated[
        int,
        Field(
            alias='turing-machine:head-position',
            ge=-9223372036854775808,
            le=9223372036854775807,
        ),
    ]
    """
    Position of tape read/write head.
    """
    tape: Annotated[TapeContainer, Field(alias='turing-machine:tape')] = None
    transition_function: Annotated[
        TransitionFunctionContainer, Field(alias='turing-machine:transition-function')
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
    namespace: ClassVar = 'http://example.net/turing-machine'
    prefix: ClassVar = 'tm'
    turing_machine: Annotated[
        TuringMachineContainer, Field(alias='turing-machine:turing-machine')
    ] = None


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