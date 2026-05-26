import tkinter as tk
import random
import ai

# ---------------- GAME SETTINGS ----------------

WIDTH = 600
HEIGHT = 400
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "white"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
SPEED = 100

score = 0
last_direction = "right"
high_score = 0

# ---------------- WINDOW ----------------

window = tk.Tk()
window.title("Snake AI Game")
window.resizable(False, False)

label = tk.Label(window, text="Score: 0    High Score: 0", font=('Arial', 20))
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
canvas.pack()


# ---------------- SNAKE ----------------

class Snake:
    def __init__(self):
        self.coordinates = []
        self.squares = []

        # FIX: prevent overlapping body (IMPORTANT FIX)
        for i in range(BODY_PARTS):
            self.coordinates.append([100 - i * SPACE_SIZE, 100])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR
            )
            self.squares.append(square)


# ---------------- FOOD ----------------

class Food:
    def __init__(self):
        self.spawn()

    def spawn(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food"
        )


# ---------------- COLLISION ----------------

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return "wall"
    if y < 0 or y >= HEIGHT:
        return "wall"

    for part in snake.coordinates[1:]:
        if [x, y] == part:
            return "self"

    return None


# ---------------- GAME OVER ----------------

def game_over():
    global snake, food, score

    score = 0
    canvas.delete("all")

    canvas.create_text(
        WIDTH / 2,
        HEIGHT / 2,
        text="GAME OVER",
        fill="red",
        font=("Arial", 30)
    )

    window.after(1500, restart_game)


# ---------------- RESTART ----------------

def restart_game():
    global snake, food, score

    score = 0

    canvas.delete("all")

    snake = Snake()
    food = Food()

    next_turn(snake, food)


# ---------------- MAIN LOOP ----------------

def next_turn(snake, food):
    global score, high_score, last_direction

    # AI decision
    state = ai.get_state(snake, food)
    direction = ai.get_ai_direction(state)
    opposite = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}

    if direction == opposite.get(last_direction, ""):
        direction = last_direction

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    last_direction = direction 

    # new head
    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(
        x, y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    reward = 0

    # ---------------- FOOD CHECK ----------------
    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        reward = ai.calculate_reward("eat")
        print("Reward:", reward)

        if score > high_score:
            high_score = score

        label.config(text=f"Score: {score}    High Score: {high_score}")

        canvas.delete("food")
        food = Food()

    else:
        reward = 0
        print("reward:", reward)
        # remove tail
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # ---------------- COLLISION ----------------
    collision = check_collisions(snake)
    next_state = ai.get_state(snake, food)

    if collision:
        reward = ai.calculate_reward(collision)
        print("Reward:", reward)

        ai.update_q_table(state, direction, reward, next_state)
        ai.save_qtable()

        game_over()
        return

    else:
        ai.update_q_table(state, direction, reward, next_state)
        ai.save_qtable()

        window.after(SPEED, next_turn, snake, food)


# ---------------- START GAME ----------------

snake = Snake()
food = Food()

next_turn(snake, food)
window.mainloop()