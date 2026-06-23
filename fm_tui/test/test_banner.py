"""Banner-renderer tests: block layout, palette, and CLI."""

from rich.console import Console

from fm_tui import banner


def _capture(title, description="", role="step", width=40):
    # Record to an off-screen console so we can inspect what `emit` draws.
    console = Console(record=True, width=width, force_terminal=True, color_system="truecolor")
    banner.emit(title, description, role, console=console)
    return console.export_text().rstrip("\n").split("\n")


def test_block_is_rule_title_rule_without_description():
    top, title, bottom = _capture("up", width=40)
    assert top == "─" * 40  # rule spans the full width
    assert bottom == "─" * 40
    assert "▸ up" in title


def test_description_adds_a_row_between_title_and_rule():
    top, title, desc, bottom = _capture("Container Up", "compose up -d", width=40)
    assert top == "─" * 40
    assert bottom == "─" * 40
    assert "▸ Container Up" in title
    assert "compose up -d" in desc


def test_rules_track_the_terminal_width():
    top, _, bottom = _capture("build", width=20)
    assert len(top) == 20
    assert len(bottom) == 20


def test_role_picks_its_palette_colour():
    # export_html carries the colour; the info sand must appear in the markup.
    console = Console(record=True, width=40, force_terminal=True, color_system="truecolor")
    banner.emit("Foxglove", "ws://localhost:8765", "info", console=console)
    assert banner.SAND.lstrip("#").lower() in console.export_html().lower()


def test_unknown_role_falls_back_to_lilac():
    console = Console(record=True, width=40, force_terminal=True, color_system="truecolor")
    banner.emit("x", "", "nope", console=console)
    assert banner.LILAC.lstrip("#").lower() in console.export_html().lower()


def test_cli_defaults_role_and_succeeds(capsys):
    # run.sh calls `banner.py <msg>` with no role; CLI must default and print.
    assert banner.main(["bringing container up"]) == 0
    assert "▸ bringing container up" in capsys.readouterr().out


def test_cli_without_args_is_usage_error(capsys):
    assert banner.main([]) == 2
    assert "usage" in capsys.readouterr().err
