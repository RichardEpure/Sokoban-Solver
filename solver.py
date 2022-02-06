import gym
import gym_sokoban
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from config import path_logs, path_PPO


class Solver:
    def __init__(self, env_name="Sokoban-v0", path_model=path_PPO):
        self.env_name = env_name
        self.path_model = path_model
        self.env = None
        self.model = None
        self._set_env()
        self.load_model()

    def _set_env(self):
        env = gym.make(self.env_name)
        self.env = DummyVecEnv([lambda: env])

    def load_model(self):
        try:
            model = PPO.load(self.path_model, self.env)
            self.model = model
        except FileNotFoundError:
            model = PPO('MlpPolicy', self.env, verbose=1, tensorboard_log=path_logs)
            self.model = model

    def evaluate_model(self, episodes=10, render=False):
        print(evaluate_policy(self.model, self.env, n_eval_episodes=episodes, render=render))

    def test_model(self, episodes=5, render=False):
        for i in range(1, episodes + 1):
            obs = self.env.reset()
            done = False
            score = 0

            while not done:
                if render:
                    self.env.render(mode="human")
                action, states = self.model.predict(obs)
                obs, reward, done, info = self.env.step(action)
                score += reward
            print(f'Episode:{i} Score:{score}')

    def train_model(self, total_time_steps):
        self.model.learn(total_timesteps=total_time_steps)

    def save_model(self):
        self.model.save(self.path_model)

    def close(self):
        self.env.close()


def main():
    solver = Solver()
    solver.test_model(render=True)
    solver.close()


if __name__ == '__main__':
    main()
