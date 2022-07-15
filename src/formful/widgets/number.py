from formful.widgets.meta import Input


class NumberInput(Input):
    """
    Renders an input with type "number".
    """

    input_type = "number"
    validation_attrs = ["required", "max", "min", "step"]

    def __init__(self, step=None, min=None, max=None):
        self.step = step
        self.min = min
        self.max = max

    def __call__(self, field, **kwargs):
        if self.step is not None:
            kwargs.setdefault("step", self.step)
        if self.min is not None:
            kwargs.setdefault("min", self.min)
        if self.max is not None:
            kwargs.setdefault("max", self.max)
        return super().__call__(field, **kwargs)


class RangeInput(Input):
    """
    Renders an input with type "range".
    """

    input_type = "range"
    validation_attrs = ["required", "max", "min", "step"]

    def __init__(self, step=None):
        self.step = step

    def __call__(self, field, **kwargs):
        if self.step is not None:
            kwargs.setdefault("step", self.step)
        return super().__call__(field, **kwargs)
