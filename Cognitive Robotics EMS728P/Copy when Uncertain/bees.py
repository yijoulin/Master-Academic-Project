import numpy as np
import random
from collections import defaultdict

class bee:
    def __init__(self, individual_probability = 0.5):
        # bee's age: len(self.memory)
        # every bees has a dict to record the past experience
        self.memory = defaultdict(float)
        self.last_patch = 0
        self.age = 0

        # every bee is rather individual learner or social learner
        # individual learner will be 1 else 0 depends on the probability
        if random.random() < individual_probability:
            self.individual = 1
        else: self.individual = 0
    
    def update_memory(self, current_sucrose, index):
        self.memory[index] = current_sucrose
        self.last_patch = index
        self.age += 1
    
    def get_best_patch(self):
        return max(self.memory, key=self.memory.get)
    
    def replace(self, individual_probability):
        self.memory = defaultdict(float)
        self.last_patch = 0
        self.age = 0

        if random.random() < individual_probability:
            self.individual = 1
        else: self.individual = 0