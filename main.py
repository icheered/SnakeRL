from game import Game
from display import Display
from human import get_human_action
from agent import Agent
from plot import plot_metrics
import time
import numpy as np

actions = ["UP", "RIGHT", "DOWN", "LEFT"]

def main():
    game = Game(w=10, h=10)
    game.reset()
    display = Display(game, blocksize=20, title="Snake")
    
    action = 1
    score = 0
    done = False

    scores = []
    mean_score = None
    mean_scores = []
    total_score = 0
    record = 0
    
    rewards = []
    total_reward = 0
    epsilons = []
    
    agent = Agent(game)

    while True:
        # Get state
        old_state = game.get_state()
        old_score = score

        # Get input
        # action = get_human_input(action)
        action = agent.get_action(game, action)
        
        # Update game
        score, done = game.step(action)

        # Train agent
        reward = agent.get_reward(score, old_score, done, game)
        total_reward += reward
        agent.train_short_memory(old_state, action, reward, game.get_state(), done)
        agent.remember(old_state, action, reward, game.get_state(), done)

        if done:
            # train long memory, plot result
            print(f"####### GAME: {agent.n_games}. SCORE: {score} #######")
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            mean_scores.append(mean_score)

            rewards.append(total_reward) 
            total_reward = 0

            epsilons.append(agent.epsilon)
            if(agent.n_games > 100 ):
                plot_metrics(scores, mean_scores, rewards, epsilons)
            
            action = 1
        # game.print_board()

        # Update display
        if(agent.n_games > 100 and agent.n_games % 20 == 0):
            display.update(game)
        #time.sleep(0.5)

    pass


if __name__ == "__main__":
    main()
