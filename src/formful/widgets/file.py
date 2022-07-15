from formful.widgets.meta import Input


class FileInput(Input):
    """Render a file chooser input.
    :param multiple: allow choosing multiple files
    """

    input_type = "file"
    validation_attrs = ["required", "accept"]

    def __init__(self, multiple=False):
        super().__init__()
        self.multiple = multiple

    def __call__(self, field, **kwargs):
        # browser ignores value of file input for security
        kwargs["value"] = False

        if self.multiple:
            kwargs["multiple"] = True

        return super().__call__(field, **kwargs)
