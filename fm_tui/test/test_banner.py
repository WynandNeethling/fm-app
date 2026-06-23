"""Banner-renderer tests: layout, palette, and graceful degradation."""

from fm_tui import banner


def test_plain_layout_fills_to_width():
    line = banner.render("up", columns=40, colour=False)
    assert line.startswith("▸ up ")
    assert len(line) == 40
    assert "\x1b[" not in line  # no escapes when colour is off


def test_narrow_width_keeps_a_minimum_rule():
    # Even when the label overflows the width, a short rule still trails it.
    line = banner.render("a very long step message", columns=10, colour=False)
    assert line.endswith("---")


def test_colour_uses_palette_and_resets():
    line = banner.render("build", role="step", columns=40, colour=True)
    r, g, b = banner.ROLES["step"]
    assert f"38;2;{r};{g};{b}" in line
    assert line.endswith(banner._RESET)


def test_unknown_role_falls_back_to_lilac():
    line = banner.render("x", role="nope", columns=40, colour=True)
    r, g, b = banner.LILAC
    assert f"38;2;{r};{g};{b}" in line


def test_no_color_env_disables_colour(monkeypatch):
    monkeypatch.setenv("NO_COLOR", "1")
    assert not banner.supports_colour()


def test_render_default_role_is_step():
    # Omitting role must match an explicit "step" — the path run.sh hits most.
    assert banner.render("x", columns=40) == banner.render("x", "step", columns=40)


def test_cli_defaults_role_and_succeeds(capsys):
    # run.sh calls `banner.py <msg>` with no role; CLI must default and print.
    assert banner.main(["bringing container up"]) == 0
    assert capsys.readouterr().out.startswith("▸ bringing container up")


def test_cli_without_args_is_usage_error(capsys):
    assert banner.main([]) == 2
    assert "usage" in capsys.readouterr().err
