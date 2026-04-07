from pydantic import BaseModel
import random

class Observation(BaseModel):
    player_health: int
    enemy_health: int
    resources: int
    turn: int

class Action(BaseModel):
    action_type: str
    explanation: str

class GameEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player_health = 100
        self.enemy_health = 100
        self.resources = 2
        self.turn = 0
        return self.state()

    def state(self):
        return Observation(
            player_health=self.player_health,
            enemy_health=self.enemy_health,
            resources=self.resources,
            turn=self.turn
        )

    def step(self, action: Action):
        self.turn += 1
        reward = 0

        if action.action_type == "attack":
            self.enemy_health -= random.randint(10, 20)
            reward += 0.4

        elif action.action_type == "defend":
            self.player_health += 5
            reward += 0.2

        elif action.action_type == "collect":
            self.resources += 1
            reward += 0.3

        # Enemy attack
        self.player_health -= random.randint(5, 15)

        # Explanation reward
        if len(action.explanation) > 10:
            reward += 0.3

        done = False
        if self.enemy_health <= 0:
            reward += 1
            done = True
        elif self.player_health <= 0:
            reward -= 1
            done = True

        return self.state(), round(reward, 2), done, {}