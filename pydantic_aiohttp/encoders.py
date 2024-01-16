# This code was taken from https://github.com/tiangolo/fastapi
# Thanks to @tiangolo for implementing it
import dataclasses
import datetime
from collections import defaultdict
from collections import deque
from decimal import Decimal
from enum import Enum
from ipaddress import IPv4Address
from ipaddress import IPv4Interface
from ipaddress import IPv4Network
from ipaddress import IPv6Address
from ipaddress import IPv6Interface
from ipaddress import IPv6Network
from pathlib import Path
from pathlib import PurePath
from re import Pattern
from types import GeneratorType
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Type
from typing import Union
from uuid import UUID

from pydantic import BaseModel
from pydantic.color import Color
from pydantic.networks import AnyUrl
from pydantic.networks import NameEmail
from pydantic.types import SecretBytes
from pydantic.types import SecretStr

IncEx = Union[Set[int], Set[str], Dict[int, Any], Dict[str, Any]]


def _model_dump(
        model: BaseModel, mode: Literal["json", "python"] = "json", **kwargs: Any
) -> Any:
    return model.model_dump(mode=mode, **kwargs)


# Taken from Pydantic v1 as is
def isoformat(o: Union[datetime.date, datetime.time]) -> str:
    return o.isoformat()


# Taken from Pydantic v1 as is
# TODO: pv2 should this return strings instead?
def decimal_encoder(dec_value: Decimal) -> Union[int, float]:
    """
    Encodes a Decimal as int of there's no exponent, otherwise float

    This is useful when we use ConstrainedDecimal to represent Numeric(x,0)
    where an integer (but not int typed) is used. Encoding this as a float
    results in failed round-tripping between encode and parse.
    Our ID type is a prime example of this.

    >>> decimal_encoder(Decimal("1.0"))
    1.0

    >>> decimal_encoder(Decimal("1"))
    1
    """
    if dec_value.as_tuple().exponent >= 0:  # type: ignore[operator]
        return int(dec_value)
    else:
        return float(dec_value)


ENCODERS_BY_TYPE: Dict[Type[Any], Callable[[Any], Any]] = {
    bytes: lambda o: o.decode(),
    Color: str,
    datetime.date: isoformat,
    datetime.datetime: isoformat,
    datetime.time: isoformat,
    datetime.timedelta: lambda td: td.total_seconds(),
    Decimal: decimal_encoder,
    Enum: lambda o: o.value,
    frozenset: list,
    deque: list,
    GeneratorType: list,
    IPv4Address: str,
    IPv4Interface: str,
    IPv4Network: str,
    IPv6Address: str,
    IPv6Interface: str,
    IPv6Network: str,
    NameEmail: str,
    Path: str,
    Pattern: lambda o: o.pattern,
    SecretBytes: str,
    SecretStr: str,
    set: list,
    UUID: str,
    AnyUrl: str,
}


def generate_encoders_by_class_tuples(
        type_encoder_map: Dict[Any, Callable[[Any], Any]]
) -> Dict[Callable[[Any], Any], Tuple[Any, ...]]:
    _encoders_by_class_tuples: Dict[Callable[[Any], Any], Tuple[Any, ...]] = defaultdict(tuple)
    for type_, encoder in type_encoder_map.items():
        _encoders_by_class_tuples[encoder] += (type_,)
    return _encoders_by_class_tuples


encoders_by_class_tuples = generate_encoders_by_class_tuples(ENCODERS_BY_TYPE)


def jsonable_encoder(
        obj: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        custom_encoder: Optional[Dict[Any, Callable[[Any], Any]]] = None,
        sqlalchemy_safe: bool = True,
) -> Any:
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)
    if isinstance(obj, BaseModel):
        encoders: Dict[Any, Any] = {}
        obj_dict = _model_dump(
            obj,
            mode="json",
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        if "__root__" in obj_dict:
            obj_dict = obj_dict["__root__"]
        return jsonable_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            # TODO: remove when deprecating Pydantic v1
            custom_encoder=encoders,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if dataclasses.is_dataclass(obj):
        obj_dict = dataclasses.asdict(obj)
        return jsonable_encoder(
            obj_dict,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            custom_encoder=custom_encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, (str, int, float, type(None))):
        return obj
    if isinstance(obj, dict):
        encoded_dict = {}
        allowed_keys = set(obj.keys())
        if include is not None:
            allowed_keys &= set(include)
        if exclude is not None:
            allowed_keys -= set(exclude)
        for key, value in obj.items():
            if (
                    (
                            not sqlalchemy_safe
                            or (not isinstance(key, str))
                            or (not key.startswith("_sa"))
                    )
                    and (value is not None or not exclude_none)
                    and key in allowed_keys
            ):
                encoded_key = jsonable_encoder(
                    key,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = jsonable_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                jsonable_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)

    try:
        data = dict(obj)
    except Exception as e:
        errors: List[Exception] = [e]
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors) from e

    return jsonable_encoder(
        data,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )


# noinspection DuplicatedCode
def url_compatible_encoder(
        obj: Any,
        include: Optional[IncEx] = None,
        exclude: Optional[IncEx] = None,
        by_alias: bool = True,
        exclude_unset: bool = True,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        custom_encoder: Optional[Dict[Any, Callable[[Any], Any]]] = None,
        sqlalchemy_safe: bool = True,
) -> str | list[str] | dict[str, str | list[str]]:
    custom_encoder = custom_encoder or {}
    if custom_encoder:
        if type(obj) in custom_encoder:
            return custom_encoder[type(obj)](obj)
        else:
            for encoder_type, encoder_instance in custom_encoder.items():
                if isinstance(obj, encoder_type):
                    return encoder_instance(obj)
    if include is not None and not isinstance(include, (set, dict)):
        include = set(include)
    if exclude is not None and not isinstance(exclude, (set, dict)):
        exclude = set(exclude)
    if isinstance(obj, BaseModel):
        encoders: Dict[Any, Any] = {}
        obj_dict = _model_dump(
            obj,
            mode="json",
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
        )
        if "__root__" in obj_dict:
            obj_dict = obj_dict["__root__"]
        return url_compatible_encoder(
            obj_dict,
            exclude_none=exclude_none,
            exclude_defaults=exclude_defaults,
            # TODO: remove when deprecating Pydantic v1
            custom_encoder=encoders,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if dataclasses.is_dataclass(obj):
        obj_dict = dataclasses.asdict(obj)
        return url_compatible_encoder(
            obj_dict,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
            custom_encoder=custom_encoder,
            sqlalchemy_safe=sqlalchemy_safe,
        )
    if isinstance(obj, Enum):
        return obj.value
    if isinstance(obj, PurePath):
        return str(obj)
    if isinstance(obj, type(None)):
        return ""
    if isinstance(obj, str):
        return obj
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, dict):
        encoded_dict = {}
        allowed_keys = set(obj.keys())
        if include is not None:
            allowed_keys &= set(include)
        if exclude is not None:
            allowed_keys -= set(exclude)
        for key, value in obj.items():
            if (
                    (
                            not sqlalchemy_safe
                            or (not isinstance(key, str))
                            or (not key.startswith("_sa"))
                    )
                    and (value is not None or not exclude_none)
                    and key in allowed_keys
            ):
                encoded_key = url_compatible_encoder(
                    key,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
                encoded_value = url_compatible_encoder(
                    value,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )

                if not bool(encoded_key):
                    # '' or None
                    continue

                encoded_dict[encoded_key] = encoded_value
        return encoded_dict
    if isinstance(obj, (list, set, frozenset, GeneratorType, tuple, deque)):
        encoded_list = []
        for item in obj:
            encoded_list.append(
                url_compatible_encoder(
                    item,
                    include=include,
                    exclude=exclude,
                    by_alias=by_alias,
                    exclude_unset=exclude_unset,
                    exclude_defaults=exclude_defaults,
                    exclude_none=exclude_none,
                    custom_encoder=custom_encoder,
                    sqlalchemy_safe=sqlalchemy_safe,
                )
            )
        return encoded_list

    if type(obj) in ENCODERS_BY_TYPE:
        return ENCODERS_BY_TYPE[type(obj)](obj)
    for encoder, classes_tuple in encoders_by_class_tuples.items():
        if isinstance(obj, classes_tuple):
            return encoder(obj)

    try:
        data = dict(obj)
    except Exception as e:
        errors: List[Exception] = [e]
        try:
            data = vars(obj)
        except Exception as e:
            errors.append(e)
            raise ValueError(errors) from e

    return url_compatible_encoder(
        data,
        include=include,
        exclude=exclude,
        by_alias=by_alias,
        exclude_unset=exclude_unset,
        exclude_defaults=exclude_defaults,
        exclude_none=exclude_none,
        custom_encoder=custom_encoder,
        sqlalchemy_safe=sqlalchemy_safe,
    )
