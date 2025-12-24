# Human vs Robot Game Mode (HvR)

from tkinter import *
import numpy as np
import random

WINDOW = 600
DOTS = 6
GAP = WINDOW / DOTS

DOT_R = 6
EDGE_W = 4

DOT_COLOR = "#2ECC71"
P1_BOX = "#AED6F1"
P2_BOX = "#F5B7B1"


class DotsBoxes:
    def __init__(self):
        self.root = Tk()
        self.root.title("Dots and Boxes - Competitive AI")

        self.canvas = Canvas(self.root, width=WINDOW, height=WINDOW)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.human_click)

        # restart button (hidden until game over)
        self.restart_button = Button(
            self.root,
            text="Play Again",
            font=("Arial", 12, "bold"),
            command=self.reset
        )
        self.restart_button.place_forget()

        self.reset()

    # setup
    def reset(self):
        self.restart_button.place_forget()

        self.h = np.zeros((DOTS, DOTS - 1), bool)
        self.v = np.zeros((DOTS - 1, DOTS), bool)
        self.owner = np.zeros((DOTS - 1, DOTS - 1), int)

        self.turn = 1
        self.done = False
        self.draw()

    # draw
    def draw(self):
        self.canvas.delete("all")
        self.draw_status()

        for r in range(DOTS - 1):
            for c in range(DOTS - 1):
                if self.owner[r][c]:
                    self.fill_box(r, c)

        for r in range(DOTS):
            for c in range(DOTS - 1):
                if self.h[r][c]:
                    self.h_edge(r, c)

        for r in range(DOTS - 1):
            for c in range(DOTS):
                if self.v[r][c]:
                    self.v_edge(r, c)

        for i in range(DOTS):
            for j in range(DOTS):
                x = GAP / 2 + i * GAP
                y = GAP / 2 + j * GAP
                self.canvas.create_oval(
                    x - DOT_R, y - DOT_R,
                    x + DOT_R, y + DOT_R,
                    fill=DOT_COLOR, outline=""
                )

    def draw_status(self):
        h = np.sum(self.owner == 1)
        a = np.sum(self.owner == 2)
        text = "Game Over" if self.done else ("Your Turn" if self.turn == 1 else "AI Turn")
        self.canvas.create_text(
            WINDOW // 2, 18,
            text=f"{text}   |   You: {h}   AI: {a}",
            font=("Arial", 14, "bold"),
            fill="white"
        )

    def h_edge(self, r, c):
        x = GAP / 2 + c * GAP
        y = GAP / 2 + r * GAP
        self.canvas.create_line(x, y, x + GAP, y, width=EDGE_W)

    def v_edge(self, r, c):
        x = GAP / 2 + c * GAP
        y = GAP / 2 + r * GAP
        self.canvas.create_line(x, y, x, y + GAP, width=EDGE_W)

    def fill_box(self, r, c):
        x = GAP / 2 + c * GAP
        y = GAP / 2 + r * GAP
        color = P1_BOX if self.owner[r][c] == 1 else P2_BOX
        self.canvas.create_rectangle(x, y, x + GAP, y + GAP, fill=color, outline="")

    # human
    def human_click(self, e):
        if self.done or self.turn != 1:
            return

        if self.place_edge(e.x, e.y):
            if not self.claim_boxes(1):
                self.turn = 2
                self.draw()
                self.root.after(500, self.ai_turn)
            else:
                self.draw()

            if self.is_done():
                self.done = True
                self.restart_button.place(
                    x=WINDOW // 2,
                    y=WINDOW - 30,
                    anchor="center"
                )
                self.draw()


    # robot
    def ai_turn(self):
        if self.done:
            return

        move = self.ai_best_move()
        self.apply(move)

        if not self.claim_boxes(2):
            self.turn = 1

        self.draw()

        if self.is_done():
            self.done = True
            self.restart_button.place(
                x=WINDOW // 2,
                y=WINDOW - 30,
                anchor="center"
            )
            self.draw()
            return

        if self.turn == 2:
            self.root.after(500, self.ai_turn)

    # human game logic
    def place_edge(self, x, y):
        grid = (np.array([x, y]) - GAP / 4) // (GAP / 2)
        r, c = int(grid[1]), int(grid[0])

        if r % 2 == 0 and c % 2 == 1:
            rr, cc = r // 2, (c - 1) // 2
            if not self.h[rr][cc]:
                self.h[rr][cc] = True
                return True

        if r % 2 == 1 and c % 2 == 0:
            rr, cc = (r - 1) // 2, c // 2
            if not self.v[rr][cc]:
                self.v[rr][cc] = True
                return True

        return False

    def apply(self, m):
        if m[0] == "h":
            self.h[m[1]][m[2]] = True
        else:
            self.v[m[1]][m[2]] = True

    def claim_boxes(self, player):
        got = False
        for r in range(DOTS - 1):
            for c in range(DOTS - 1):
                if self.owner[r][c] == 0 and self.count_edges(r, c) == 4:
                    self.owner[r][c] = player
                    got = True
        return got

    def count_edges(self, r, c):
        return sum([
            self.h[r][c],
            self.h[r + 1][c],
            self.v[r][c],
            self.v[r][c + 1]
        ])

    def is_done(self):
        return np.all(self.owner != 0)

    # robot game logic
    def ai_best_move(self):
        moves = self.all_moves()
        for m in moves:
            if self.simulates_box(m):
                return m
        safe = [m for m in moves if not self.creates_third(m)]
        return random.choice(safe if safe else moves)

    def all_moves(self):
        res = []
        for r in range(DOTS):
            for c in range(DOTS - 1):
                if not self.h[r][c]:
                    res.append(("h", r, c))
        for r in range(DOTS - 1):
            for c in range(DOTS):
                if not self.v[r][c]:
                    res.append(("v", r, c))
        return res

    def simulates_box(self, m):
        self.apply(m)
        ok = any(self.count_edges(r, c) == 4 and self.owner[r][c] == 0
                 for r in range(DOTS - 1) for c in range(DOTS - 1))
        self.undo(m)
        return ok

    def creates_third(self, m):
        self.apply(m)
        bad = any(self.count_edges(r, c) == 3 and self.owner[r][c] == 0
                  for r in range(DOTS - 1) for c in range(DOTS - 1))
        self.undo(m)
        return bad

    def undo(self, m):
        if m[0] == "h":
            self.h[m[1]][m[2]] = False
        else:
            self.v[m[1]][m[2]] = False

    def run(self):
        self.root.mainloop()


DotsBoxes().run()