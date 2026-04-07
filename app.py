import gradio as gr
from env import GameEnv, Action
import matplotlib.pyplot as plt

env = GameEnv()
env.reset()

total_score = 0
score_history = []

# 🎯 Difficulty multiplier
def get_multiplier(level):
    if level == "Easy":
        return 0.8
    elif level == "Medium":
        return 1.0
    else:
        return 1.2

# 🤖 Smart AI suggestion
def ai_suggestion(state):
    if state.enemy_health < 30:
        return "🔥 Attack now to finish the enemy!"
    elif state.player_health < 30:
        return "🛡️ Defend to regain health!"
    else:
        return "💰 Collect resources for future advantage!"

# 📊 Plot score graph
def plot_scores():
    plt.figure()
    plt.plot(score_history, marker='o')
    plt.title("Score Progress")
    plt.xlabel("Turn")
    plt.ylabel("Score")
    return plt

def play(action, explanation, difficulty):
    global total_score, score_history

    obs, reward, done, _ = env.step(Action(
        action_type=action,
        explanation=explanation
    ))

    reward *= get_multiplier(difficulty)
    total_score += reward
    score_history.append(total_score)

    # Feedback
    if reward > 0.7:
        feedback = "🔥 Excellent strategic move!"
    elif reward > 0.4:
        feedback = "👍 Good decision!"
    else:
        feedback = "⚠️ Weak reasoning."

    suggestion = ai_suggestion(obs)

    return f"""
🎮 GAME STATE

❤️ Player Health: {obs.player_health}
⚔️ Enemy Health: {obs.enemy_health}
💰 Resources: {obs.resources}
🔁 Turn: {obs.turn}

🏆 Reward: {round(reward,2)}
📈 Total Score: {round(total_score,2)}

🎯 Difficulty: {difficulty}

🧠 Feedback:
{feedback}

🤖 AI Suggestion:
{suggestion}

{"🏁 GAME OVER" if done else ""}
""", plot_scores()

def reset_game():
    global total_score, score_history
    total_score = 0
    score_history = []
    env.reset()
    return "🔄 Game Reset!", None

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("## 🎮 AI Game Strategist Ultimate")
    gr.Markdown("### 🚀 Intelligent decision simulator with analytics")

    difficulty = gr.Radio(["Easy", "Medium", "Hard"], value="Medium", label="🎯 Difficulty")

    with gr.Row():
        action = gr.Radio(["attack", "defend", "collect"], label="🎮 Action")
        explanation = gr.Textbox(label="🧠 Explain your strategy")

    output = gr.Textbox(label="📊 Result")
    graph = gr.Plot(label="📈 Score Progress")

    with gr.Row():
        play_btn = gr.Button("🚀 Run Strategy")
        reset_btn = gr.Button("🔄 Reset")

    play_btn.click(play, [action, explanation, difficulty], [output, graph])
    reset_btn.click(reset_game, outputs=[output, graph])

app.launch()