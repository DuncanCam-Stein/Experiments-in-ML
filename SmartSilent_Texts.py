# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 15:34:47 2018

@author: Duncan C-S
"""

# This code will create a fictional list of text messages to be used as a sample
# data set for SmartSilent

import pandas as pd
import scipy as sp
import numpy as np
import matplotlib.pylab as plt
import seaborn
import string

# Defining the list of contacts
Names = ['Friend', 'Family', 'Colleague', 'Aquaintance']
MessagesFile = pd.DataFrame( columns = ['Name','Time','Received'])

# Creating 1000 incoming texts

T = pd.Timestamp(2018,1,1)
j = -1
for i in range(1000):
    j = j + 1
    # A text is received from a random person
    N = Names[np.random.randint(0,4)] 
    MessagesFile.loc[j, 'Name'] = N 
    MessagesFile.loc[j, 'Time'] = T 
    MessagesFile.loc[j, 'Received'] = True # Wether the text is incoming or outgoing
    
    # A random response time is chosen on the interval of 0 and 2 hours.
    Delta = pd.Timedelta(hours=np.random.randint(0,2), minutes = np.random.randint(0,60))
    
    j = j + 1
    # For each contact there a probability for a response.
    # In addition, 'Friend' has a 30 minute shorter response time, and aquaintance
    # has a 30 minute longer response time
    if N == 'Friend' and np.random.random_sample() > 0.25:
        Delta = Delta - pd.Timedelta(minutes = 30)
        T = T + Delta 
        MessagesFile.loc[j] = ('Friend', T, False)
        
    elif N == 'Family' and np.random.random_sample() > 0.25:
        T = T + Delta
        MessagesFile.loc[j] = ('Family', T, False)

    elif N == 'Colleague' and np.random.random_sample() > 0.5:
        T = T + Delta
        MessagesFile.loc[j] = ('Colleague', T, False)

    elif N == 'Aquaintance' and np.random.random_sample() > 0.75:
        Delta = Delta + pd.Timedelta(minutes = 30)
        T = T + Delta 
        MessagesFile.loc[j] = ('Aquaintance', T, False)
    else:
        T = T + Delta
        j = j - 1
        
# The messages data set is finished being constructed
        
# The following Code is used for making the plots and the only purpose is to be
# facilitate visualizing the data in MessagesFile

# If a message is responded to in 60 minutes, then the message response status
# is True
Cut_off = pd.Timedelta(minutes = 60)

# This dataFrame is used solely for plotting
NamesPlot = ['Friend','FriendTotal','Family','FamilyTotal','Colleague','ColleagueTotal','Aquaintance','AquaintanceTotal']
Plot = pd.DataFrame(data = np.zeros((1,len(NamesPlot))), columns = NamesPlot)
j = 0

# Searches through each message, if the condition that a response happened is 
# True, then the total responses for that name is updated.
for i in range(1,len(MessagesFile)-1):    
    if MessagesFile.loc[i, 'Received'] == True:
        j = j + 1

        N = MessagesFile.loc[i, 'Name']
        Plot.loc[j] = Plot.loc[j-1]
        time_delay = MessagesFile.loc[i+1, 'Time'] - MessagesFile.loc[i, 'Time']
        if MessagesFile.loc[i+1,'Received'] == False and time_delay < Cut_off:
            response = True
            Plot.loc[j, N] = Plot.loc[j, N] + 1
            Plot.loc[j, N + 'Total'] = Plot.loc[j, N + 'Total'] + 1
            
        else:
            response = False
            Plot.loc[j, N + 'Total'] = Plot.loc[j, N + 'Total'] + 1
            
    else:
        received = False

plt.plot(Plot[Names])
plt.legend(Names)
plt.title("Positive responses by person for increasing texts received")
plt.ylabel("Responses")
plt.xlabel("texts received")

plt.figure()

PlotData = Plot.loc[998]
plt.bar(Names,PlotData[['FriendTotal','FamilyTotal','ColleagueTotal','AquaintanceTotal']], label = 'Total Texts')
plt.bar(Names,PlotData[Names], color = 'g', label = 'Responded texts')
plt.legend()
plt.ylabel("texts")
plt.title("Texts with responses vs total texts")

