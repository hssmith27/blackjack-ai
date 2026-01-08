# Blackjack AI Trainer

This project is a Blackjack training application that helps users improve their decision-making by comparing their actions against an AI-generated policy trained with Q-learning.

This project started with the goal of generating an AI-generated policy for Blackjack with more possible acitons than other works have accomplished. It's been expanded into a full-stack training application to help show potential applications for the work.

## Project Overview

While Blackjack isn't as complicated as a game like chess, it still presents numerous challenges for reinforcement learning due to:
* Large state space
* Random card draws
To handle these issues, I carefully reduced the state space and adjusted parameters to train the model on numerous iterations, reducing the impact of random card draws.

## How to Run

1. **Train the Agent:**
Run `agent_training.py` for a desired number of iterations, you can also modify learning rate and epsilon in `blackjack_agent.py`. In practice, I've found that a very high epsilon value and a low learning rate with >= 100,000,000 iterations works well for convergence.

2. **Start the Backend:**
Run `optimal_policy.py` to start up the backend, allowing the frontend to fetch the optimal_policy.

3. **Start the Frontend:**
Enter the `frontend` directory and run `npm start` to start the frontend.

4. **Start Practicing:**
Go to `http://localhost:3000/` and start practicing!

## AI Model Notes

While the AI model isn't 100% accurate, its policy is effective enough to generate an edge of around 1.8% in general casino conditions.

## Future Improvements
* Add login / registration to allow players to track their performance across sessions
* Add additional parameters to let players choose what conditions they want to practice in (ex: dealer standing on soft 17)
* Further improve the model's training process to make it converge closer to the calculated optimal policy
* Focus on showing users more difficult situations, rather than just any situtation that can be generated