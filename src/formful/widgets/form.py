from markupsafe import Markup
from formful.utils import html_params


class TableWidget:
    """
    Renders a list of fields as a set of table rows with th/td pairs.
    If `with_table_tag` is True, then an enclosing <table> is placed around the
    rows.
    Hidden fields will not be displayed with a row, instead the field will be
    pushed into a subsequent table row to ensure XHTML validity. Hidden fields
    at the end of the field list will appear outside the table.
    """

    def __init__(self, with_table_tag=True):
        self.with_table_tag = with_table_tag

    def __call__(self, field, **kwargs):
        html = []
        if self.with_table_tag:
            kwargs.setdefault("id", field.id)
            html.append("<table %s>" % html_params(**kwargs))
        hidden = ""
        for subfield in field:
            if subfield.type in ("HiddenField", "CSRFTokenField"):
                hidden += str(subfield)
            else:
                html.append(
                    "<tr><th>%s</th><td>%s%s</td></tr>"
                    % (str(subfield.label), hidden, str(subfield))
                )
                hidden = ""
        if self.with_table_tag:
            html.append("</table>")
        if hidden:
            html.append(hidden)
        return Markup("".join(html))
