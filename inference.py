from env import GameEnv, Action

env = GameEnv()
obs = env.reset()

print("[START]")

for step in range(5):
    action = Action(
        action_type="attack",
        explanation="I attack strategically to reduce enemy health"
    )

    obs, reward, done, _ = env.step(action)

    print(f"[STEP] {step} ACTION={action.action_type} REWARD={reward}")

    if done:
        break

print("[END]")