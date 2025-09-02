from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RuleStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RULE_STATUS_UNSPECIFIED: _ClassVar[RuleStatus]
    RULE_STATUS_SUCCESS: _ClassVar[RuleStatus]
    RULE_STATUS_FAILURE: _ClassVar[RuleStatus]
    RULE_STATUS_RETRY: _ClassVar[RuleStatus]
    RULE_STATUS_SKIP: _ClassVar[RuleStatus]
RULE_STATUS_UNSPECIFIED: RuleStatus
RULE_STATUS_SUCCESS: RuleStatus
RULE_STATUS_FAILURE: RuleStatus
RULE_STATUS_RETRY: RuleStatus
RULE_STATUS_SKIP: RuleStatus

class IdentifyRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IdentifyResponse(_message.Message):
    __slots__ = ("name", "version", "rules")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RULES_FIELD_NUMBER: _ClassVar[int]
    name: str
    version: str
    rules: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., version: _Optional[str] = ..., rules: _Optional[_Iterable[str]] = ...) -> None: ...

class HelpRequest(_message.Message):
    __slots__ = ("request_id", "rule")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    rule: str
    def __init__(self, request_id: _Optional[str] = ..., rule: _Optional[str] = ...) -> None: ...

class HelpResponse(_message.Message):
    __slots__ = ("short", "long")
    SHORT_FIELD_NUMBER: _ClassVar[int]
    LONG_FIELD_NUMBER: _ClassVar[int]
    short: str
    long: str
    def __init__(self, short: _Optional[str] = ..., long: _Optional[str] = ...) -> None: ...

class EvaluateRequest(_message.Message):
    __slots__ = ("request_id", "rule", "params")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RULE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    rule: str
    params: _containers.ScalarMap[str, str]
    def __init__(self, request_id: _Optional[str] = ..., rule: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ("id", "metadata")
    class MetadataEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    metadata: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., metadata: _Optional[_Mapping[str, str]] = ...) -> None: ...

class EvaluateResponse(_message.Message):
    __slots__ = ("status", "message", "params", "items")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    status: RuleStatus
    message: str
    params: _containers.ScalarMap[str, str]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, status: _Optional[_Union[RuleStatus, str]] = ..., message: _Optional[str] = ..., params: _Optional[_Mapping[str, str]] = ..., items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class InsertRequest(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[Item]
    def __init__(self, items: _Optional[_Iterable[_Union[Item, _Mapping]]] = ...) -> None: ...

class InsertResponse(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...
