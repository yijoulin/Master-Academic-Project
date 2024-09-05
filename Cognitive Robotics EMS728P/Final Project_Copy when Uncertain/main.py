import numpy as np
import arena 
import plots
import test

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class model:
    def __init__(self,bees_number,patches_number,type_name):
        # create environment
        self.arena = arena.arena(type_name=type_name, flowers_number=patches_number, bees_number=bees_number)
        self.arena.create_environment()
        self.record = []
        self.patch_list = []
        self.bee_list = []
        self.number_of_social_bee = []
        self.number_of_individual_bee = []

    def train(self, timestep):
        self.arena.forage(timestep)
        self.arena.update_bees()
    
    def update_parameters(self):
        self.patch_list.append(self.arena.get_patches_list())
        bee_individual_total, bee_social_total,bee_list = self.arena.get_bees_list()
        self.bee_list.append(bee_list)
        self.number_of_social_bee.append(bee_social_total)
        self.number_of_individual_bee.append(bee_individual_total)

        self.arena.clear()
    
if __name__ == '__main__':
    # parameters setting
    patches_number, bees_number = 100, 33
    simulation_numbers = 100
    timesteps, recording = 800, 300
    total_record_no_variance = []
    total_record_high_variance = []

    # training
    for simulation in range(simulation_numbers):
        ### initializing models
        model_no_variance = model(bees_number, patches_number, "no_variance")
        model_high_variance = model(bees_number, patches_number, "high_variance")

        # for record each simulation's average
        record_high_variance = []
        record_no_variance = []

        for timestep in range(timesteps):
            # record the average
            if timestep > recording:
                record_high_variance.append(model_high_variance.arena.get_individual_learner()/33)
                record_no_variance.append(model_no_variance.arena.get_individual_learner()/33)

            ### ENVIRONMENT 1 (NO VARIANCE)
            model_no_variance.train(timestep)
            model_no_variance.update_parameters()
            
            ### ENVIRONMENT 2 (HIGH VARIANCE)
            model_high_variance.train(timestep)
            model_high_variance.arena.update_patches()
            model_high_variance.update_parameters()

        # record the total average of all simulations
        total_record_no_variance.append(np.average(record_no_variance))
        total_record_high_variance.append(np.average(record_high_variance))
    

    ave_no_bees = np.sum(total_record_no_variance)
    ave_high_bees = np.sum(total_record_high_variance)
    print("========================================================AVERAGE RESULT===========================================================")
    print("Timestep: ",timesteps)
    print("Number of simulation: ",simulation_numbers)
    print(" No  variance's average individual bee's PERCENTAGE: ",ave_no_bees*10,"%")
    print("High variance's average individual bee's PERCENTAGE: ",ave_high_bees*10,"%")
    print("=================================================================================================================================")

    '''------------------------------------------------
                        Plotting Result
    ------------------------------------------------'''
    ### Show the simulation result
    plots.plot_bar_compare(total_record_high_variance,total_record_no_variance)

    ### Show the plotting comparison
    plots.plot_grid(model_high_variance.patch_list, model_no_variance.patch_list,
                    model_high_variance.bee_list, model_no_variance.bee_list, 
                    model_high_variance.number_of_individual_bee, model_high_variance.number_of_social_bee,
                    model_no_variance.number_of_individual_bee, model_no_variance.number_of_social_bee)
    