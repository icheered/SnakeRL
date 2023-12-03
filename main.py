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
    total_score = 0
    record = 0
    
    rewards = []
    total_reward = 0
    total_score_reward = 0
    total_moving_to_apple = 0
    total_survive_duration_reward = 0
    epsilons = []
    
    agent = Agent(game)

    while True:
        # Get state
        old_state = game.get_state()
        old_score = score

        # Get input
        # action = get_human_input(action)
        action = agent.get_action(game)
        
        # Update game
        score, done = game.step(action)

        # Train agent
        score_reward, moving_to_apple, survive_duration_reward = agent.get_reward(score, old_score, done, game)
        reward = score_reward + moving_to_apple + survive_duration_reward
        #print(f"reward: {reward}, score_reward: {score_reward}, moving_to_apple: {moving_to_apple}, survive_duration_reward: {survive_duration_reward}")
        
        
        total_reward += reward
        total_score_reward += score_reward
        total_moving_to_apple += moving_to_apple
        total_survive_duration_reward += survive_duration_reward
        agent.train_short_memory(old_state, action, reward, game.get_state(), done)
        agent.remember(old_state, action, reward, game.get_state(), done)

        if done:
            # train long memory, plot result
            print(f"####### GAME: {agent.n_games}. SCORE: {score}. TOTAL REWARD: {total_reward} #######")
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            scores.append(score)
            total_score += score

            rewards.append(
                [total_reward, total_score_reward, total_moving_to_apple, total_survive_duration_reward]
            ) 
            
            epsilons.append(agent.epsilon)
            if(agent.n_games >= 5 ):
                plot_metrics(scores, rewards, epsilons)

            game.reset()
            action = 1
            old_score = 0
            score = 0
            done = False 

            total_reward = 0
            total_score_reward = 0
            total_moving_to_apple = 0
            total_survive_duration_reward = 0
            
        # game.print_board()

        # Update display
        if(agent.n_games >= 50 and agent.n_games % 10 == 0):
            display.update(game)
        #time.sleep(0.5)

    pass


if __name__ == "__main__":
    main()
    #main()
