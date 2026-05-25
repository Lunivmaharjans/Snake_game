import tkinter as tk
import random

# Game settings
WIDTH = 600
HEIGHT = 400
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
SPEED = 100

# Create window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
high_score = 0

direction = 'down'

# Score label
label = tk.Label(
    window,
    text="Score: 0    High Score: 0",
    font=('Arial', 20)
)

label.pack()

# Canvas
canvas = tk.Canvas(
    window,
    bg=BACKGROUND_COLOR,
    height=HEIGHT,
    width=WIDTH
)

canvas.pack()


# Snake body
class Snake:

    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:

            square = canvas.create_rectangle(
                x,
                y,
                x + SPACE_SIZE,
                y + SPACE_SIZE,
                fill=SNAKE_COLOR,
                tag="snake"
            )

            self.squares.append(square)


# Food body
class Food:

    def __init__(self):

        x = random.randint(
            0,
            (WIDTH // SPACE_SIZE) - 1
        ) * SPACE_SIZE

        y = random.randint(
            0,
            (HEIGHT // SPACE_SIZE) - 1
        ) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(
            x,
            y,
            x + SPACE_SIZE,
            y + SPACE_SIZE,
            fill=FOOD_COLOR,
            tag="food"
        )


# Snake Turn
def next_turn(snake, food):

    global score
    global high_score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE

    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(
        x,
        y,
        x + SPACE_SIZE,
        y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    # Eating food
    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1

        # Update high score
        if score > high_score:
            high_score = score

        label.config(
            text=f"Score: {score}    High Score: {high_score}"
        )

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    # Check collision
    if check_collisions(snake):

        game_over()

    else:

        window.after(
            SPEED,
            next_turn,
            snake,
            food
        )


# Changing Direction
def change_direction(new_direction):

    global direction

    if new_direction == 'left':

        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':

        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':

        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':

        if direction != 'up':
            direction = new_direction


# Collision check
def check_collisions(snake):

    x, y = snake.coordinates[0]

    if x < 0 or x >= WIDTH:
        return True

    elif y < 0 or y >= HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:

        if x == body_part[0] and y == body_part[1]:
            return True

    return False


# Game over
def game_over():

    canvas.delete(tk.ALL)

    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 - 30,
        font=('Arial', 40),
        text="GAME OVER",
        fill="red",
        tag="gameover"
    )

    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 30,
        font=('Arial', 20),
        text=f"High Score: {high_score}",
        fill="yellow"
    )


# Restart game
def restart_game(event=None):

    global score
    global direction
    global snake
    global food

    # Reset values
    score = 0
    direction = 'down'

    label.config(
        text=f"Score: 0    High Score: {high_score}"
    )

    # Clear canvas
    canvas.delete(tk.ALL)

    # Create new snake and food
    snake = Snake()
    food = Food()

    # Start game again
    next_turn(snake, food)


# Keyboard controls
window.bind(
    '<Left>',
    lambda event: change_direction('left')
)

window.bind(
    '<Right>',
    lambda event: change_direction('right')
)

window.bind(
    '<Up>',
    lambda event: change_direction('up')
)

window.bind(
    '<Down>',
    lambda event: change_direction('down')
)

# Restart key
window.bind('r', restart_game)
window.bind('R', restart_game)

# Start game
snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()