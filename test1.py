"""A borderless, 10-level Snake game built with Tkinter."""

from __future__ import annotations

import random
import tkinter as tk
from collections import deque
from typing import Deque, Tuple


Point = Tuple[int, int]


class SnakeGame:
    """Snake with wraparound edges, growing length, and ten speed levels."""

    WIDTH = 640
    HEIGHT = 480
    CELL = 20
    COLUMNS = WIDTH // CELL
    ROWS = HEIGHT // CELL
    MAX_LEVEL = 10
    STARTING_SPEED = 145
    SPEED_STEP = 11

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Snake - 10 Levels")
        self.root.resizable(False, False)
        self.root.configure(bg="#101820")

        header = tk.Frame(root, bg="#101820")
        header.pack(fill="x")
        self.status = tk.Label(header, text="", font=("Segoe UI", 12, "bold"),
                               fg="#f2f5f7", bg="#101820", pady=8)
        self.status.pack(side="left", padx=12)
        help_label = tk.Label(
            header,
            text="Arrow keys / WASD  •  R to restart  •  Esc to quit",
            font=("Segoe UI", 9), fg="#aab8c2", bg="#101820", pady=8,
        )
        help_label.pack(side="right", padx=12)

        self.canvas = tk.Canvas(root, width=self.WIDTH, height=self.HEIGHT,
                                bg="#18242b", highlightthickness=0)
        self.canvas.pack()

        self.snake: Deque[Point] = deque()
        self.direction: Point = (1, 0)
        self.next_direction: Point = (1, 0)
        self.food: Point = (0, 0)
        self.score = 0
        self.level = 1
        self.running = True
        self.game_over = False

        self.root.bind_all("<KeyPress>", self.handle_key)
        self.restart()

    def restart(self) -> None:
        center = (self.COLUMNS // 2, self.ROWS // 2)
        self.snake = deque([(center[0] - offset, center[1]) for offset in range(5)])
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.level = 1
        self.running = True
        self.game_over = False
        self.place_food()
        self.draw()
        self.tick()

    def handle_key(self, event: tk.Event[tk.Misc]) -> None:
        key = str(event.keysym).lower()
        if key in {"r", "return"} and self.game_over:
            self.restart()
            return
        if key in {"escape", "q"}:
            self.root.destroy()
            return
        directions = {
            "up": (0, -1), "w": (0, -1), "down": (0, 1), "s": (0, 1),
            "left": (-1, 0), "a": (-1, 0), "right": (1, 0), "d": (1, 0),
        }
        new_direction = directions.get(key)
        if new_direction and new_direction != (-self.direction[0], -self.direction[1]):
            self.next_direction = new_direction

    def place_food(self) -> None:
        occupied = set(self.snake)
        available = [(x, y) for y in range(self.ROWS) for x in range(self.COLUMNS)
                     if (x, y) not in occupied]
        if available:
            self.food = random.choice(available)

    def tick(self) -> None:
        if not self.running:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = ((head_x + dx) % self.COLUMNS, (head_y + dy) % self.ROWS)

        body_to_check = set(self.snake if new_head == self.food else list(self.snake)[:-1])
        if new_head in body_to_check:
            self.end_game()
            return

        self.snake.appendleft(new_head)
        if new_head == self.food:
            self.score += 1
            self.level = min(self.MAX_LEVEL, 1 + self.score // 5)
            self.place_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(self.speed(), self.tick)

    def speed(self) -> int:
        return max(35, self.STARTING_SPEED - (self.level - 1) * self.SPEED_STEP)

    def end_game(self) -> None:
        self.running = False
        self.game_over = True
        self.draw()

    def draw_cell(self, point: Point, color: str, inset: int = 2) -> None:
        x, y = point
        self.canvas.create_rectangle(x * self.CELL + inset, y * self.CELL + inset,
                                     (x + 1) * self.CELL - inset,
                                     (y + 1) * self.CELL - inset,
                                     fill=color, outline="")

    def draw(self) -> None:
        self.canvas.delete("all")
        self.status.configure(text=f"Level {self.level}/{self.MAX_LEVEL}    "
                               f"Score: {self.score}    Length: {len(self.snake)}")
        for index, segment in enumerate(self.snake):
            self.draw_cell(segment, "#48d597" if index == 0 else "#2ca875")
        self.draw_cell(self.food, "#ffca3a", inset=3)

        if self.game_over:
            self.canvas.create_rectangle(0, 0, self.WIDTH, self.HEIGHT,
                                         fill="#101820", stipple="gray50", outline="")
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 - 18,
                                    text="GAME OVER", fill="#ffffff",
                                    font=("Segoe UI", 28, "bold"))
            self.canvas.create_text(self.WIDTH // 2, self.HEIGHT // 2 + 24,
                                    text="Press R or Enter to play again",
                                    fill="#d6e2e8", font=("Segoe UI", 13))


def main() -> None:
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
