import pickle
from blackjack_model.blackjack_agent import BlackjackAgent

MAX_ITER = 100000

agent = BlackjackAgent()

# Train agent MAX_ITER times
for _ in range(MAX_ITER):
    agent.run_episode()

# Check learned states and parameter values
print(len(agent.q_vals))
print(agent.epsilon)
print(agent.alpha)

# Save agent
with open("blackjack_model/blackjack_agent.pkl", "wb") as f:
    pickle.dump(agent, f)