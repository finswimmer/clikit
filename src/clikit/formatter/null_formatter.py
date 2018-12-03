from typing import Optional

from clikit.api.formatter import Formatter


class NullFormatter(Formatter):
    """
    A formatter that returns all text unchanged.
    """

    def format(self, string, style=None):  # type: (str, Optional[Style]) -> str
        return string

    def remove_format(self, string):  # type: (str) -> str
        return string