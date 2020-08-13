import numpy as np

from collections import defaultdict

class GreedyPolicy:
    def __init__(self, options):
        # copy options
        self.options = []
        for option in options:
            self.options.append(option)
        
        self.q = defaultdict(lambda: np.zeros(len(self.options)))
        self.current_option = None
        self.current_option_index = None
        self.epsilon = 0

    def best_option_index(self, state):
        q_values = self.q[state]

        best_option_q = None
        best_option_i = None

        for i in possible_options(self.options, state):
            if best_option_q is None or q_values[i] > best_option_q:
                best_option_q = q_values[i]
                best_option_i = i

        return best_option_i

    def option_index(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(possible_options(self.options, state))
        else:
            return self.best_option_index(state)

    def action(self, state):
        if self.current_option is None or self.current_option.should_end(state):
            self.current_option_index = self.option_index(state)
            self.current_option = self.options[self.current_option_index]
        
        return self.current_option.action(state)

    def option_did_finished(self, state):
        return self.current_option.should_end(state)

    def q_values(self, state):
        return self.q[state]

    def q_value(self, state, option):
        return self.q[state][option]
    
    def update_q(self, state, option, value):
        self.q[state][option] = value

    def __str__(self):
        s = ''
        for state, q_values in self.q.items():
            s += '{}: {} {}\n'.format(state, self.options[self.best_option_index(state)].name, q_values)

        return s



def possible_options(options, state):
    possible = []
    for i in range(len(options)):
        possible.append(i)

    return possible
