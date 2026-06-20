# Diagrams

Architecture diagrams for the application layer, authored in [d2](https://d2lang.com).
Each `.d2` file is the source of truth; the matching `.svg` is a generated
artifact referenced by the docs. Edit the `.d2`, then re-render.

## Render

```bash
./render.sh          # renders every *.d2 to *.svg with the brand font
```

Needs `d2` on `PATH`. The font ships in [`fonts/`](fonts/), so rendering is
self-contained — no font install, no personal tooling. The script passes the
font explicitly:

```bash
d2 --layout elk --font-regular fonts/GeistMono-VF.ttf \
   --font-bold fonts/GeistMono-VF.ttf --font-italic fonts/GeistMono-VF.ttf in.d2 out.svg
```

## Font

**Geist Mono** — First Motive's brand monospace ([Vercel](https://github.com/vercel/geist-font),
OFL). Ships as `fonts/GeistMono-VF.ttf`. Mono suits the technical tokens the
diagrams carry (`fm_*`, `*.launch.py`, `ros2_control`).

## Palette

Mirrors firstmotive.ai. Defined once in [`styles.d2`](styles.d2), imported with
`...@styles`.

| Token | Hex | Use |
|-------|-----|-----|
| plum | `#3B3443` | role band, borders, edges |
| lavender | `#B6A5C6` | package band |
| cream | `#E7DDC8` | artifact / node band |
| light text | `#ECE2CF` | text on plum |
| deep | `#342E3B` | text on lavender / cream |

## Block Grammar

Every component is a stacked block built as a `grid-rows` container:

```
┌─────────────────┐  role  — human label (plum)
├─────────────────┤  pkg   — package name (lavender), one colour for all packages
├─────────────────┤  art   — artifact / node (cream)
└─────────────────┘
```

- A block expanded in a deeper diagram uses `class: zoom` (dashed border).
- Node/topic graphs use `node` (plum box) + `topic` (cream pill) instead.
- Layout is ELK (straight orthogonal edges); `direction: right` for fan-in.

## Diagrams

The application layer is the entry point: the launcher menu and the bringup
composition that starts the whole stack, plus the visualization clients that
watch it.

```
launcher   fm_tui → View · Teleop · Auto  (capability → package → launch file)
bringup    Description → Control ← Manual · Auto → Hardware Boundary
viz        any ROS graph topics → foxglove_bridge (browser) · rviz2 (local X)
```

`bringup` composes packages from sibling repos
([`fm-robot`](https://github.com/first-motive/fm-robot),
[`fm-sim`](https://github.com/first-motive/fm-sim),
[`fm-teleop`](https://github.com/first-motive/fm-teleop)). Its `Hardware
Boundary` block expands in `fm-robot`'s `hardware` diagram. See
[ARCHITECTURE.md](../ARCHITECTURE.md).
