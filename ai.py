# ai.py

import random
import pickle
import os

SPACE_SIZE = 20
WIDTH = 600
HEIGHT = 400

# ---------------- REWARDS ----------------

REWARD_EAT = 10
PENALTY_WALL = -10
PENALTY_SELF = -10

# ---------------- Q LEARNING ----------------

ALPHA = 0.1
GAMMA = 0.9
EPSILON = 0.2

ACTIONS = ["up", "down", "left", "right"]

# ---------------- LOAD MEMORY ----------------

if os.path.exists("qtable.pkl"):

    with open("qtable.pkl", "rb") as f:
        q_table = pickle.load(f)

else:
    q_table = {}

# ---------------- STATE ----------------

def get_state(snake, food):

    head_x, head_y = snake.coordinates[0]
    food_x, food_y = food.coordinates

    return (
        head_x // SPACE_SIZE,
        head_y // SPACE_SIZE,
        food_x // SPACE_SIZE,
        food_y // SPACE_SIZE
    )

# ---------------- CHOOSE ACTION ----------------

def get_ai_direction(state):

    # Explore randomly
    if random.uniform(0, 1) < EPSILON:
        return random.choice(ACTIONS)

    # Create state if not exists
    if state not in q_table:

        q_table[state] = {
            action: 0 for action in ACTIONS
        }

    # Best action
    return max(
        q_table[state],
        key=q_table[state].get
    )

# ---------------- REWARD ----------------

def calculate_reward(event):

    if event == "eat":
        return REWARD_EAT

    elif event == "wall":
        return PENALTY_WALL

    elif event == "self":
        return PENALTY_SELF

    return 0

# ---------------- UPDATE Q TABLE ----------------

def update_q_table(state, action, reward, next_state):

    if state not in q_table:

        q_table[state] = {
            a: 0 for a in ACTIONS
        }

    if next_state not in q_table:

        q_table[next_state] = {
            a: 0 for a in ACTIONS
        }

    old_value = q_table[state][action]

    next_max = max(
        q_table[next_state].values()
    )

    new_value = old_value + ALPHA * (
        reward + GAMMA * next_max - old_value
    )

    q_table[state][action] = new_value

# ---------------- SAVE ----------------

def save_qtable():

    with open("qtable.pkl", "wb") as f:
        pickle.dump(q_table, f)