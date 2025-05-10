import random
import pickle
from games.tic_tac_toe import TicTacToe

class QLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        # (state, action) -> Q value
        self.q_table = {}  
        # learning rate
        self.alpha = alpha
        # discount factor
        self.gamma = gamma
        # exploration factor
        self.epsilon = epsilon

    # convert the tic_tac_toe board to a tuple 
    def get_state(self, grid):
        return tuple(grid)

    def flatten_grid(self, grid):
        return [cell for row in grid for cell in row]

    # returns 0 to 8 for valid actions
    def get_valid_actions(self, grid):
        return [i for i in range(9) if grid[i] == '-']

    # I used the episolon greedy method
    # With probability ε → explores randomly
    # Else, picks the action with the highest q-value among valid action
    def choose_action(self, state, valid_actions):
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        q_vals = [self.q_table.get((state, a), 0.0) for a in valid_actions]
        max_q = max(q_vals)
        return random.choice([a for a, q in zip(valid_actions, q_vals) if q == max_q])

    # update the q learning formula
    def update(self, state, action, reward, next_state, done):
        old_q = self.q_table.get((state, action), 0.0)
        future_q = 0.0 if done else max([self.q_table.get((next_state, a), 0.0) for a in self.get_valid_actions(next_state)])
        self.q_table[(state, action)] = old_q + self.alpha * (reward + self.gamma * future_q - old_q)

def train(agent, episodes=10000):
    # loop through this many episodes 
    for episode in range(episodes):
        # create a new game every single time
        game = TicTacToe()
        state = agent.get_state(game.grid)
        done = False
        history = []

        # for picking the correct actions, 
        # if winning: +1
        # if loosing: -1
        # if draw: 0.5
        # onging: 0
        while not game.game_over():
            flat_grid = agent.flatten_grid(game.grid)
            valid_actions = agent.get_valid_actions(flat_grid)
            if not valid_actions:
                break  # no valid moves, skip turn / exit loop
            action = agent.choose_action(state, valid_actions)
            game.make_move(action)
            next_state = agent.get_state(game.grid)
            reward = 0

            if game.check_winner() == 'X':
                reward = 1
                done = True
            elif game.check_winner() == 'O':
                reward = -1
                done = True
            elif game.is_draw():
                reward = 0.5
                done = True

            agent.update(state, action, reward, next_state, done)
            state = next_state

            if not done:
                game.switch_player()

    #save the q learning table
    with open("q_table_ttt.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)

if __name__ == "__main__":
    agent = QLearningAgent()
    train(agent)
