from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
RULE_STATUS_FAILURE: RuleStatus
RULE_STATUS_RETRY: RuleStatus
RULE_STATUS_SKIP: RuleStatus
RULE_STATUS_SUCCESS: RuleStatus
RULE_STATUS_UNSPECIFIED: RuleStatus

class EvaluateRequest(_message.Message):
    __slots__ = ["params", "rule"]
    class ParamsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    params: _containers.ScalarMap[str, str]
    rule: str
    def __init__(self, rule: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ...) -> None: ...

class EvaluateResponse(_message.Message):
    __slots__ = ["files", "message", "params", "status"]
    class ParamsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    FILES_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedScalarFieldContainer[str]
    message: str
    params: _containers.ScalarMap[str, str]
    status: RuleStatus
    def __init__(self, status: _Optional[_Union[RuleStatus, str]] = ..., message: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...

class IdentifyRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class IdentifyResponse(_message.Message):
    __slots__ = ["name", "rules", "version"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    name: str
    rules: _containers.RepeatedScalarFieldContainer[str]
    version: str
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., rules: _Optional[_Iterable[str]] = ...) -> None: ...

class InsertRequest(_message.Message):
    __slots__ = ["files"]
    FILES_FIELD_NUMBER: _ClassVar[int]
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, files: _Optional[_Iterable[str]] = ...) -> None: ...

class InsertResponse(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class RuleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
