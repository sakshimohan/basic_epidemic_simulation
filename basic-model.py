import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D # for manually adding legends

def epi_simulation(simdays, r, h, d_h, h_stay, H_max, max_I_prop, total_pop, infection_prop_init):
    n = simdays
    H_max = beds_per1000 * 1000
    
    I = np.empty(n) # number of newly infected
    cum_I = np.empty(n) # cumulative number infected
    
    H_need = np.empty(n) # number of additional people requiring hospitalisation on a given day
    cum_H_need = np.empty(n) # total number of people requiring hospitalisation on a given day
    H_actual = np.empty(n) # number of people hospitalised given capacity
    cum_H_actual = np.empty(n) # total number of people requiring hospitalisation on a given day


    D = np.empty(n) # number dead

    I[0] = infection_prop_init * total_pop
    cum_I[0] = I[0]
    H_need[0] = I_0 * h 
    cum_H_need[0] = H_need[0]
    H_actual[0] = min(H_max, cum_H_need[0])
    cum_H_actual[0] = H_actual[0]

    D[0] =  0

    r = r # infection multiplication rate

    # Calculate total number of infected people on each day
    for i in range(n-1):
        I[i+1] = I[i]*(1+r)
        cum_I[i+1] = sum(I[0:i+1])
        H_need[i+1] = I[i+1] * h
        

    # Each additional case which needs hospitalization on a given day needs hopitalisation for the period of recovery
    # Calculate the total number of people requiring hospitalisation each day
    for i in range(n-1):
        if i+1-h_stay < 0:
            if H_max < cum_H_need[i]: #some people did not recive hospitalisation and died
                cum_H_need[i+1] = sum(H_need[0:i+2]) - (cum_H_need[i]- H_max)
            else:
                cum_H_need[i+1] = sum(H_need[0:i+2])
        else:
            if H_max < cum_H_need[i]: #some people did not recive hospitalisation and died
                cum_H_need[i+1] = sum(H_need[i+1-h_stay+1:i+2]) - (cum_H_need[i]- H_max)
            else:
                cum_H_need[i+1] = sum(H_need[i+1-h_stay+1:i+2])

    # Calculate the total number of people in hospital on a given day
    for i in range(n-1):
        cum_H_actual[i+1] = min(H_max, cum_H_need[i+1]) # total number of people hospitalised
        if i+1-h_stay < 0:
            H_actual[i+1] = cum_H_actual[i+1] - cum_H_actual[i]
        else:    
            H_actual[i+1] = cum_H_actual[i+1] - cum_H_actual[i] + H_actual[i+1-h_stay] # additional new people admitted

    # Calculate the number of additional people dying each day
    for i in range(n-1):
        # Anyone who doesn't get hospitalised on the day he/she needs hospitalisation dies
        # x% of hospitalised cases admitted h_stay days ago die 
        if i+1-h_stay < 0:
            if H_need[i+1] > H_actual[i+1]:
                D[i+1] =  (H_need[i+1] - H_actual[i+1])
            else:
                D[i+1] = 0
        else:
            D[i+1] =  (H_need[i+1] - H_actual[i+1]) + d_h * H_actual[i+2-h_stay]
    
    df = pd.DataFrame(columns=['New daily infections', 'New daily cases hospitalised', 'Daily deaths'])
    df['New daily infections'] = np.around(I, decimals = 0)
    df['New daily cases hospitalised'] = np.around(H_actual, decimals = 0)
    df['Daily deaths'] = np.around(D, decimals = 0)
    
    # Print assumptions:
    print("Assumptions:")
    print(".......")
    print("Total population = ",total_pop)
    print("Proportion of population infected on day 0 of simulation = ", infection_prop_init)
    print("Number of days of simulation = ",simdays)
    print("Daily rate of increase of infections = ",r)
    print("Proportion of newly infected cases needing hospitalisation = ",h)
    print("Proportion of hospitalised patients who die = ",d_h, "(Note we assume that all patients needing hospitalisation who don't receive it die on the day on infection)")
    print("Length of hospital stay (days) = ",5)
    print("Bed capacity per 1000 people = ",beds_per1000)
    
    # Print outputs
    print("Ouputs:")
    print(".......")
    print("# infected on day 0 = ", round(I[0]))
    print("Hospital bed capacity = ", round(H_max,0))
    print("Maximum hospital bed demand on any day = ", round(cum_H_need.max(),0))
    print("Total infected = ", round(I.sum(),0))
    print("Total hospitalised = ", round(H_actual.sum(),0))
    print("Total deaths = ", round(D.sum(),0))
    #print(df)
    
    # Create a figure instance
    fig = plt.figure(figsize = (22,22))
    xlabel = "Day of simulation"
    ylabel = "Number of cases"
    # Create legend labels common across graphs
    colors1 = ['black']
    lines1 = [Line2D([0], [0], color=c, linewidth=3, linestyle='-') for c in colors1]
    labels1 = ['Infections']
    colors2 = ['blue', 'red']
    lines2 = [Line2D([0], [0], color=c, linewidth=3, linestyle='-') for c in colors2]
    labels2 = ['Hospital admissions','Deaths']
    
    plt.subplot(421)
    plt.plot('New daily infections', data=df, marker='',color='black', linewidth=1)
    plt.ylabel(ylabel, fontsize=17)
    plt.xlabel(xlabel, fontsize=17)
    plt.title('Daily infections', fontsize=17,weight="bold")
    plt.legend(lines1,labels1,fontsize=14)
    
    plt.subplot(422)
    plt.plot('New daily cases hospitalised', data=df, marker='',color='blue', linewidth=1)
    plt.plot('Daily deaths', data=df, marker='',color='red', linewidth=1)
    plt.ylabel(ylabel, fontsize=17)
    plt.xlabel(xlabel, fontsize=17)
    plt.title('Daily hospital admissions/deaths', fontsize=17,weight="bold")
    plt.legend(lines2,labels2,fontsize=14)
