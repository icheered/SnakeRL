import matplotlib.pyplot as plt
from IPython import display

# Interactive plot
plt.ion()

# Create 4 subplots for each metric
fig, axes = plt.subplots(4, 1, figsize=(10, 12))

def plot_metrics(scores, rewards, epsilons):
    display.clear_output(wait=True)
    
    # Clear current plots
    for ax in axes:
        ax.clear()

    # Plot Scores
    axes[0].set_title('Scores')
    axes[0].plot(scores)
    axes[0].text(len(scores) - 1, scores[-1], str(scores[-1]))

    # Plot Moving average of  Scores
    mean_scores = [sum(scores[i-50:i])/50 if i > 50 else sum(scores[:i])/i for i in range(1, len(scores))]
    axes[1].set_title('Moving average of Scores')
    axes[1].plot(mean_scores, color='orange')
    axes[1].text(len(mean_scores) - 1, mean_scores[-1], str(round(mean_scores[-1], 1)))
    

    # Plot Rewards
    axes[2].set_title('Rewards')
    axes[2].plot([reward[0] for reward in rewards], color='orange') # Plotting all first elements
    axes[2].plot([reward[1] for reward in rewards], color='blue')  # Plotting all second elements
    axes[2].plot([reward[2] for reward in rewards], color="green")   # Plotting all third elements
    
    axes[2].plot([], [], color='green', label='Total Reward')
    axes[2].plot([], [], color='red', label='Score Reward')
    axes[2].plot([], [], color='blue', label='Moving to Apple Reward')


    # Plot Epsilons
    axes[3].set_title('Epsilons')
    axes[3].plot(epsilons, color='red')
    axes[3].text(len(epsilons) - 1, epsilons[-1], str(round(epsilons[-1], 1)))

    # Adjust layout
    plt.tight_layout()

    display.display(fig)  # Display the figure
    plt.pause(0.1)
