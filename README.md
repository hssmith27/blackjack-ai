# Blackjack AI Trainer

This project allows users to practice their Blackjack decision making by comparing their choices with an optimal policy found by AI.

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