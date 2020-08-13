class Option:
    def __init__(self, name, policy, start_condition, end_condition):
        self.name = name
        self.policy = policy
        self.start_condition = start_condition
        self.end_condition = end_condition

    def can_start(self, state):
        return self.start_condition(state)

    def should_end(self, state):
        return self.end_condition(state)

    def action(self, state):
        return self.policy.action(state)

class PrimitiveOption:
    def __init__(self, action):
        self.name = action.name
        self.primitive = action

    def can_start(self, state):
        return True
    
    def should_end(self, state):
        return True

    def action(self, state):
        return self.primitive

