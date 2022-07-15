from formful.widgets.meta import Input


class DateTimeInput(Input):
    """
    Renders an input with type "datetime".
    """

    input_type = "datetime"
    validation_attrs = ["required", "max", "min", "step"]


class DateInput(Input):
    """
    Renders an input with type "date".
    """

    input_type = "date"
    validation_attrs = ["required", "max", "min", "step"]


class MonthInput(Input):
    """
    Renders an input with type "month".
    """

    input_type = "month"
    validation_attrs = ["required", "max", "min", "step"]


class WeekInput(Input):
    """
    Renders an input with type "week".
    """

    input_type = "week"
    validation_attrs = ["required", "max", "min", "step"]


class TimeInput(Input):
    """
    Renders an input with type "time".
    """

    input_type = "time"
    validation_attrs = ["required", "max", "min", "step"]


class DateTimeLocalInput(Input):
    """
    Renders an input with type "datetime-local".
    """

    input_type = "datetime-local"
    validation_attrs = ["required", "max", "min", "step"]
