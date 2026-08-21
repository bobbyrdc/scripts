# just some scripts i make to do things for me... they are ok

## standup.py

Generates a markdown file with a header for each weekday of a given month, for use as a daily standup notes template.

### Install

Requires Python 3. No external dependencies.

```bash
git clone <this repo>
cd scripts
chmod +x standup.py
```

To run it as `standup` from anywhere, symlink it onto your PATH (using `~/.local/bin` here, adjust if yours differs):

```bash
ln -sf "$(pwd)/standup.py" ~/.local/bin/standup
```

### Usage

If you symlinked it as described above, use `standup`. Otherwise use `./standup.py` (or `python3 standup.py` if it is not executable).

Run with no arguments to generate a file for the current month and year:

```bash
standup
```

Specify a month and/or year with `-m` and `-y`:

```bash
standup -m 3 -y 2026
```

Jump to next or previous month relative to today (cannot be combined with `-m`/`-y`):

```bash
standup --next
standup --prev
```

Other flags:

- `--dir <path>` - write to a custom directory instead of the default.
- `--open` - open the file after creating it, or open it directly if it already exists. Uses `$EDITOR` if set, otherwise falls back to `open`.
- `-f`, `--force` - overwrite the file if it already exists.

The file is written to `~/Documents/NOTES/standup/YYYY-MM.md` by default. The directory is created automatically if it does not exist. If the file already exists and `--force` is not set, the script prints a message and exits with a non-zero status instead of overwriting it.
