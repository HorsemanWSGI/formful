import inspect
import typing
from collections import OrderedDict
from abc import ABCMeta


class Field:
    def __init__(self, title):
        self.title = title

    def __repr__(self):
        return f'<Field {self.title}>'


def get_fields(*bases: typing.Type):
    for cls in bases:
        for name, member in inspect.getmembers(cls, predicate=(
                lambda x: isinstance(x, Field))):
            yield name, member


class SchemaMeta(ABCMeta):

    def __new__(cls, name, bases, attrs):
        if '__fields' not in attrs:
            fields = OrderedDict(list(get_fields(*bases)))
            for attr, value in attrs.items():
                if isinstance(value, Field):
                    fields[attr] = value
            attrs['fields'] = fields
        return type.__new__(cls, name, bases, attrs)


class Schema(behaviorclass=SchemaMeta):
    pass


class Test(Schema):
    a = Field(1)
    b = Field(2)


class Test2(Test):
    a = Field(3)
    c = Field(4)


print(Test.fields, Test2.fields, Test.a, Test2.b)
