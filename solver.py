import os
import time
import gym
import gym_sokoban
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import EvalCallback
from config import path_logs, path_models


class Solver:
    def __init__(self, path_model, env_name="Sokoban-v0", policy_kwargs=None):
        self.env_name = env_name
        self.path_model = path_model
        self.policy_kwargs = policy_kwargs
        self.env = gym.make(self.env_name)
        # self.env = DummyVecEnv([lambda: env])
        # self.eval_callback = EvalCallback(self.env,
        #                                   eval_freq=500000,
        #                                   best_model_save_path=path_models,
        #                                   verbose=1)
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            model = PPO.load(self.path_model, self.env)
            self.model = model
        except FileNotFoundError:
            print(f'Could not find model at: {self.path_model} Creating new model...')
            model = PPO('MlpPolicy', self.env, verbose=1, tensorboard_log=path_logs, policy_kwargs=self.policy_kwargs)
            self.model = model
            self.save_model()

    def evaluate_model(self, episodes=10, render=False):
        print(evaluate_policy(self.model, self.env, n_eval_episodes=episodes, render=render))

    def test(self, games=5, steps=100):
        for i in range(games):
            obs = self.env.reset()
            for j in range(steps):
                action, _state = self.model.predict(obs, deterministic=True)
                obs, reward, done, info = self.env.step(action)
                self.env.render(mode="human")
                time.sleep(0.1)
                if done:
                    obs = self.env.reset()

    def random_sampling(self, games=5, steps=100):
        for i in range(games):
            obs = self.env.reset()
            for j in range(steps):
                action = self.env.action_space.sample()
                obs, reward, done, info = self.env.step(action)
                self.env.render(mode="human")
                time.sleep(0.1)
                if done:
                    obs = self.env.reset()
                    print("done")

    def train_model(self, total_time_steps, iterations=1):
        for i in range(iterations):
            self.model.learn(total_timesteps=total_time_steps)
            self.save_model()

    def save_model(self):
        self.model.save(self.path_model)

    def close(self):
        self.env.close()


class SolverA2C(Solver):
    def __init__(self, path_model, env_name="Sokoban-v0", policy_kwargs=None):
        super().__init__(path_model, env_name, policy_kwargs)

    def load_model(self):
        try:
            model = A2C.load(self.path_model, self.env)
            self.model = model
        except FileNotFoundError:
            print(f'Could not find model at: {self.path_model} Creating new model...')
            model = A2C('MlpPolicy', self.env, n_steps=1000, verbose=1, tensorboard_log=path_logs, policy_kwargs=self.policy_kwargs)
            self.model = model
            self.save_model()


def main():
    policy_kwargs = dict(net_arch=[dict(pi=[1024, 1024], vf=[4096, 4096])])

    solver = Solver(os.path.join(path_models, 'PPO'))
    solver.random_sampling()
    solver.close()

    # solver_soko = SolverA2C(os.path.join(path_models, 'A2C-SokobanV3'), policy_kwargs=policy_kwargs)
    # solver_soko.train_model(10000)
    # # solver_soko.evaluate_model(render=True)
    # solver_soko.test()
    # solver_soko.close()

    # solver2 = Solver(env_name='CartPole-v0', path_model=os.path.join(path_models, 'cart-pole'))
    # solver2.train_model(5000)
    # solver2.evaluate_model(render=True)
    # solver2.close()


if __name__ == '__main__':
    main()
