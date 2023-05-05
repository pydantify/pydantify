from __future__ import annotations

from enum import Enum
from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field


class CandidateLeaf(BaseModel):
    """
    The candidate configuration is the config source.
    """


class CandidateCase(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config source.
    """


class RunningLeaf(BaseModel):
    """
    The running configuration is the config source.
    """


class RunningCase(BaseModel):
    running: Annotated[
        Optional[RunningLeaf], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config source.
    """


class StartupLeaf(BaseModel):
    """
    The startup configuration is the config source.
    This is optional-to-implement on the server because
    not all servers will support filtering for this
    datastore.
    """


class StartupCase(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config source.
    This is optional-to-implement on the server because
    not all servers will support filtering for this
    datastore.
    """


class SourceContainer(BaseModel):
    """
    Particular configuration to retrieve.
    """

    config_source: Annotated[
        Union[CandidateCase, RunningCase, StartupCase],
        Field(alias="ietf-netconf:config-source"),
    ]


class Filter(BaseModel):
    """
    Subtree or XPath filter to use.
    """


class Input(BaseModel):
    source: Annotated[
        Optional[SourceContainer], Field(alias="ietf-netconf:source")
    ] = None
    filter: Filter


class Data(BaseModel):
    """
    Copy of the source datastore subset that matched
    the filter criteria (if any).  An empty data container
    indicates that the request did not produce any results.
    """


class Output(BaseModel):
    data: Data


class GetConfigRpc(BaseModel):
    """
    Retrieve all or part of a specified configuration.
    """

    input: Input
    output: Output


class Output2(BaseModel):
    pass


class CandidateLeaf2(BaseModel):
    """
    The candidate configuration is the config target.
    """


class CandidateCase2(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf2], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config target.
    """


class RunningLeaf2(BaseModel):
    """
    The running configuration is the config source.
    """


class RunningCase2(BaseModel):
    running: Annotated[
        Optional[RunningLeaf2], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config source.
    """


class TargetContainer(BaseModel):
    """
    Particular configuration to edit.
    """

    config_target: Annotated[
        Union[CandidateCase2, RunningCase2], Field(alias="ietf-netconf:config-target")
    ]


class EnumerationEnum(Enum):
    """
    An enumeration.
    """

    int_0 = 0
    int_1 = 1
    int_2 = 2


class DefaultOperationLeaf(BaseModel):
    __root__: EnumerationEnum
    """
    The default operation to use.
    """


class EnumerationEnum2(Enum):
    """
    An enumeration.
    """

    int_0 = 0
    int_1 = 1
    int_2 = 2


class TestOptionLeaf(BaseModel):
    __root__: EnumerationEnum2
    """
    The test option to use.
    """


class EnumerationEnum3(Enum):
    """
    An enumeration.
    """

    int_0 = 0
    int_1 = 1
    int_2 = 2


class ErrorOptionLeaf(BaseModel):
    __root__: EnumerationEnum3
    """
    The error option to use.
    """


class Config(BaseModel):
    """
    Inline Config content.
    """


class ConfigCase(BaseModel):
    config: Config


class UriType(BaseModel):
    __root__: str
    """
    The uri type represents a Uniform Resource Identifier
    (URI) as defined by STD 66.

    Objects using the uri type MUST be in US-ASCII encoding,
    and MUST be normalized as described by RFC 3986 Sections
    6.2.1, 6.2.2.1, and 6.2.2.2.  All unnecessary
    percent-encoding is removed, and all case-insensitive
    characters are set to lowercase except for hexadecimal
    digits, which are normalized to uppercase as described in
    Section 6.2.2.1.

    The purpose of this normalization is to help provide
    unique URIs.  Note that this normalization is not
    sufficient to provide uniqueness.  Two URIs that are
    textually distinct after this normalization may still be
    equivalent.

    Objects using the uri type may restrict the schemes that
    they permit.  For example, 'data:' and 'urn:' schemes
    might not be appropriate.

    A zero-length URI is not a valid URI.  This can be used to
    express 'URI absent' where required.

    In the value set and its semantics, this type is equivalent
    to the Uri SMIv2 textual convention defined in RFC 5017.
    """


class UrlLeaf(BaseModel):
    __root__: UriType
    """
    URL-based config content.
    """


class UrlCase(BaseModel):
    url: Annotated[Optional[UrlLeaf], Field(alias="ietf-netconf:url")] = None
    """
    URL-based config content.
    """


class Input2(BaseModel):
    target: Annotated[
        Optional[TargetContainer], Field(alias="ietf-netconf:target")
    ] = None
    default_operation: Annotated[
        DefaultOperationLeaf, Field(alias="ietf-netconf:default-operation")
    ] = "merge"
    """
    The default operation to use.
    """
    test_option: Annotated[
        TestOptionLeaf, Field(alias="ietf-netconf:test-option")
    ] = "test-then-set"
    """
    The test option to use.
    """
    error_option: Annotated[
        ErrorOptionLeaf, Field(alias="ietf-netconf:error-option")
    ] = "stop-on-error"
    """
    The error option to use.
    """
    edit_content: Annotated[
        Union[ConfigCase, UrlCase], Field(alias="ietf-netconf:edit-content")
    ]


class EditConfigRpc(BaseModel):
    """
    The <edit-config> operation loads all or part of a specified
    configuration to the specified target configuration.
    """

    output: Output2
    input: Input2


class Output3(BaseModel):
    pass


class CandidateLeaf3(BaseModel):
    """
    The candidate configuration is the config target.
    """


class CandidateCase3(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf3], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config target.
    """


class RunningLeaf3(BaseModel):
    """
    The running configuration is the config target.
    This is optional-to-implement on the server.
    """


class RunningCase3(BaseModel):
    running: Annotated[
        Optional[RunningLeaf3], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config target.
    This is optional-to-implement on the server.
    """


class StartupLeaf2(BaseModel):
    """
    The startup configuration is the config target.
    """


class StartupCase2(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf2], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config target.
    """


class UrlLeaf2(BaseModel):
    __root__: UriType
    """
    The URL-based configuration is the config target.
    """


class UrlCase2(BaseModel):
    url: Annotated[Optional[UrlLeaf2], Field(alias="ietf-netconf:url")] = None
    """
    The URL-based configuration is the config target.
    """


class TargetContainer2(BaseModel):
    """
    Particular configuration to copy to.
    """

    config_target: Annotated[
        Union[CandidateCase3, RunningCase3, StartupCase2, UrlCase2],
        Field(alias="ietf-netconf:config-target"),
    ]


class CandidateLeaf4(BaseModel):
    """
    The candidate configuration is the config source.
    """


class CandidateCase4(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf4], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config source.
    """


class RunningLeaf4(BaseModel):
    """
    The running configuration is the config source.
    """


class RunningCase4(BaseModel):
    running: Annotated[
        Optional[RunningLeaf4], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config source.
    """


class StartupLeaf3(BaseModel):
    """
    The startup configuration is the config source.
    """


class StartupCase3(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf3], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config source.
    """


class UrlLeaf3(BaseModel):
    __root__: UriType
    """
    The URL-based configuration is the config source.
    """


class UrlCase3(BaseModel):
    url: Annotated[Optional[UrlLeaf3], Field(alias="ietf-netconf:url")] = None
    """
    The URL-based configuration is the config source.
    """


class Config2(BaseModel):
    """
    Inline Config content: <config> element.  Represents
    an entire configuration datastore, not
    a subset of the running datastore.
    """


class ConfigCase2(BaseModel):
    config: Config2


class SourceContainer2(BaseModel):
    """
    Particular configuration to copy from.
    """

    config_source: Annotated[
        Union[CandidateCase4, RunningCase4, StartupCase3, UrlCase3, ConfigCase2],
        Field(alias="ietf-netconf:config-source"),
    ]


class Input3(BaseModel):
    target: Annotated[
        Optional[TargetContainer2], Field(alias="ietf-netconf:target")
    ] = None
    source: Annotated[
        Optional[SourceContainer2], Field(alias="ietf-netconf:source")
    ] = None


class CopyConfigRpc(BaseModel):
    """
    Create or replace an entire configuration datastore with the
    contents of another complete configuration datastore.
    """

    output: Output3
    input: Input3


class Output4(BaseModel):
    pass


class StartupLeaf4(BaseModel):
    """
    The startup configuration is the config target.
    """


class StartupCase4(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf4], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config target.
    """


class UrlLeaf4(BaseModel):
    __root__: UriType
    """
    The URL-based configuration is the config target.
    """


class UrlCase4(BaseModel):
    url: Annotated[Optional[UrlLeaf4], Field(alias="ietf-netconf:url")] = None
    """
    The URL-based configuration is the config target.
    """


class TargetContainer3(BaseModel):
    """
    Particular configuration to delete.
    """

    config_target: Annotated[
        Union[StartupCase4, UrlCase4], Field(alias="ietf-netconf:config-target")
    ]


class Input4(BaseModel):
    target: Annotated[
        Optional[TargetContainer3], Field(alias="ietf-netconf:target")
    ] = None


class DeleteConfigRpc(BaseModel):
    """
    Delete a configuration datastore.
    """

    output: Output4
    input: Input4


class Output5(BaseModel):
    pass


class CandidateLeaf5(BaseModel):
    """
    The candidate configuration is the config target.
    """


class CandidateCase5(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf5], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config target.
    """


class RunningLeaf5(BaseModel):
    """
    The running configuration is the config target.
    """


class RunningCase5(BaseModel):
    running: Annotated[
        Optional[RunningLeaf5], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config target.
    """


class StartupLeaf5(BaseModel):
    """
    The startup configuration is the config target.
    """


class StartupCase5(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf5], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config target.
    """


class TargetContainer4(BaseModel):
    """
    Particular configuration to lock.
    """

    config_target: Annotated[
        Union[CandidateCase5, RunningCase5, StartupCase5],
        Field(alias="ietf-netconf:config-target"),
    ]


class Input5(BaseModel):
    target: Annotated[
        Optional[TargetContainer4], Field(alias="ietf-netconf:target")
    ] = None


class LockRpc(BaseModel):
    """
    The lock operation allows the client to lock the configuration
    system of a device.
    """

    output: Output5
    input: Input5


class Output6(BaseModel):
    pass


class CandidateLeaf6(BaseModel):
    """
    The candidate configuration is the config target.
    """


class CandidateCase6(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf6], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config target.
    """


class RunningLeaf6(BaseModel):
    """
    The running configuration is the config target.
    """


class RunningCase6(BaseModel):
    running: Annotated[
        Optional[RunningLeaf6], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config target.
    """


class StartupLeaf6(BaseModel):
    """
    The startup configuration is the config target.
    """


class StartupCase6(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf6], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config target.
    """


class TargetContainer5(BaseModel):
    """
    Particular configuration to unlock.
    """

    config_target: Annotated[
        Union[CandidateCase6, RunningCase6, StartupCase6],
        Field(alias="ietf-netconf:config-target"),
    ]


class Input6(BaseModel):
    target: Annotated[
        Optional[TargetContainer5], Field(alias="ietf-netconf:target")
    ] = None


class UnlockRpc(BaseModel):
    """
    The unlock operation is used to release a configuration lock,
    previously obtained with the 'lock' operation.
    """

    output: Output6
    input: Input6


class Filter2(BaseModel):
    """
    This parameter specifies the portion of the system
    configuration and state data to retrieve.
    """


class Input7(BaseModel):
    filter: Filter2


class Data2(BaseModel):
    """
    Copy of the running datastore subset and/or state
    data that matched the filter criteria (if any).
    An empty data container indicates that the request did not
    produce any results.
    """


class Output7(BaseModel):
    data: Data2


class GetRpc(BaseModel):
    """
    Retrieve running configuration and device state information.
    """

    input: Input7
    output: Output7


class Input8(BaseModel):
    pass


class Output8(BaseModel):
    pass


class CloseSessionRpc(BaseModel):
    """
    Request graceful termination of a NETCONF session.
    """

    input: Input8
    output: Output8


class Output9(BaseModel):
    pass


class SessionIdTypeType(BaseModel):
    __root__: Annotated[int, Field(ge=1, le=4294967295)]
    """
    NETCONF Session Id
    """


class SessionIdLeaf(BaseModel):
    __root__: SessionIdTypeType
    """
    Particular session to kill.
    """


class Input9(BaseModel):
    session_id: Annotated[SessionIdLeaf, Field(alias="ietf-netconf:session-id")]
    """
    Particular session to kill.
    """


class KillSessionRpc(BaseModel):
    """
    Force the termination of a NETCONF session.
    """

    output: Output9
    input: Input9


class Output10(BaseModel):
    pass


class ConfirmedLeaf(BaseModel):
    """
    Requests a confirmed commit.
    """


class ConfirmTimeoutLeaf(BaseModel):
    __root__: Annotated[int, Field(ge=1, le=4294967295)]
    """
    The timeout interval for a confirmed commit.
    """


class PersistLeaf(BaseModel):
    __root__: str
    """
    This parameter is used to make a confirmed commit
    persistent.  A persistent confirmed commit is not aborted
    if the NETCONF session terminates.  The only way to abort
    a persistent confirmed commit is to let the timer expire,
    or to use the <cancel-commit> operation.

    The value of this parameter is a token that must be given
    in the 'persist-id' parameter of <commit> or
    <cancel-commit> operations in order to confirm or cancel
    the persistent confirmed commit.

    The token should be a random string.
    """


class PersistIdLeaf(BaseModel):
    __root__: str
    """
    This parameter is given in order to commit a persistent
    confirmed commit.  The value must be equal to the value
    given in the 'persist' parameter to the <commit> operation.
    If it does not match, the operation fails with an
    'invalid-value' error.
    """


class Input10(BaseModel):
    confirmed: Annotated[
        Optional[ConfirmedLeaf], Field(alias="ietf-netconf:confirmed")
    ] = None
    """
    Requests a confirmed commit.
    """
    confirm_timeout: Annotated[
        ConfirmTimeoutLeaf, Field(alias="ietf-netconf:confirm-timeout")
    ] = 600
    """
    The timeout interval for a confirmed commit.
    """
    persist: Annotated[
        Optional[PersistLeaf], Field(alias="ietf-netconf:persist")
    ] = None
    """
    This parameter is used to make a confirmed commit
    persistent.  A persistent confirmed commit is not aborted
    if the NETCONF session terminates.  The only way to abort
    a persistent confirmed commit is to let the timer expire,
    or to use the <cancel-commit> operation.

    The value of this parameter is a token that must be given
    in the 'persist-id' parameter of <commit> or
    <cancel-commit> operations in order to confirm or cancel
    the persistent confirmed commit.

    The token should be a random string.
    """
    persist_id: Annotated[
        Optional[PersistIdLeaf], Field(alias="ietf-netconf:persist-id")
    ] = None
    """
    This parameter is given in order to commit a persistent
    confirmed commit.  The value must be equal to the value
    given in the 'persist' parameter to the <commit> operation.
    If it does not match, the operation fails with an
    'invalid-value' error.
    """


class CommitRpc(BaseModel):
    """
    Commit the candidate configuration as the device's new
    current configuration.
    """

    output: Output10
    input: Input10


class Input11(BaseModel):
    pass


class Output11(BaseModel):
    pass


class DiscardChangesRpc(BaseModel):
    """
    Revert the candidate configuration to the current
    running configuration.
    """

    input: Input11
    output: Output11


class Output12(BaseModel):
    pass


class PersistIdLeaf2(BaseModel):
    __root__: str
    """
    This parameter is given in order to cancel a persistent
    confirmed commit.  The value must be equal to the value
    given in the 'persist' parameter to the <commit> operation.
    If it does not match, the operation fails with an
    'invalid-value' error.
    """


class Input12(BaseModel):
    persist_id: Annotated[
        Optional[PersistIdLeaf2], Field(alias="ietf-netconf:persist-id")
    ] = None
    """
    This parameter is given in order to cancel a persistent
    confirmed commit.  The value must be equal to the value
    given in the 'persist' parameter to the <commit> operation.
    If it does not match, the operation fails with an
    'invalid-value' error.
    """


class CancelCommitRpc(BaseModel):
    """
    This operation is used to cancel an ongoing confirmed commit.
    If the confirmed commit is persistent, the parameter
    'persist-id' must be given, and it must match the value of the
    'persist' parameter.
    """

    output: Output12
    input: Input12


class Output13(BaseModel):
    pass


class CandidateLeaf7(BaseModel):
    """
    The candidate configuration is the config source.
    """


class CandidateCase7(BaseModel):
    candidate: Annotated[
        Optional[CandidateLeaf7], Field(alias="ietf-netconf:candidate")
    ] = None
    """
    The candidate configuration is the config source.
    """


class RunningLeaf7(BaseModel):
    """
    The running configuration is the config source.
    """


class RunningCase7(BaseModel):
    running: Annotated[
        Optional[RunningLeaf7], Field(alias="ietf-netconf:running")
    ] = None
    """
    The running configuration is the config source.
    """


class StartupLeaf7(BaseModel):
    """
    The startup configuration is the config source.
    """


class StartupCase7(BaseModel):
    startup: Annotated[
        Optional[StartupLeaf7], Field(alias="ietf-netconf:startup")
    ] = None
    """
    The startup configuration is the config source.
    """


class UrlLeaf5(BaseModel):
    __root__: UriType
    """
    The URL-based configuration is the config source.
    """


class UrlCase5(BaseModel):
    url: Annotated[Optional[UrlLeaf5], Field(alias="ietf-netconf:url")] = None
    """
    The URL-based configuration is the config source.
    """


class Config3(BaseModel):
    """
    Inline Config content: <config> element.  Represents
    an entire configuration datastore, not
    a subset of the running datastore.
    """


class ConfigCase3(BaseModel):
    config: Config3


class SourceContainer3(BaseModel):
    """
    Particular configuration to validate.
    """

    config_source: Annotated[
        Union[CandidateCase7, RunningCase7, StartupCase7, UrlCase5, ConfigCase3],
        Field(alias="ietf-netconf:config-source"),
    ]


class Input13(BaseModel):
    source: Annotated[
        Optional[SourceContainer3], Field(alias="ietf-netconf:source")
    ] = None


class ValidateRpc(BaseModel):
    """
    Validates the contents of the specified configuration.
    """

    output: Output13
    input: Input13


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
    - `exclude_defaults=True` omits fields set to their default value (recommended)
    - `by_alias=True` ensures qualified names are used (necessary)
    """

    get_config: Annotated[GetConfigRpc, Field(alias="get-config")]
    edit_config: Annotated[EditConfigRpc, Field(alias="edit-config")]
    copy_config: Annotated[CopyConfigRpc, Field(alias="copy-config")]
    delete_config: Annotated[DeleteConfigRpc, Field(alias="delete-config")]
    lock: LockRpc
    unlock: UnlockRpc
    get: GetRpc
    close_session: Annotated[CloseSessionRpc, Field(alias="close-session")]
    kill_session: Annotated[KillSessionRpc, Field(alias="kill-session")]
    commit: CommitRpc
    discard_changes: Annotated[DiscardChangesRpc, Field(alias="discard-changes")]
    cancel_commit: Annotated[CancelCommitRpc, Field(alias="cancel-commit")]
    validate_: ValidateRpc


from pydantic import BaseConfig, Extra

BaseConfig.allow_population_by_field_name = True
BaseConfig.smart_union = True  # See Pydantic issue#2135 / pull#2092
BaseConfig.extra = Extra.forbid


if __name__ == "__main__":
    model = Model(
        # <Initialize model here>
    )

    restconf_payload = model.json(exclude_defaults=True, by_alias=True, indent=2)

    print(f"Generated output: {restconf_payload}")

    # Send config to network device:
    # from pydantify.utility import restconf_patch_request
    # restconf_patch_request(url='...', user_pw_auth=('usr', 'pw'), data=restconf_payload)
