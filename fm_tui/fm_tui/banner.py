"""FM-branded terminal banners — the colour-coded step rules run.sh paints with.

run.sh narrates each launch step (install OrbStack, bring the container up, build
the workspace, open the TUI). Each step renders as a three-row block — a rule, the
title, an optional description, another rule — in the First Motive palette so the
steps read at a glance instead of scrolling by as plain ``>>`` lines::

    ────────────────────────────────────────
    ▸ Building Workspace
      colcon build --symlink-install · incremental
    ────────────────────────────────────────

The rules are drawn by rich's ``Console.rule`` command, which fits the line to the
terminal width for us. The palette lives here once so run.sh and the TUI share one
source of brand colour (it mirrors ``docs/diagrams/styles.d2``).

rich is a fm_tui dependency (Textual already pulls it in). The first run.sh steps
fire on the host before the container exists, so run.sh runs this through
``uv run --with rich`` to get rich on the host too.

    python3 -m fm_tui.banner "Container Up" "compose up -d"
    python3 -m fm_tui.banner "Foxglove Studio" "ws://localhost:8765" info
"""

from __future__ import annotations

import sys

from rich.console import Console
from rich.style import Style
from rich.text import Text

# First Motive palette — mirrors docs/diagrams/styles.d2.
PLUM = "#3B3443"
LILAC = "#B6A5C6"
SAND = "#E7DDC8"
CREAM = "#ECE2CF"

# Role -> colour. ``step`` is an active launch step; ``info`` a secondary note
# (endpoints, teardown hint); ``done`` a completed milestone.
ROLES = {
    "step": LILAC,
    "info": SAND,
    "done": CREAM,
}


def emit(
    title: str,
    description: str = "",
    role: str = "step",
    *,
    console: Console | None = None,
) -> None:
    """Draw a banner block (rule / bold title / dim description / rule) to ``console``.

    ``description`` is optional — omit it for a two-row title-only block. Defaults
    to a stdout console, which auto-detects width, TTY, and ``NO_COLOR``.
    """
    console = console or Console()
    colour = ROLES.get(role, LILAC)
    console.rule(style=colour)
    console.print(Text(f"▸ {title}", style=Style(color=colour, bold=True)))
    if description:
        console.print(Text(f"  {description}", style=Style(color=colour, dim=True)))
    console.rule(style=colour)


def main(argv: list[str] | None = None) -> int:
    """CLI: ``banner.py <title> [description] [role]`` — print one banner block."""
    args = sys.argv[1:] if argv is None else argv
    if not args:
        print("usage: banner.py <title> [description] [step|info|done]", file=sys.stderr)
        return 2
    title = args[0]
    description = args[1] if len(args) > 1 else ""
    role = args[2] if len(args) > 2 else "step"
    emit(title, description, role)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
