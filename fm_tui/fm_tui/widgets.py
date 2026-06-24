"""Plain fallback widgets — fm_tui's look when nish-tui is not installed.

These twins mirror the nish-tui widget API (``Header(title)``,
``BorderedPanel(..., title=)``, ``LogView.log_line(severity, message)``) so the
theming layer can swap one set for the other without touching the app. They
carry the First Motive palette (:mod:`fm_tui.palette`), so fm_tui stays on-brand
and readable even bare.
"""

from __future__ import annotations

from rich.text import Text
from textual.containers import Container
from textual.widgets import RichLog, Static

from fm_tui.palette import CREAM, LILAC, PLUM, SAND, SEVERITY


class Header(Static):
    """Branded title bar."""

    DEFAULT_CSS = f"""
    Header {{
        color: {CREAM};
        background: {PLUM};
        text-style: bold;
        height: 1;
        padding: 0 1;
    }}
    """

    def __init__(self, title: str = "", **kwargs) -> None:
        super().__init__(title, **kwargs)


class BorderedPanel(Container):
    """Titled container with a heavy lilac border and an uppercase brand title."""

    DEFAULT_CSS = f"""
    BorderedPanel {{
        border: heavy {LILAC};
        border-title-color: {SAND};
        height: auto;
        padding: 0 1;
    }}
    """

    def __init__(self, *children, title: str = "", **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.border_title = title.upper()


class LogView(RichLog):
    """Scrolling log; colours lines by severity from the FM palette."""

    DEFAULT_CSS = """
    LogView {
        height: 1fr;
    }
    """

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("markup", False)
        kwargs.setdefault("wrap", True)
        super().__init__(**kwargs)

    def _build_line(self, severity: str, message: str) -> Text:
        _glyph, colour = SEVERITY.get(severity.lower(), ("·", CREAM))
        line = Text()
        line.append(f"{severity.upper():<5} ", style=f"bold {colour}")
        line.append(message, style=colour)
        return line

    def log_line(self, severity: str, message: str) -> None:
        self.write(self._build_line(severity, message))
