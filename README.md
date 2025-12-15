# Blackjack Q-Learning Agent

This project is a reinforcement learning agent that plays Blackjack using Q-learning with card counting.

## Project Overview

This project implements a tabular Q-learning agent for Blackjack. It learns an optimal policy through repeated play in a Blackjack environment.

## State Representation

To restrict the size of the state, the state only contains the following information:
(player_total, is_player_val_soft, dealer_total, can_split, can_double, true_count)

## Learning Method

- Algorithm: Q-Learning
- Exploration: Epsilon-Greedy
- Rewards: Hand outcomes

## How to Run

1. **Train the Agent:**
Run `agent_training.py` for a desired number of iterations, you can also modify learning rate and epsilon in `blackjack_agent.py`. In practice, I've found that a very high epsilon value and a low learning rate with >= 100,000,000
iterations works well for convergence.

2. **Test the Agent:**
Run `test_agent.py` to check how well the agent is doing. Run at least 1,000,000 iterations to ensure proper performance in the long-run.

3. **Inspect the Policy:**
Check the agent's policy at specific states with `blackjack_agent.get_policy()`.

4. **Adjust other Parameters:**
Now that you know how to train and test the model, you can try altering other parameters like the number of decks per shoe or the shoe penetration in `game.py`.