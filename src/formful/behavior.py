class Behavior:

    def bind_field(self, form, unbound_field, options):
        """
        bind_field allows potential customization of how fields are bound.
        The default implementation simply passes the options to
        :meth:`UnboundField.bind`.
        :param form: The form.
        :param unbound_field: The unbound field.
        :param options:
            A dictionary of options which are typically passed to the field.
        :return: A bound field
        """
        return unbound_field.bind(form=form, **options)

    def render_field(self, field, render_kw):
        """
        render_field allows customization of how widget rendering is done.
        The default implementation calls ``field.widget(field, **render_kw)``
        """

        render_kw = {clean_key(k): v for k, v in render_kw.items()}

        other_kw = getattr(field, "render_kw", None)
        if other_kw is not None:
            other_kw = {clean_key(k): v for k, v in other_kw.items()}
            render_kw = dict(other_kw, **render_kw)
        return field.widget(field, **render_kw)


DEFAULT_BEHAVIOR = Behavior()
