# IDE terminal composer glitches (Cursor / VS Code)

Symptoms in the Ink TUI (`hermes -p heavy-coder chat`):

- A **stray letter** beside the **first character you type** (often **h**, **c**, **a**, **t** - fragments of the `heavy-coder` prefix as columns drift)
- **Multi-character junk** in the composer even with the IDE skin, e.g. `heavy-coder > Iky "refactor the auth module"` where **`Iky`** is not your text - prefix column math is still off until you shorten the profile name (see mitigations)
- A **miscolored letter** inside the prompt prefix (`heavy-coder ⛓ …`)
- **Ghost text on the right edge** while typing, like `t tt r re re` (each key leaves debris on the margin)
- **One vertical `#` out of step** in the **HEAVYCODER** banner (figlet rows were not the same width)

These are usually **not** random font bugs. The composer splits the row into:

1. A **fixed-width prompt prefix** (`heavy-coder` + skin `prompt_symbol`)
2. The **TextInput** field (hardware caret)

On IDE built-in terminals, **emoji width** and **extra prompt glyphs** often disagree with Hermes Ink's `stringWidth()` math. The prefix **bleeds one or more cells** into the input zone, so you see prompt junk as a "ghost" character next to your text, or a letter from `heavy-coder` painted in the wrong column.

The **`t tt r re re` pattern** is Ink **fast-echo**: keystrokes are written straight to the PTY for speed. When the prompt column math is off (or the IDE terminal cursor diverges from Ink's model), those writes land on the **right margin** instead of after your real input. Hermes should disable fast-echo in VS Code / Cursor / Windsurf (same class of bug as Apple Terminal and tmux).

## What we ship in the profile skin

- **`display.auto_ide_skin: true`** (default): on session start, profile bootstrap sets **`heavy-coder-ide`** in Cursor / VS Code / Windsurf terminals (ASCII `>` prompt, no tall hero art). Set `display.auto_ide_skin: false` to keep **`heavy-coder`** everywhere.
- **`branding.prompt_symbol: "⛓"`** (chain **only**) on **`heavy-coder`**. Do **not** add `▸`, `❯`, etc. after the chain; that second glyph is the usual source of the ghost beside your first typed character.
- **`heavy-coder-ide`** and **`heavy-coder-light`**: ASCII **`>`** prompt (no emoji width drift). Light panels: `export HERMES_TUI_THEME=light` - bootstrap picks **`heavy-coder-light`** when `auto_ide_skin` is on.
- **Banner figlet**: all seven **HEAVYCODER** rows are padded to the same width so no lone `#` column sticks out vertically.

## Quick mitigations

1. **Shorten the profile prefix** (most effective for `Iky`-style bleed; `>` skin alone may not be enough):

   ```bash
   hermes profile install github.com/codegraphtheory/heavy-coder --name hc --alias --force --yes
   hc chat
   ```

   Prompt becomes `hc >` instead of `heavy-coder >`.

2. **IDE-safe launcher** (after Hermes honors `HERMES_TUI_FAST_ECHO=0`):

   ```bash
   ./scripts/ide_safe_chat.sh chat
   ```

3. **Widen the terminal panel** in the IDE (more columns reduces wrap/overlap).

4. **Classic CLI** (no Ink composer, no fast-echo):

   ```bash
   hermes -p heavy-coder chat --cli
   ```

5. **Upstream / local Hermes**: patch `ui-tui/src/components/textInput.tsx` so `supportsFastEchoTerminal()` returns `false` for `detectVSCodeLikeTerminal()` and respects `HERMES_TUI_FAST_ECHO=0`. Rebuild TUI: `cd ui-tui && npm run build`.

After skin or Hermes changes, restart the session (`/new` or exit and relaunch).

## Unreadable dim secondary text on light panels

The cyberpunk **heavy-coder** skin targets **dark** terminal backgrounds. Secondary copy (status bar model name, `/help` hints, tool progress, timestamps) uses `banner_dim`, which Ink maps to `color.muted`. On a **light** IDE terminal panel, near-white body text (`#F0FDFF`) and purple-muted tones can look like unreadable dim mush, especially with Ink `dimColor`.

**Dark terminal (default look):** reinstall the updated skin (brighter `banner_dim` / status colors in 0.2.21+).

**Light terminal panel (common in Cursor):**

```bash
export HERMES_TUI_THEME=light
hermes -p heavy-coder chat
# bootstrap sets heavy-coder-light when display.auto_ide_skin is true; or /skin heavy-coder-light
```

Or set your IDE terminal profile to a **dark** background and keep `/skin heavy-coder`.