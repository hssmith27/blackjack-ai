import pickle
from blackjack_agent import BlackjackAgent

MAX_ITER = 150000000
agent = BlackjackAgent()

for _ in range(MAX_ITER):
    agent.run_episode()

print(len(agent.q_vals))
print(agent.epsilon)
print(agent.alpha)

# Save agent
with open("blackjack_agent.pkl", "wb") as f:
    pickle.dump(agent, f)