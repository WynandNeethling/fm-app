"""Fallback-widget tests: the plain twins carry the FM palette and brand title.

These exercise ``fm_tui.widgets`` directly (not through the theme resolver), so
they cover the bare look regardless of whether nish-tui is installed.
"""

from fm_tui import palette
from fm_tui.widgets import BorderedPanel, LogView


def test_border_title_is_uppercased():
    assert BorderedPanel(title="nodes").border_title == "NODES"


def test_log_line_colours_by_severity():
    line = LogView()._build_line("warn", "battery low")
    styles = " ".join(str(span.style) for span in line.spans)
    assert palette.AMBER in styles


def test_unknown_severity_falls_back_to_cream():
    line = LogView()._build_line("trace", "mystery")
    styles = " ".join(str(span.style) for span in line.spans)
    assert palette.CREAM in styles
