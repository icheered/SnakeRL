# 
# The Monitor class shows graphs of the the reward and survive duration of each episode.
# 

import matplotlib.pyplot as plt

class Monitor:
    def __init__(self, config: dict):
        self.scores = [0]
        self.average_scores = [0]
        self.rewards = [0]
        self.average_rewards = [0]
        self.survive_durations = [0]
        self.average_survive_durations = [0]


        ppi = 109 # pixels per inch, specific to my monitor
        self.fig, (self.ax1, self.ax2, self.ax3) = plt.subplots(3, 1, figsize=(config["display"]["width"]/ppi, config["display"]["height"]/ppi), dpi=ppi)
        plt.tight_layout()

        # Score subplot
        self.score_line, = self.ax1.plot(self.scores, color="#fac384", linestyle='-', label='Score')
        self.avg_score_line, = self.ax1.plot(self.average_scores, color="#fc8803", linestyle='-', label='25-Episode Moving Average', linewidth=2)
        self.ax1.set_xlabel('Episode')
        self.ax1.set_ylabel('Score')
        self.ax1.tick_params(axis='y')
        self.ax1.set_title('Score')
        self.ax1.legend(loc='best')
        self.ax1.grid(True)

        # Reward subplot
        self.reward_line, = self.ax2.plot(self.rewards, color="#99ff99", linestyle='-', label='Reward')
        self.avg_reward_line, = self.ax2.plot(self.average_rewards, color="#009900", linestyle='-', label='25-Episode Moving Average', linewidth=2)
        self.ax2.set_xlabel('Episode')
        self.ax2.set_ylabel('Reward')
        self.ax2.tick_params(axis='y')
        self.ax2.set_title('Reward')
        self.ax2.legend(loc='best')
        self.ax2.grid(True)

        # Survive duration subplot
        self.survive_line, = self.ax3.plot(self.survive_durations, color="#9999ff", linestyle='-', label='Survive Duration')
        self.avg_survive_line, = self.ax3.plot(self.average_survive_durations, color="#0000cc", linestyle='-', label='25-Episode Moving Average', linewidth=2)
        self.ax3.set_xlabel('Episode')
        self.ax3.set_ylabel('Survive Duration')
        self.ax3.tick_params(axis='y')
        self.ax3.set_title('Survive Duration')
        self.ax3.legend(loc='best')
        self.ax3.grid(True)

    def log_data(self, reward, survive_duration, score):
        """Logs the received reward and survive duration, updates moving averages."""
        self.scores.append(score)
        self.rewards.append(reward)
        self.survive_durations.append(survive_duration)

        # Update moving average for score
        if len(self.scores) <= 25:
            avg_scores = sum(self.scores) / len(self.scores)
        else:
            avg_scores = sum(self.scores[-25:]) / 25
        self.average_scores.append(avg_scores)

        # Update moving average for rewards
        if len(self.rewards) <= 25:
            avg_reward = sum(self.rewards) / len(self.rewards)
        else:
            avg_reward = sum(self.rewards[-25:]) / 25
        self.average_rewards.append(avg_reward)

        # Update moving average for survive durations
        if len(self.survive_durations) <= 25:
            avg_survive_duration = sum(self.survive_durations) / len(self.survive_durations)
        else:
            avg_survive_duration = sum(self.survive_durations[-25:]) / 25
        self.average_survive_durations.append(avg_survive_duration)

    def update_plot(self):
        """Updates the plot with new data for rewards, moving average, survive durations, and their moving average."""
        x_data = range(len(self.rewards))
        self.score_line.set_data(x_data, self.scores)
        self.avg_score_line.set_data(x_data, self.average_scores)
        self.reward_line.set_data(x_data, self.rewards)
        self.avg_reward_line.set_data(x_data, self.average_rewards)
        self.survive_line.set_data(x_data, self.survive_durations)
        self.avg_survive_line.set_data(x_data, self.average_survive_durations)

        # Rescale both y-axes
        self.ax1.relim()
        self.ax1.autoscale_view()
        self.ax2.relim()
        self.ax2.autoscale_view()
        self.ax3.relim()
        self.ax3.autoscale_view()

        self.fig.tight_layout()
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.01)