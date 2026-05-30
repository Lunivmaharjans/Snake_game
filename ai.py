import random
import pickle
import os

SPACE_SIZE = 20
WIDTH = 600
HEIGHT = 400

# ---------------- REWARDS ----------------

REWARD_EAT = 10
REWARD_STEP = 0.1
PENALTY_WALL = -100
PENALTY_SELF = -100

# ---------------- Q LEARNING ----------------

ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.05

ACTIONS = ["up", "down", "left", "right"]

# ---------------- LOAD Q TABLE ----------------

if os.path.exists("qtable.pkl"):
    with open("qtable.pkl", "rb") as f:
        q_table = pickle.load(f)
else:
    q_table = {}


# ---------------- STATE (IMPROVED) ----------------

def get_state(snake, food):
    head_x, head_y = snake.coordinates[0]
    food_x, food_y = food.coordinates

    food_left = food_x < head_x
    food_right = food_x > head_x
    food_up = food_y < head_y
    food_down = food_y > head_y

    danger_left = head_x - SPACE_SIZE < 0
    danger_right = head_x + SPACE_SIZE >= WIDTH
    danger_up = head_y - SPACE_SIZE < 0
    danger_down = head_y + SPACE_SIZE >= HEIGHT

    return (
        food_left,
        food_right,
        food_up,
        food_down,
        danger_left,
        danger_right,
        danger_up,
        danger_down
    )


# ---------------- ACTION ----------------

def get_ai_direction(state):

    if random.uniform(0, 1) < EPSILON:
        return random.choice(ACTIONS)

    if state not in q_table:
        q_table[state] = {a: 0 for a in ACTIONS}

    best_value = max(q_table[state].values())

    best_actions = [
        action for action, value in q_table[state].items()
        if value == best_value
    ]

    return random.choice(best_actions)

# ---------------- REWARD ----------------

def calculate_reward(event):
    if event == "eat":
        return REWARD_EAT
    elif event == "wall":
        return PENALTY_WALL
    elif event == "self":
        return PENALTY_SELF
    return REWARD_STEP


# ---------------- UPDATE ----------------

def update_q_table(state, action, reward, next_state):

    if state not in q_table:
        q_table[state] = {a: 0 for a in ACTIONS}

    if next_state not in q_table:
        q_table[next_state] = {a: 0 for a in ACTIONS}

    old = q_table[state][action]
    next_max = max(q_table[next_state].values())

    q_table[state][action] = old + ALPHA * (
        reward + GAMMA * next_max - old
    )


# ---------------- SAVE ----------------

def save_qtable():
    with open("qtable.pkl", "wb") as f:
        pickle.dump(q_table, f)