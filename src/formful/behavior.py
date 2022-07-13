from formful.widgets.core import clean_key


class CSRF:

    csrf = False
    csrf_field_name = "csrf_token"
    csrf_secret = None
    csrf_context = None
    csrf_class = None

    def build_csrf(self, form):
        """
        Build a CSRF implementation. This is called once per form instance.
        The default implementation builds the class referenced to by
        :attr:`csrf_class` with zero arguments. If `csrf_class` is ``None``,
        will instead use the default implementation
        :class:`wtforms.csrf.session.SessionCSRF`.
        :param form: The form.
        :return: A CSRF implementation.
        """
        if self.csrf_class is not None:
            return self.csrf_class()

        from wtforms.csrf.session import SessionCSRF

        return SessionCSRF()


class Behavior:

    def bind_field(self, form, unbound_field, options):
        return unbound_field.bind(form=form, **options)

    def render_field(self, field, render_kw):
        render_kw = {clean_key(k): v for k, v in render_kw.items()}
        other_kw = getattr(field, "render_kw", None)
        if other_kw is not None:
            other_kw = {clean_key(k): v for k, v in other_kw.items()}
            render_kw = {**other_kw, **render_kw}
        return field.widget(field, **render_kw)

    def render_form(self, form):
        html = ''
        for field in form:
            html += field()
        return html




DEFAULT_BEHAVIOR = Behavior()
