import random
import pickle
from games.connect_four import ConnectFour

class ConnectFourQLearningAgent:
    def __init__(self, alpha=0.5, gamma=0.9, epsilon=0.1):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def flatten_grid(self, grid):
        return [cell for row in grid for cell in row]

    def get_state(self, grid):
        flat = self.flatten_grid(grid)
        return tuple(flat)

    def get_valid_actions(self, grid):
        return [col for col in range(7) if grid[0][col] == '-']

    def choose_action(self, state, valid_actions):
        if not valid_actions:
            return None
        if random.random() < self.epsilon:
            return random.choice(valid_actions)
        q_vals = [self.q_table.get((state, a), 0.0) for a in valid_actions]
        max_q = max(q_vals)
        return random.choice([a for a, q in zip(valid_actions, q_vals) if q == max_q])

    def update(self, state, action, reward, next_state, done, valid_next_actions):
        old_q = self.q_table.get((state, action), 0.0)
        future_q = 0.0
        if not done and valid_next_actions:
            future_q = max([self.q_table.get((next_state, a), 0.0) for a in valid_next_actions])
        self.q_table[(state, action)] = old_q + self.alpha * (reward + self.gamma * future_q - old_q)

def train(agent, episodes=10000):
    for episode in range(episodes):
        game = ConnectFour()
        state = agent.get_state(game.board)
        done = False

        # Alternate players each episode
        agent_symbol = 'X' if episode % 2 == 0 else 'O'
        opp_symbol = 'O' if agent_symbol == 'X' else 'X'
        game.is_x_turn = (agent_symbol == 'X')

        while not game.game_over():
            valid_actions = agent.get_valid_actions(game.board)
            if not valid_actions:
                break

            current_symbol = 'X' if game.is_x_turn else 'O'
            flat_board = agent.flatten_grid(game.board)
            state = tuple(flat_board)

            if current_symbol == agent_symbol:
                action = agent.choose_action(state, valid_actions)
            else:
                action = random.choice(valid_actions)

            game.make_move(action)
            next_state = agent.get_state(game.board)
            winner = game.check_winner()

            if winner == agent_symbol:
                reward = 1
                done = True
            elif winner == opp_symbol:
                reward = -1
                done = True
            elif game.is_draw():
                reward = 0.5
                done = True
            else:
                reward = 0

            next_valid_actions = agent.get_valid_actions(game.board)
            if current_symbol == agent_symbol:
                agent.update(state, action, reward, next_state, done, next_valid_actions)

            if not done:
                game.is_x_turn = not game.is_x_turn

    with open("q_table_connect4.pkl", "wb") as f:
        pickle.dump(agent.q_table, f)

if __name__ == "__main__":
    agent = ConnectFourQLearningAgent()
    train(agent)