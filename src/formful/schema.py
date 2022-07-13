import inspect
import typing
from abc import ABCMeta
from collections import OrderedDict
from formful.fields import UnboundField


def get_fields(*bases: typing.Type):
    for cls in bases:
        for name, member in inspect.getmembers(cls, predicate=(
                lambda x: isinstance(x, UnboundField))):
            yield name, member


class SchemaMeta(ABCMeta):

    def __new__(cls, name, bases, attrs):
        if not bases:
            # Enum itself
            return super().__new__(cls, name, bases, attrs)

        if '_fields' not in attrs:
            fields = OrderedDict(list(get_fields(*bases)))
            for attr, value in attrs.items():
                if isinstance(value, UnboundField):
                    if attr[0] != '_':
                        fields[attr] = value
            attrs['_fields'] = fields
            attrs = {name: attr for name, attr in attrs.items() if
                     name not in fields}
        return type.__new__(cls, name, bases, attrs)


class Schema(metaclass=SchemaMeta):

    @classmethod
    def get_fields(cls):
        return cls._fields
