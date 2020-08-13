import numpy as np

def learn_episodic(world_gen,
        policy,
        reward_func,
        max_steps,
        max_episodes,
        alpha,
        epsilon,
        discount_rate):

    for episode in range(max_episodes):
        env = world_gen(episode)
        for step in range(max_steps):
            # agent state
            s = env.agent_state()

            # get action from policy
            policy.epsilon = epsilon(step)
            a = policy.action(s)
            
            # perform action
            env.step(a)
            s_prime = env.agent_state()

            # get reward
            reward = reward_func(env)

            # update policy if option ended
            if policy.option_did_finished(s):
                o = policy.current_option_index
                o_prime = np.argmax(policy.q_values(s))
                td_target = reward + discount_rate * policy.q_value(s_prime, o_prime)
                q_value = policy.q_value(s, o)
                td_delta = td_target - q_value
                policy.update_q(s, o, q_value + alpha(step)*td_delta)

            if env.goal_achieved():
                break

