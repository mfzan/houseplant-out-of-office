"""Houseplant out-of-office auto-reply generator.

Writes a single one-line out-of-office message, as if the monstera on
the desk wrote it, to entry.txt inside the output directory.

The gate for this bounty: the file must hold UTF-8 text of 1 to 120
characters, and must not be only whitespace. This program refuses to
write anything outside that range, so a bad line fails loudly here
instead of silently scoring zero later.
"""

import os
import sys

# The entry: the monstera is out of office because its human finally
# watered it, so now it is too busy photosynthesizing to answer email.
# The human's emails get to wait, the way the plant waited.
ENTRY = (
    "Out of office: you finally watered me, so I'm too busy "
    "photosynthesizing to reply. Your emails can wait like I did."
)

MIN_CHARS = 1
MAX_CHARS = 120


def check_entry(line):
    """Fail loudly unless the line is inside the bounty gate."""
    if not isinstance(line, str):
        raise SystemExit("entry must be text, got %r" % type(line).__name__)
    if "\n" in line or "\r" in line:
        raise SystemExit("entry must be exactly one line")
    if not line.strip():
        raise SystemExit("entry must not be only whitespace")
    size = len(line)
    if size < MIN_CHARS or size > MAX_CHARS:
        raise SystemExit(
            "entry is %d characters, outside the gate of %d-%d"
            % (size, MIN_CHARS, MAX_CHARS)
        )
    return line


def main():
    os.umask(0o022)

    output_dir = os.environ.get("OUTPUT_DIR") or "/output"
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir, mode=0o755)

    line = check_entry(ENTRY)

    target = os.path.join(output_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")
    # The grader collects outputs as another user, so the file we just
    # created must be world-readable. Never chmod the output directory
    # itself: it is provided by the grader and may not be ours to change.
    os.chmod(target, 0o644)

    print("wrote %s (%d characters)" % (target, len(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
