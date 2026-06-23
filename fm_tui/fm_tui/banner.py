"""FM-branded terminal banners — the colour-coded step rules run.sh paints with.

run.sh narrates each launch step (install OrbStack, bring the container up, build
the workspace, open the TUI). This module renders each step as a full-width rule
in the First Motive palette so the steps read at a glance instead of scrolling by
as plain ``>>`` lines.

It is deliberately pure stdlib + ANSI truecolour: the first run.sh steps fire on
the host before the container exists, so the renderer cannot depend on ROS,
Textual, or the image. Any host ``python3`` can run it by file path, and the
palette lives here once so run.sh and the TUI share one source of brand colour
(it mirrors ``docs/diagrams/styles.d2``).

    python3 src/fm-app/fm_tui/fm_tui/banner.py "bringing container up"
    python3 src/fm-app/fm_tui/fm_tui/banner.py "Foxglove: ws://localhost:8765" info
"""

from __future__ import annotations

import os
import shutil
import sys

# First Motive palette (truecolour RGB) — mirrors docs/diagrams/styles.d2.
PLUM = (59, 52, 67)  # #3B3443
LILAC = (182, 165, 198)  # #B6A5C6
SAND = (231, 221, 200)  # #E7DDC8
CREAM = (236, 226, 207)  # #ECE2CF

# Role -> rule colour. ``step`` is an active launch step; ``info`` a secondary
# note (endpoints, teardown hint); ``done`` a completed milestone.
ROLES = {
    "step": LILAC,
    "info": SAND,
    "done": CREAM,
}

_GLYPH = "━"  # rule fill glyph (heavy horizontal box-drawing)
_RESET = "\x1b[0m"  # clear all styling
_BOLD = "\x1b[1m"  # bold the label


def _fg(rgb: tuple[int, int, int]) -> str:
    """ANSI 24-bit foreground escape (``38;2;r;g;b``) for an ``(r, g, b)`` triple."""
    r, g, b = rgb
    return f"\x1b[38;2;{r};{g};{b}m"


def supports_colour(stream=sys.stdout) -> bool:
    """True when ``stream`` is a TTY that should get ANSI colour.

    Honours the ``NO_COLOR`` convention and a ``dumb`` terminal so the banner
    degrades to plain text in pipes, logs, and CI.
    """
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return bool(getattr(stream, "isatty", lambda: False)())


def render(message: str, role: str = "step", *, columns: int = 0, colour: bool = True) -> str:
    """Return a full-width banner line: ``▸ message ━━━━…`` in the role colour.

    ``columns`` overrides the detected terminal width (0 = auto-detect). With
    ``colour`` false, returns the same layout using ASCII dashes and no escapes.
    """
    width = columns or shutil.get_terminal_size((80, 20)).columns
    label = f"▸ {message} "
    fill = max(3, width - len(label))

    if not colour:
        return label + "-" * fill

    rgb = ROLES.get(role, LILAC)
    tint = _fg(rgb)
    return f"{_BOLD}{tint}{label}{_RESET}{tint}{_GLYPH * fill}{_RESET}"


def main(argv: list[str] | None = None) -> int:
    """CLI: ``banner.py <message> [role]`` — print one banner line."""
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: banner.py <message> [step|info|done]", file=sys.stderr)
        return 2
    message = args[0]
    role = args[1] if len(args) > 1 else "step"
    print(render(message, role, colour=supports_colour()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
