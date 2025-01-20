import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

#calculates the mean measurment for each finger for every  milisecond
#returns a 1201X5 matrix of the time serie for each finger's brain signal
def calc_mean_erp(trial_points_path, ecog_data_path):
    #load files
    trial_points = pd.read_csv(trial_points_path) #finger ID + start and peak point of activity
    ecog_data = pd.read_csv(ecog_data_path) #single point brain signal measurment

    #converting "trial_points" into int variables
    trial_points = trial_points.astype({'start_point': 'int', 'peak_point': 'int', 'finger': 'int'})

    #constructing the 5 X 1201 matrix with a matrix of zeroes
    fingers_erp_mean = np.zeros((5, 1201))

    #defining plot colors
    colors = ['#007847', '#000000', '#FFD700', '#D50032', '#808080']

    #plotting the graph
    plt.figure(figsize=(10, 6))
    for finger in range(1, 6):
        #filterring and creating a graph for each finger
        finger_trials = trial_points[trial_points['finger'] == finger]

        #collecting each finger's data
        finger_data = []
        for _, trial in finger_trials.iterrows():
            start_index = trial['start_point'] - 200 
            end_index = trial['start_point'] + 1000 
            #extracting and matching the single brain signal measurment to the finger activity info
            trial_data = ecog_data.iloc[start_index:end_index+1].values.flatten()
            finger_data.append(trial_data)
        
        #calculate the mean of each milisecond for the specific finger (in a loop so each time for another finger)
        fingers_erp_mean[finger-1] = np.mean(finger_data, axis=0)
        
        #show the plot
        plt.plot(fingers_erp_mean[finger-1], label=f'Finger {finger}', color=colors[finger-1])
    
    #plot settings
    plt.title('avrg erp for each of the 5 Fingers')
    plt.xlabel('time (milisecond)')
    plt.ylabel('brain signal amplitude')
    plt.legend()
    plt.tight_layout()
    plt.show()

    #making the df from the mean that was calculated for each finger
    fingers_erp_df = pd.DataFrame(fingers_erp_mean.T, columns=[f'Finger {i+1}' for i in range(5)])
    print(fingers_erp_df)
    return fingers_erp_mean

#setting files path
data_directory = r"C:\python advenced\miniproject2"

#calling the functions
fingers_erp_mean = calc_mean_erp(
    os.path.join(data_directory, 'trial_points.csv'), 
    os.path.join(data_directory, 'ecog_data.csv')
)
