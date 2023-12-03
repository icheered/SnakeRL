import matplotlib.pyplot as plt
from IPython import display

# Interactive plot
plt.ion()

# Create 4 subplots for each metric
fig, axes = plt.subplots(4, 1, figsize=(10, 12))

def plot_metrics(scores, mean_scores, rewards, epsilons):
    display.clear_output(wait=True)
    
    # Clear current plots
    for ax in axes:
        ax.clear()

    # Plot Scores
    axes[0].set_title('Scores')
    axes[0].plot(scores)
    axes[0].text(len(scores) - 1, scores[-1], str(scores[-1]))

    # Plot Mean Scores
    axes[1].set_title('Mean Scores')
    axes[1].plot(mean_scores, color='orange')
    axes[1].text(len(mean_scores) - 1, mean_scores[-1], str(round(mean_scores[-1], 1)))

    # Plot Rewards
    axes[2].set_title('Rewards')
    axes[2].plot(rewards, color='green')
    axes[2].text(len(rewards) - 1, rewards[-1], str(round(rewards[-1], 1)))

    # Plot Epsilons
    axes[3].set_title('Epsilons')
    axes[3].plot(epsilons, color='red')
    axes[3].text(len(epsilons) - 1, epsilons[-1], str(round(epsilons[-1], 1)))

    # Adjust layout
    plt.tight_layout()

    display.display(fig)  # Display the figure
    plt.pause(0.1)
