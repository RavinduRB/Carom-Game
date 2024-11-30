import tkinter as tk
import math

# Constants
BOARD_SIZE = 600
STRIKER_RADIUS = 15
COIN_RADIUS = 10
FRICTION = 0.98
SPEED_LIMIT = 15

# Helper functions
def distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def vector_angle(x1, y1, x2, y2):
    return math.atan2(y2 - y1, x2 - x1)

class CarromGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Carrom Game")

        # Create canvas
        self.canvas = tk.Canvas(root, width=BOARD_SIZE, height=BOARD_SIZE, bg="saddlebrown")
        self.canvas.pack()

        # Draw board boundary
        self.canvas.create_rectangle(50, 50, BOARD_SIZE - 50, BOARD_SIZE - 50, fill="burlywood4", outline="black", width=3)

        # Game elements
        self.striker = {"x": BOARD_SIZE // 2, "y": BOARD_SIZE - 100, "dx": 0, "dy": 0}
        self.coins = [{"x": BOARD_SIZE // 2, "y": BOARD_SIZE // 2, "dx": 0, "dy": 0}]

        # Draw striker and coins
        self.striker_id = self.canvas.create_oval(
            self.striker["x"] - STRIKER_RADIUS, self.striker["y"] - STRIKER_RADIUS,
            self.striker["x"] + STRIKER_RADIUS, self.striker["y"] + STRIKER_RADIUS,
            fill="blue"
        )

        self.coin_ids = []
        for coin in self.coins:
            coin_id = self.canvas.create_oval(
                coin["x"] - COIN_RADIUS, coin["y"] - COIN_RADIUS,
                coin["x"] + COIN_RADIUS, coin["y"] + COIN_RADIUS,
                fill="black"
            )
            self.coin_ids.append(coin_id)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_aim)
        self.canvas.bind("<B1-Motion>", self.adjust_aim)
        self.canvas.bind("<ButtonRelease-1>", self.shoot)

        # Aim line
        self.aim_line = None

        # Game loop
        self.update_game()

    def start_aim(self, event):
        self.aim_start = (event.x, event.y)

    def adjust_aim(self, event):
        if self.aim_line:
            self.canvas.delete(self.aim_line)
        self.aim_line = self.canvas.create_line(
            self.striker["x"], self.striker["y"], event.x, event.y, fill="white", width=2
        )

    def shoot(self, event):
        if self.aim_line:
            self.canvas.delete(self.aim_line)
            self.aim_line = None

        angle = vector_angle(self.striker["x"], self.striker["y"], event.x, event.y)
        strength = min(distance(self.striker["x"], self.striker["y"], event.x, event.y) / 10, SPEED_LIMIT)

        self.striker["dx"] = math.cos(angle) * strength
        self.striker["dy"] = math.sin(angle) * strength

    def update_game(self):
        # Update striker position
        self.striker["x"] += self.striker["dx"]
        self.striker["y"] += self.striker["dy"]

        # Apply friction
        self.striker["dx"] *= FRICTION
        self.striker["dy"] *= FRICTION

        # Check board boundaries for striker
        if self.striker["x"] - STRIKER_RADIUS < 50 or self.striker["x"] + STRIKER_RADIUS > BOARD_SIZE - 50:
            self.striker["dx"] = -self.striker["dx"]
        if self.striker["y"] - STRIKER_RADIUS < 50 or self.striker["y"] + STRIKER_RADIUS > BOARD_SIZE - 50:
            self.striker["dy"] = -self.striker["dy"]

        # Update striker on canvas
        self.canvas.coords(
            self.striker_id,
            self.striker["x"] - STRIKER_RADIUS, self.striker["y"] - STRIKER_RADIUS,
            self.striker["x"] + STRIKER_RADIUS, self.striker["y"] + STRIKER_RADIUS
        )

        # Update coins
        for i, coin in enumerate(self.coins):
            coin["x"] += coin["dx"]
            coin["y"] += coin["dy"]

            # Apply friction
            coin["dx"] *= FRICTION
            coin["dy"] *= FRICTION

            # Check board boundaries for coins
            if coin["x"] - COIN_RADIUS < 50 or coin["x"] + COIN_RADIUS > BOARD_SIZE - 50:
                coin["dx"] = -coin["dx"]
            if coin["y"] - COIN_RADIUS < 50 or coin["y"] + COIN_RADIUS > BOARD_SIZE - 50:
                coin["dy"] = -coin["dy"]

            # Update coins on canvas
            self.canvas.coords(
                self.coin_ids[i],
                coin["x"] - COIN_RADIUS, coin["y"] - COIN_RADIUS,
                coin["x"] + COIN_RADIUS, coin["y"] + COIN_RADIUS
            )

        # Collision detection between striker and coins
        for coin in self.coins:
            if distance(self.striker["x"], self.striker["y"], coin["x"], coin["y"]) <= STRIKER_RADIUS + COIN_RADIUS:
                angle = vector_angle(self.striker["x"], self.striker["y"], coin["x"], coin["y"])
                coin["dx"] += math.cos(angle) * 2
                coin["dy"] += math.sin(angle) * 2
                self.striker["dx"] -= math.cos(angle) * 2
                self.striker["dy"] -= math.sin(angle) * 2

        # Schedule next update
        self.root.after(16, self.update_game)

# Main application
root = tk.Tk()
game = CarromGame(root)
root.mainloop()
