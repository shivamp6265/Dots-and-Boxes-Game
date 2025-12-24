# Human vs Human Game Mode (HvH)

from tkinter import *
import numpy as np

WINDOW_SIZE = 600
DOT_COUNT = 6
GAP = WINDOW_SIZE / DOT_COUNT

DOT_RADIUS = 6
EDGE_THICKNESS = 4

DOT_CLR = "#2ECC71"
P1_CLR = "#3498DB"
P2_CLR = "#E74C3C"
P1_BOX = "#85C1E9"
P2_BOX = "#F1948A"


class BoxGame:
    def __init__(self):
        self.root = Tk()
        self.root.title("Dots and Boxes")

        self.canvas = Canvas(self.root, width=WINDOW_SIZE, height=WINDOW_SIZE)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.handle_click)

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

        self.h_edges = np.zeros((DOT_COUNT, DOT_COUNT - 1), dtype=bool)
        self.v_edges = np.zeros((DOT_COUNT - 1, DOT_COUNT), dtype=bool)
        self.cell_owner = np.zeros((DOT_COUNT - 1, DOT_COUNT - 1), dtype=int)

        self.current_player = 1
        self.game_done = False

        self.redraw()

    # drawing
    def redraw(self):
        self.canvas.delete("all")
        self.draw_status_bar()

        for r in range(DOT_COUNT - 1):
            for c in range(DOT_COUNT - 1):
                if self.cell_owner[r][c] != 0:
                    self.fill_box(r, c)

        for r in range(DOT_COUNT):
            for c in range(DOT_COUNT - 1):
                if self.h_edges[r][c]:
                    self.draw_h_edge(r, c)

        for r in range(DOT_COUNT - 1):
            for c in range(DOT_COUNT):
                if self.v_edges[r][c]:
                    self.draw_v_edge(r, c)

        for i in range(DOT_COUNT):
            for j in range(DOT_COUNT):
                x = GAP / 2 + i * GAP
                y = GAP / 2 + j * GAP
                self.canvas.create_oval(
                    x - DOT_RADIUS, y - DOT_RADIUS,
                    x + DOT_RADIUS, y + DOT_RADIUS,
                    fill=DOT_CLR, outline=""
                )

    def draw_status_bar(self):
        p1 = np.sum(self.cell_owner == 1)
        p2 = np.sum(self.cell_owner == 2)

        text = "Game Over" if self.game_done else f"Player {self.current_player}'s Turn"
        self.canvas.create_text(
            WINDOW_SIZE // 2, 18,
            text=f"{text}   |   P1: {p1}   P2: {p2}",
            font=("Arial", 14, "bold"),
            fill="white"
        )

    def draw_h_edge(self, r, c):
        x1 = GAP / 2 + c * GAP
        y = GAP / 2 + r * GAP
        x2 = x1 + GAP
        self.canvas.create_line(x1, y, x2, y, width=EDGE_THICKNESS)

    def draw_v_edge(self, r, c):
        x = GAP / 2 + c * GAP
        y1 = GAP / 2 + r * GAP
        y2 = y1 + GAP
        self.canvas.create_line(x, y1, x, y2, width=EDGE_THICKNESS)

    def fill_box(self, r, c):
        x1 = GAP / 2 + c * GAP
        y1 = GAP / 2 + r * GAP
        x2 = x1 + GAP
        y2 = y1 + GAP
        color = P1_BOX if self.cell_owner[r][c] == 1 else P2_BOX
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    # game logic
    def handle_click(self, event):
        if self.game_done:
            return

        pos = np.array([event.x, event.y])
        grid = (pos - GAP / 4) // (GAP / 2)
        r, c = int(grid[1]), int(grid[0])

        move_made = False

        if r % 2 == 0 and c % 2 == 1:
            rr = r // 2
            cc = (c - 1) // 2
            if not self.h_edges[rr][cc]:
                self.h_edges[rr][cc] = True
                move_made = True

        elif r % 2 == 1 and c % 2 == 0:
            rr = (r - 1) // 2
            cc = c // 2
            if not self.v_edges[rr][cc]:
                self.v_edges[rr][cc] = True
                move_made = True

        if not move_made:
            return

        if not self.check_for_boxes():
            self.current_player = 2 if self.current_player == 1 else 1

        self.redraw()

        if self.is_finished():
            self.game_done = True
            self.restart_button.place(
                x=WINDOW_SIZE // 2,
                y=WINDOW_SIZE - 30,
                anchor="center"
            )
            self.redraw()

    def check_for_boxes(self):
        claimed = False
        for r in range(DOT_COUNT - 1):
            for c in range(DOT_COUNT - 1):
                if self.cell_owner[r][c] == 0:
                    if (self.h_edges[r][c] and
                        self.h_edges[r + 1][c] and
                        self.v_edges[r][c] and
                        self.v_edges[r][c + 1]):
                        self.cell_owner[r][c] = self.current_player
                        claimed = True
        return claimed

    def is_finished(self):
        return np.all(self.cell_owner != 0)

    def run(self):
        self.root.mainloop()


BoxGame().run()