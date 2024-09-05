import random
import numpy as np
from collections import defaultdict
import bees
import patches

class arena:
    # Arena including all the operations of bees and environment(patches)
    def __init__(self,type_name, flowers_number, bees_number):
        self.name = type_name
        self.flowers_number = flowers_number
        self.gamma_k = 0.273
        self.gamma_theta = 30.4
        self.patches = self.create_environment()
        self.bees = self.create_bees(bees_number)
        self.exploited = []

    def create_bees(self, bees_number):
        temp=[]
        for i in range(1, bees_number+1):
            if i%2 == 0:
                temp.append(bees.bee(individual_probability =1))
            else:
                temp.append(bees.bee(individual_probability =0))
        return temp

    def create_environment(self):
        if self.name == "no_variance":
            return np.array([patches.patch(8.3) for _ in range(self.flowers_number)]) # create pi surcose equally divided
        elif self.name == "high_variance": 
            pi_list = np.random.gamma(self.gamma_k, self.gamma_theta, self.flowers_number)
            return np.array([patches.patch(pi) for pi in pi_list]) #use gamma distribution to randomly assign the values
        

    def get_individual_probability(self):
        individual_fitness, social_fitness = 0, 0
        for bee in self.bees:
            if bee.individual: individual_fitness += bee.memory[bee.last_patch]
            else: social_fitness += bee.memory[bee.last_patch]
        return individual_fitness/(individual_fitness+social_fitness)
    
    def get_individual_probabilityy(self):
        temp = self.get_individual_learner()
        return temp/len(self.bees)
    
    def get_individual_learner(self):
        sum = 0
        for bee in self.bees:
            if bee.individual:
                sum +=1
        return sum 
    
    def update_patches(self):
        # update patches
        if random.random() < 10e-4:
            update_patch =  random.randint(0, self.flowers_number-1)
            self.patches[update_patch].pi = np.random.gamma(self.gamma_k, self.gamma_theta)
    
    def update_bees(self):
        # update bees
        prob = self.get_individual_probability()
        for bee in self.bees: 
            if bee.age == 100 or random.random() < 0.02:
                bee.replace(prob)

    def forage(self, timestep = 1):
        bee_visit_list=[]
        new_exploited = []
        for index, bee in enumerate(self.bees):
            if random.random() < 0.70 :
                new_exploited.append(index)
                patch_add = self.exploit(bee)
            else:
                if bee.individual or len(self.exploited) ==0:
                    patch_add = self.learn()
                else:
                    patch_add = self.explore(self.exploited[random.randint(0,len(self.exploited)-1)])
            bee_visit_list.append(patch_add)
            

            # update patches' individual or social
            if bee.individual:
                self.patches[bee_visit_list[-1]].bees_individual += 1
            else:
                self.patches[bee_visit_list[-1]].bees_social += 1

        self.exploited = new_exploited
        # count bees' number in each patch
        patch_counts = defaultdict(int)
        for number in bee_visit_list:
            patch_counts[number] += 1
        
        for index, bee in enumerate(self.bees):
            patch_index = bee_visit_list[index]
            current_sucrose = self.patches[patch_index].pi/(patch_counts[patch_index])
            bee.update_memory(current_sucrose, patch_index)

    def exploit(self, bee):
        if len(bee.memory) == 0:
            return random.randint(0,self.flowers_number-1)
        else:
            return bee.get_best_patch()
    
    def explore(self, index):
        if len(self.bees[index].memory) == 0:
            return random.randint(0, self.flowers_number-1)
        else:
            return self.bees[index].get_best_patch()
    
    def learn(self):
        return random.randint(0, self.flowers_number-1)

    def get_patches_list(self):
        patch_list = []
        for k, patch in enumerate(self.patches):
            if(k%10 == 0):
                temp=[]
                if k>1:
                    patch_list.append(temp)
            temp.append(patch.pi)
        patch_list.append(temp)
        return patch_list
    
    def get_bees_list(self):
        bee_individual_total, bee_social_total = 0,0
        bee_list = []

        individual_color = 'blue'
        social_color = 'red'
        for patch in self.patches:
            current_patch_bee_list = []
            if patch.bees_individual > 0:
                bee_individual_total += patch.bees_individual
                for _ in range(patch.bees_individual):
                    current_patch_bee_list.append('blue')
            elif patch.bees_social > 0:
                bee_social_total += patch.bees_social
                for _ in range(patch.bees_social):
                    current_patch_bee_list.append('red')
            bee_list.append(current_patch_bee_list)

        patch_list = []
        for k, patch in enumerate(bee_list):
            if(k%10 == 0):
                temp=[]
                if k>1:
                    patch_list.append(temp)
            temp.append(patch)
        patch_list.append(temp)

        return bee_individual_total, bee_social_total, patch_list
    
    def clear(self):
        for patch in self.patches:
            patch.bees_individual = 0
            patch.bees_social = 0 

