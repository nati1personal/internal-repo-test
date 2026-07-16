#!/usr/bin/env python3
"""Matrix-style digital rain, rendered directly in the terminal."""
import ois
import random
import shutil
import sys
import time

CHARS = "アイウエオカキクケコサシスセソタチツテト0123456789"
RESET = "\x1b[0m"
HEAD_COLOR = "\x1b[97m"
GLOW_COLORS = ["\x1b[38;5;46m", "\x1b[38;5;40m", "\x1b[38;5;34m", "\x1b[38;5;28m", "\x1b[38;5;22m"]


class Column:
    def __init__(self, height):
        self.height = height
        self.reset(initial=True)

    def reset(self, initial=False):
        self.y = random.randint(-height_offset(self.height), 0) if initial else 0
        self.length = random.randint(4, 20)
        self.speed = random.uniform(0.5, 1.0)
        self.progress = 0.0
        self.chars = [random.choice(CHARS) for _ in range(self.length)]

    def step(self):
        self.progress += self.speed
        while self.progress >= 1:
            self.progress -= 1
            self.y += 1
            self.chars.pop()
            self.chars.insert(0, random.choice(CHARS))
        if self.y - self.length > self.height:
            self.reset()

    def render(self, height):
        cells = [" "] * height
        for i, ch in enumerate(self.chars):
            row = self.y - i
            if 0 <= row < height:
                if i == 0:
                    cells[row] = HEAD_COLOR + ch + RESET
                else:
                    color = GLOW_COLORS[min(i - 1, len(GLOW_COLORS) - 1)]
                    cells[row] = color + ch + RESET
        return cells


def height_offset(h):
    return h


def main():
    size = shutil.get_terminal_size((80, 24))
    width, height = size.columns, size.lines - 1
    columns = [Column(height) for _ in range(width)]

    sys.stdout.write("\x1b[?25l\x1b[2J")
    try:
        while True:
            grid = [col.render(height) for col in columns]
            lines = ["".join(grid[c][r] for c in range(width)) for r in range(height)]
            sys.stdout.write("\x1b[H" + "\n".join(lines))
            sys.stdout.flush()
            for col in columns:
                col.step()
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(RESET + "\x1b[?25h\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
