class DummyTranslations:

    def gettext(self, string, target_language=None):
        return string

    def ngettext(self, singular, plural, n, target_language=None):
        if n == 1:
            return singular

        return plural
