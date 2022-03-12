import os
import time
import gym
import gym_sokoban
from stable_baselines3 import PPO, A2C
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import CheckpointCallback
from config import path_logs, path_models


class RewardLoggerCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """
    def __init__(self, verbose=0):
        super(RewardLoggerCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`..

        :return: (bool) If the callback returns False, training is aborted early.
        """
        # Log training reward
        reward = self.locals['rewards'][0]
        print(reward)
        return True


class ExitOnInvalidMoveCallback(BaseCallback):
    """
    A custom callback that derives from ``BaseCallback``.

    :param verbose: (int) Verbosity level 0: not output 1: info 2: debug
    """
    def __init__(self, threshold=0, verbose=0):
        super(ExitOnInvalidMoveCallback, self).__init__(verbose)
        self.threshold = threshold

    def _on_step(self) -> bool:
        """
        This method will be called by the model after each call to `env.step()`..

        :return: (bool) If the callback returns False, training is aborted early.
        """
        reward = self.locals['rewards'][0]

        # If an invalid action is performed enough times, then abort early.
        counter = 0
        if reward == -1:
            counter += 1

        if counter >= self.threshold:
            print("Abort due to invalid action threshold")
            return False

        return True


class Solver:
    def __init__(self, path_model, env_name="Sokoban-v0", policy_kwargs=None):
        self.env_name = env_name
        self.path_model = path_model
        self.policy_kwargs = policy_kwargs
        self.env = gym.make(self.env_name)
        self.env.set_maxsteps(200)
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            model = PPO.load(self.path_model, self.env)
            self.model = model
        except FileNotFoundError:
            print(f'Could not find model at: {self.path_model} Creating new model...')
            model = PPO('MlpPolicy', self.env, verbose=1, tensorboard_log=path_logs, policy_kwargs=self.policy_kwargs,
                        learning_rate=0.0001)
            self.model = model

    def evaluate_model(self, episodes=10, render=True):
        print(evaluate_policy(self.model, self.env, n_eval_episodes=episodes, render=render, deterministic=False))

    def test(self, games=5, steps=100):
        for i in range(games):
            obs = self.env.reset()
            for j in range(steps):
                action, _state = self.model.predict(obs, deterministic=False)
                obs, reward, done, info = self.env.step(action)
                self.env.render(mode="human")
                time.sleep(0.05)
                if done:
                    obs = self.env.reset()

    def random_sampling(self, games=5, steps=100):
        for i in range(games):
            obs = self.env.reset()
            for j in range(steps):
                action = self.env.action_space.sample()
                obs, reward, done, info = self.env.step(action)
                self.env.render(mode="human")
                time.sleep(0.05)
                if done:
                    obs = self.env.reset()
                    print("done")

    def train_model(self, total_time_steps, save_freq=50000, callbacks=None):
        if callbacks is None:
            callbacks = []

        checkpoint_callback = CheckpointCallback(save_freq=save_freq, save_path=f'{self.path_model}_checkpoints', name_prefix='rl_model')

        self.model.learn(total_timesteps=total_time_steps, callback=[checkpoint_callback, *callbacks])
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
            model = A2C('MlpPolicy', self.env, verbose=1, tensorboard_log=path_logs, policy_kwargs=self.policy_kwargs, learning_rate=0.000007)
            self.model = model
            self.save_model()


def main():
    policy_kwargs = dict(net_arch=[dict(pi=[512, 512], vf=[512, 512])])
    reward_logger_callback = RewardLoggerCallback()
    # invalid_move_callback = ExitOnInvalidMoveCallback()

    solver = Solver(os.path.join(path_models, 'PPO_C1'), env_name='Sokoban-learn-v0', policy_kwargs=policy_kwargs)
    # solver.train_model(20000, callbacks=[reward_logger_callback])
    # solver.test()
    solver.evaluate_model()
    solver.close()

    # solver = Solver(os.path.join(path_models, 'PPO_D8'), env_name='Sokoban-learn-v0', policy_kwargs=policy_kwargs)
    # solver.train_model(20000, callbacks=[reward_logger_callback])
    # solver.test()
    # solver.evaluate_model()
    # solver.close()

    # Cart pole test
    # solver2 = Solver(env_name='CartPole-v0', path_model=os.path.join(path_models, 'cart-pole'))
    # solver2.train_model(10000)
    # solver2.evaluate_model(episodes=20, render=True)
    # solver2.close()


if __name__ == '__main__':
    main()
