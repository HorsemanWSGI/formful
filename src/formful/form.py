import itertools
import typing as t
from collections import OrderedDict
from formful.fields import Field, UnboundField
from formful.schema import Schema, SchemaMeta
from formful.behavior import Behavior, DEFAULT_BEHAVIOR
from formful.utils import unset_value


Fields = t.Mapping[str, UnboundField]


class Form:

    fields: Fields
    behavior: Behavior
    prefix: str
    form_errors: t.Iterable[str]
    extra_filters: t.Iterable

    def __init__(self,
                 fields: t.Optional[t.Union[Fields, Schema]] = None,
                 prefix="",
                 translations=None,
                 behavior=DEFAULT_BEHAVIOR,
                 extra_filters=None):

        self.form_errors = []
        if prefix:
            if prefix[-1] not in "-_;:/.":
                prefix += "-"
            self.prefix = prefix

        self.behavior = behavior
        self.prefix = prefix
        self.translations = None
        self.fields = OrderedDict()
        self.extra_filters = extra_filters

        if fields is not None:
            if isinstance(fields, SchemaMeta):
                fields = fields.get_fields()
            if not isinstance(fields, dict):
                raise NotImplementedError('Fields must be dict.')
            for name, unbound_field in fields.items():
                self[name] = unbound_field

    def __iter__(self):
        """Iterate form fields in creation order."""
        return iter(self.fields.values())

    def __contains__(self, name):
        """ Returns `True` if the named field is a member of this form. """
        return name in self.fields

    def __getitem__(self, name):
        """ Dict-style access to this form's fields."""
        return self.fields[name]

    def __setitem__(self, name, unbound_field):
        """ Bind a field to this form. """
        field_name = unbound_field.name or name
        options = {
            "name": field_name,
            "prefix": self.prefix,
            "translations": self.translations
        }
        self.fields[name] = self.behavior.bind_field(
            self, unbound_field, options
        )

    def __delitem__(self, name):
        """ Remove a field from this form. """
        del self.fields[name]

    def populate_obj(self, obj):
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields.
        :note: This is a destructive operation; Any attribute with the same name
               as a field will be overridden. Use with caution.
        """
        for name, field in self.fields.items():
            field.populate_obj(obj, name)

    def process(self, formdata=None, obj=None, data=None, extra_filters=None, **kwargs):
        """Process default and input data with each field.
        :param formdata: Input data coming from the client, usually
            ``request.form`` or equivalent. Should provide a "multi
            dict" interface to get a list of values for a given key,
            such as what Werkzeug, Django, and WebOb provide.
        :param obj: Take existing data from attributes on this object
            matching form field attributes. Only used if ``formdata`` is
            not passed.
        :param data: Take existing data from keys in this dict matching
            form field attributes. ``obj`` takes precedence if it also
            has a matching attribute. Only used if ``formdata`` is not
            passed.
        :param extra_filters: A dict mapping field attribute names to
            lists of extra filter functions to run. Extra filters run
            after filters passed when creating the field. If the form
            has ``filter_<fieldname>``, it is the last extra filter.
        :param kwargs: Merged with ``data`` to allow passing existing
            data as parameters. Overwrites any duplicate keys in
            ``data``. Only used if ``formdata`` is not passed.
        """
        if data is not None:
            kwargs = dict(data, **kwargs)

        filters = extra_filters.copy() if extra_filters is not None else {}

        for name, field in self.fields.items():
            field_extra_filters = filters.get(name, [])

            if self.extra_filters is not None and name in self.extra_filters:
                field_extra_filters.extend(self.extra_filters[name])

            if obj is not None and hasattr(obj, name):
                data = getattr(obj, name)
            elif name in kwargs:
                data = kwargs[name]
            else:
                data = unset_value

            field.process(formdata, data, extra_filters=field_extra_filters)

    def validate(self, extra_validators=None):
        """
        Validates the form by calling `validate` on each field.
        :param extra_validators:
            If provided, is a dict mapping field names to a sequence of
            callables which will be passed as extra validators to the field's
            `validate` method.
        Returns `True` if no errors occur.
        """
        success = True
        for name, field in self.fields.items():
            if extra_validators is not None and name in extra_validators:
                extra = extra_validators[name]
            else:
                extra = tuple()
            if not field.validate(self, extra):
                success = False
        return success

    @property
    def data(self):
        return {name: f.data for name, f in self.fields.items()}

    @property
    def errors(self):
        errors = {name: f.errors for name, f in self.fields.items() if f.errors}
        if self.form_errors:
            errors[None] = self.form_errors
        return errors

    def __call__(self):
        return self.behavior.render_form(self)
