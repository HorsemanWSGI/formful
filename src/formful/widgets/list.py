from markupsafe import Markup
from formful.utils import html_params


class ListWidget:
    """
    Renders a list of fields as a `ul` or `ol` list.
    This is used for fields which encapsulate many inner fields as subfields.
    The widget will try to iterate the field to get access to the subfields and
    call them to render them.
    If `prefix_label` is set, the subfield's label is printed before the field,
    otherwise afterwards. The latter is useful for iterating radios or
    checkboxes.
    """

    def __init__(self, html_tag="ul", prefix_label=True):
        assert html_tag in ("ol", "ul")
        self.html_tag = html_tag
        self.prefix_label = prefix_label

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        html = ["<{} {}>".format(self.html_tag, html_params(**kwargs))]
        for subfield in field:
            if self.prefix_label:
                html.append(f"<li>{subfield.label} {subfield()}</li>")
            else:
                html.append(f"<li>{subfield()} {subfield.label}</li>")
        html.append("</%s>" % self.html_tag)
        return Markup("".join(html))
