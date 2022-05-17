import ray
from ray import tune

from run_everything import CustomEnv
from ray.rllib import agents

import gym


if False:
    tune.run(
        "SAC", # reinforced learning agent
        name = "Training4",
        # to resume training from a checkpoint, set the path accordingly:
        # resume = True, # you can resume from checkpoint
        # restore = r'.\ray_results\Example\SAC_RocketMeister10_ea992_00000_0_2020-11-11_22-07-33\checkpoint_3000\checkpoint-3000',
        checkpoint_freq = 100,
        checkpoint_at_end = True,
        local_dir = r'./ray_results/',
        config={
            "env": CustomEnv,
            "num_workers": 30,
            "num_cpus_per_worker": 0.5,
            "env_config":{
                "max_steps": 1000,
                "export_frames": True,
                "export_states": True,
                # "reward_mode": "continuous",
                # "env_flipped": True,
                # "env_flipmode": True,
                }
            },
        stop = {
            "timesteps_total": 5_000_000,
            },
        )
    
if False:
    env_cart = gym.make('CartPole-v0')
    env_cart.reset()
    tune.run(
        "SAC", # reinforced learning agent
        name = "CartpoleTest3",
        # to resume training from a checkpoint, set the path accordingly:
        # resume = True, # you can resume from checkpoint
        # restore = r'.\ray_results\Example\SAC_RocketMeister10_ea992_00000_0_2020-11-11_22-07-33\checkpoint_3000\checkpoint-3000',
        checkpoint_freq = 100,
        checkpoint_at_end = True,
        local_dir = r'./ray_results/',
        config={
            "env": env_cart,
            "num_workers": 30,
            "num_cpus_per_worker": 0.5,
            "env_config":{
                "max_steps": 1000,
                "monitor" : True,
                "export_frames": True,
                "export_states": True,
                # "reward_mode": "continuous",
                # "env_flipped": True,
                # "env_flipmode": True,
                }
            },
        
        stop = {
            "timesteps_total": 10,
            },
        )


if False:
    env = gym.make("CartPole-v0")
    env.reset() # Instantiate enviroment with default parameters
    
    results = tune.run(
        'SAC',
        stop={
            'timesteps_total': 500000
        },
        name = "CartPoleMonitor0",
        local_dir = r'./ray_results/',
        config={
            "env": env,
            "num_workers": 20,
            "num_cpus_per_worker": 0.5,
            "monitor" : True
        }
    )
    
if False:
    config = {'gamma': 0.999,
        'lr': 0.0001,
        "n_step": 1000,
        'num_workers': 3,
        'monitor': True}
    trainer2 = agents.dqn.DQNTrainer(env='LunarLander-v2', config=config)
    results2 = trainer2.train()
    
    
if True:

    ray.init() # Skip or set to ignore if already called
    config = {'gamma': 0.9,
            'lr': 1e-2,
            'num_workers': 4,
            'train_batch_size': 1000,
            'monitor' : True,
            'model': {
                'fcnet_hiddens': [128, 128]
            }}
    print(dir(agents))
    #trainer = agents.ppo.PPOTrainer(env='CartPole-v0', config=config)
    #results = trainer.train()