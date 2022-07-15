from markupsafe import escape


def clean_key(key):
    key = key.rstrip("_")
    if key.startswith("data_") or key.startswith("aria_"):
        key = key.replace("_", "-")
    return key


def html_params(**kwargs):
    """
    Generate HTML attribute syntax from inputted keyword arguments.
    The output value is sorted by the passed keys, to provide consistent output
    each time this function is called with the same parameters. Because of the
    frequent use of the normally reserved keywords `class` and `for`, suffixing
    these with an underscore will allow them to be used.
    In order to facilitate the use of ``data-`` and ``aria-`` attributes, if the
    name of the attribute begins with ``data_`` or ``aria_``, then every
    underscore will be replaced with a hyphen in the generated attribute.
    >>> html_params(data_attr='user.name', aria_labeledby='name')
    'data-attr="user.name" aria-labeledby="name"'
    In addition, the values ``True`` and ``False`` are special:
      * ``attr=True`` generates the HTML compact output of a boolean attribute,
        e.g. ``checked=True`` will generate simply ``checked``
      * ``attr=False`` will be ignored and generate no output.
    >>> html_params(name='text1', id='f', class_='text')
    'class="text" id="f" name="text1"'
    >>> html_params(checked=True, readonly=False, name="text1", abc="hello")
    'abc="hello" checked name="text1"'
    .. versionchanged:: 3.0
        ``aria_`` args convert underscores to hyphens like ``data_``
        args.
    .. versionchanged:: 2.2
        ``data_`` args convert all underscores to hyphens, instead of
        only the first one.
    """
    params = []
    for k, v in sorted(kwargs.items()):
        k = clean_key(k)
        if v is True:
            params.append(k)
        elif v is False:
            pass
        else:
            params.append('{}="{}"'.format(str(k), escape(v)))
    return " ".join(params)


class UnsetValue:
    """
    An unset value.
    This is used in situations where a blank value like `None` is acceptable
    usually as the default value of a class variable or function parameter
    (iow, usually when `None` is a valid value.)
    """

    def __str__(self):
        return "<unset value>"

    def __repr__(self):
        return "<unset value>"

    def __bool__(self):
        return False

    def __nonzero__(self):
        return False


unset_value = UnsetValue()
