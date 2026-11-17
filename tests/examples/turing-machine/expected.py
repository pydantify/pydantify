from __future__ import annotations

from enum import Enum
from typing import Annotated, ClassVar

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, RootModel


class EnumerationEnum(Enum):
    left = "left"
    right = "right"


class HeadDirType(RootModel[EnumerationEnum]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: EnumerationEnum
    """
    Possible directions for moving the read/write head, one cell
    to the left or right (default).
    """


class HeadMoveLeaf(RootModel[HeadDirType]):
    model_config = ConfigDict(
        regex_engine="python-re",
    )
    root: HeadDirType
    """
    Move the head one cell to the left or right
    """


class CellListEntry(BaseModel):
    """
    List of non-blank cells.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    coord: Annotated[
        int,
        Field(
            ge=-9223372036854775808,
            le=9223372036854775807,
            serialization_alias="turing-machine:coord",
            validation_alias=AliasChoices("turing-machine:coord", "coord"),
        ),
    ]
    """
    Coordinate (index) of the tape cell.
    """
    symbol: Annotated[
        str | None,
        Field(
            max_length=1,
            min_length=0,
            serialization_alias="turing-machine:symbol",
            validation_alias=AliasChoices("turing-machine:symbol", "symbol"),
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
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    state: Annotated[
        int,
        Field(
            ge=0,
            le=65535,
            serialization_alias="turing-machine:state",
            validation_alias=AliasChoices("turing-machine:state", "state"),
        ),
    ]
    """
    Current state of the control unit.
    """
    symbol: Annotated[
        str,
        Field(
            max_length=1,
            min_length=0,
            serialization_alias="turing-machine:symbol",
            validation_alias=AliasChoices("turing-machine:symbol", "symbol"),
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
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    state: Annotated[
        int | None,
        Field(
            ge=0,
            le=65535,
            serialization_alias="turing-machine:state",
            validation_alias=AliasChoices("turing-machine:state", "state"),
        ),
    ] = None
    """
    New state of the control unit. If this leaf is not
    present, the state doesn't change.
    """
    symbol: Annotated[
        str | None,
        Field(
            max_length=1,
            min_length=0,
            serialization_alias="turing-machine:symbol",
            validation_alias=AliasChoices("turing-machine:symbol", "symbol"),
        ),
    ] = None
    """
    Symbol to be written to the tape cell. If this leaf is
    not present, the symbol doesn't change.
    """
    head_move: Annotated[
        HeadMoveLeaf | None,
        Field(
            serialization_alias="turing-machine:head-move",
            validate_default=True,
            validation_alias=AliasChoices(
                "turing-machine:head-move", "head_move", "head-move"
            ),
        ),
    ] = "right"


class TapeContainer(BaseModel):
    """
    The contents of the tape.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    cell: Annotated[
        list[CellListEntry] | None,
        Field(
            serialization_alias="turing-machine:cell",
            validate_default=True,
            validation_alias=AliasChoices("turing-machine:cell", "cell"),
        ),
    ] = []


class DeltaListEntry(BaseModel):
    """
    The list of transition rules.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    label: Annotated[
        str,
        Field(
            serialization_alias="turing-machine:label",
            validation_alias=AliasChoices("turing-machine:label", "label"),
        ),
    ]
    """
    An arbitrary label of the transition rule.
    """
    input: Annotated[
        InputContainer | None,
        Field(
            serialization_alias="turing-machine:input",
            validation_alias=AliasChoices("turing-machine:input", "input"),
        ),
    ] = None
    output: Annotated[
        OutputContainer | None,
        Field(
            serialization_alias="turing-machine:output",
            validation_alias=AliasChoices("turing-machine:output", "output"),
        ),
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
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    delta: Annotated[
        list[DeltaListEntry] | None,
        Field(
            serialization_alias="turing-machine:delta",
            validate_default=True,
            validation_alias=AliasChoices("turing-machine:delta", "delta"),
        ),
    ] = []


class TuringMachineContainer(BaseModel):
    """
    State data and configuration of a Turing Machine.
    """

    model_config = ConfigDict(
        populate_by_name=True,
        regex_engine="python-re",
    )
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    state: Annotated[
        int,
        Field(
            ge=0,
            le=65535,
            serialization_alias="turing-machine:state",
            validation_alias=AliasChoices("turing-machine:state", "state"),
        ),
    ]
    """
    Current state of the control unit.
    The initial state is 0.
    """
    head_position: Annotated[
        int,
        Field(
            ge=-9223372036854775808,
            le=9223372036854775807,
            serialization_alias="turing-machine:head-position",
            validation_alias=AliasChoices(
                "turing-machine:head-position", "head_position", "head-position"
            ),
        ),
    ]
    """
    Position of tape read/write head.
    """
    tape: Annotated[
        TapeContainer | None,
        Field(
            serialization_alias="turing-machine:tape",
            validation_alias=AliasChoices("turing-machine:tape", "tape"),
        ),
    ] = None
    transition_function: Annotated[
        TransitionFunctionContainer | None,
        Field(
            serialization_alias="turing-machine:transition-function",
            validation_alias=AliasChoices(
                "turing-machine:transition-function",
                "transition_function",
                "transition-function",
            ),
        ),
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
    namespace: ClassVar[str | None] = "http://example.net/turing-machine"
    prefix: ClassVar[str | None] = "tm"
    turing_machine: Annotated[
        TuringMachineContainer | None,
        Field(
            serialization_alias="turing-machine:turing-machine",
            validation_alias=AliasChoices(
                "turing-machine:turing-machine", "turing_machine", "turing-machine"
            ),
        ),
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
