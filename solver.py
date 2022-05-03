import os
import time

import gym
import gym_sokoban
import numpy as np

from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.callbacks import BaseCallback
from stable_baselines3.common.callbacks import CheckpointCallback

from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from sb3_contrib.common.maskable.utils import get_action_masks
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib.ppo_mask import MaskablePPO

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


class RelevantRewardLoggerCallback(BaseCallback):
    def __init__(self, verbose=0):
        super(RelevantRewardLoggerCallback, self).__init__(verbose)

    def _on_step(self) -> bool:
        reward = self.locals['rewards'][0]
        if reward > 0 or reward < -0.2:
            print(reward)
        return True


class Solver:
    def __init__(self, path_model, env_name="Sokoban-v0", policy_kwargs=None):
        self.env_name = env_name
        self.path_model = path_model
        self.policy_kwargs = policy_kwargs
        self.env = None
        self.model = None
        self._setup_environment()
        self.load_model()

    def _setup_environment(self):
        self.env = gym.make(self.env_name)
        self.env.set_maxsteps(200)

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
            print(f'episode: {i}')
            for j in range(steps):
                action, _state = self.model.predict(obs, deterministic=False)
                obs, reward, done, info = self.env.step(action)
                print(f'{j} - action: {action}, reward: {reward}')
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


class MaskableSolver(Solver):
    def __init__(self, path_model, env_name="Sokoban-v0", policy_kwargs=None):
        super().__init__(path_model, env_name, policy_kwargs)

    def _setup_environment(self):
        super()._setup_environment()
        self.env = ActionMasker(self.env, mask_function)

    def load_model(self):
        try:
            model = MaskablePPO.load(self.path_model, self.env)
            self.model = model
        except FileNotFoundError:
            print(f'Could not find model at: {self.path_model} Creating new model...')
            model = MaskablePPO(MaskableActorCriticPolicy, self.env, verbose=1,
                                tensorboard_log=path_logs, policy_kwargs=self.policy_kwargs,
                                n_steps=50000, batch_size=25000, learning_rate=0.003)
            self.model = model
            self.save_model()

    def test(self, games=10, steps=100):
        for i in range(games):
            obs = self.env.reset()
            print(f'episode: {i}')
            for j in range(steps):
                action_masks = get_action_masks(self.env)
                action, _state = self.model.predict(obs, deterministic=False, action_masks=action_masks)
                obs, reward, done, info = self.env.step(action)
                if reward > 0 or reward < -0.2:
                    print(f'{j}, action: {action}, reward: {reward} -- action_masks: {action_masks}')
                self.env.render(mode="human")
                time.sleep(0.1)
                if done:
                    obs = self.env.reset()
                    break


def mask_function(env: gym.Env) -> np.ndarray:
    return env.valid_action_mask()


def main():
    policy_kwargs = dict(net_arch=[dict(pi=[256, 256], vf=[256, 256])])
    reward_logger_callback = RewardLoggerCallback()
    relevant_reward_logger_callback = RelevantRewardLoggerCallback()

    solver_mask = MaskableSolver(os.path.join(path_models, 'rl_model'), env_name='Sokoban-v0', policy_kwargs=policy_kwargs)
    # solver_mask.train_model(20000000, callbacks=[relevant_reward_logger_callback])
    solver_mask.test()
    solver_mask.close()

    # Cart pole test
    # solver2 = Solver(env_name='CartPole-v0', path_model=os.path.join(path_models, 'cart-pole'))
    # solver2.train_model(10000)
    # solver2.evaluate_model(episodes=20, render=True)
    # solver2.close()


if __name__ == '__main__':
    main()
