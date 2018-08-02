# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 16:05:47 2018

@author: Duncan C-S
"""

# The following code uses MessagesFile as a training set to determine the
# probabilty that a user will want to have a phone on silent or not on silent.

# This is accomplished twice, the first time stores data on each text that is
# received and sent, Bayes theorm is then used to derive the probability of the
# user wanting to receive the next text from that person.

# Seccond, the same insights are attempted to be drawn however data from each
# text is NOT recorded. Instead a probability value is updated with each iteration

# The rational: A need to develop 'smart' software using ML without needing to
# send private data to a cloud server. Instead instance based learning may be
# employed as a way to have offline ML on any device. without a need for storing
# large amounts of private data.

### Storing data, using Bayes theorum

Contacts = pd.DataFrame(data = {'Names': Names})
# App starts here:

Contacts['Returns'] = np.zeros(len(Contacts.Names))
# Returns is the total value of texts replied to per contact
Contacts['Total'] = np.zeros(len(Contacts.Names))
# Total is the number of texts received per contact
Contacts['Bayes Probability']= np.zeros(len(Contacts.Names))
# Bayes Probability uses the data stored on each contact (ie. Returns and total)
# and uses these values to calculate the probability of wanting to respond to that person.

Contacts['Likelihood'] = np.zeros(len(Contacts.Names))
# Likelihood is the is the percentage of texts responded to by each contact.
Contacts['Evidence'] = np.zeros(len(Contacts.Names))
# Evidence is the confidence in the likelihood value
Contacts['Last'] = np.zeros(len(Contacts.Names))
# Last stores the number of the last text received from that person
Contacts['Modified Bayes Probabiliy'] = np.zeros(len(Contacts.Names))
# "Modified Bayes Probability" is the probability of a text being returned.
# It is calculated using "likelihood" and "Evidence" neither of which collect
# absolute data.

Cut_off = pd.Timedelta(minutes = 60)
TotalSent = 0
Prior = 1

# Collecting Data
def Increase_TotalSent(TotalSent):
    TotalSent = TotalSent+1
    return TotalSent

def Increase_Returns(name):
    Returns = Contacts.loc[Contacts['Names'] == name, 'Returns']
    Returns = Returns + 1
    Contacts.loc[Contacts['Names'] == name, 'Returns'] = Returns

def Increase_TotalReceived(name):
    Total = Contacts.loc[Contacts['Names'] == name, 'Total']
    Total = Total + 1
    Contacts.loc[Contacts['Names'] == name, 'Total'] = Total
    
# Not directly collecting data, just tracking probability
def Increase_Prior(Prior, n):
    Prior = (Prior*n+1)/(n+1)
    return Prior
    
def Increase_Likelihood(name, n, Prior):   
    Last = Contacts.loc[Contacts['Names'] == name, 'Last']
    S = n*Prior
    Likelihood = Contacts.loc[Contacts['Names'] == name, 'Likelihood']
    Likelihood = (Likelihood*Last + 1)/S
    Contacts.loc[Contacts['Names'] == name, 'Likelihood'] = Likelihood

def Increase_Evidence(name, n):
    Evidence = Contacts.loc[Contacts['Names'] == name, 'Evidence']
    Last = Contacts.loc[Contacts['Names'] == name, 'Last']
    Evidence = (Evidence*Last + 1)/(n+1)
    Contacts.loc[Contacts['Names'] == name, 'Evidence'] = Evidence
    
def Update_last(name, count):
    Contacts.loc[Contacts['Names'] == name, 'Last'] = count

# Iterate through all past messages to quantify trends
count = 0
for i in range(0,len(MessagesFile)-1):    
    if MessagesFile.loc[i, 'Received'] == True:
        count = count + 1

        N = MessagesFile.loc[i, 'Name']

        time_delay = MessagesFile.loc[i+1, 'Time'] - MessagesFile.loc[i, 'Time']
        if MessagesFile.loc[i+1,'Received'] == False and time_delay < Cut_off:
            response = True

            TotalSent = Increase_TotalSent(TotalSent)
            Increase_Returns(N)
            Increase_TotalReceived(N)

            Prior = Increase_Prior(Prior, count)
            Increase_Likelihood(N, count, Prior)
            Increase_Evidence(N, count)
            Update_last(N, count)
            
        else:
            response = False
            Update_last(N, count)
            Increase_TotalReceived(N)
            Increase_Evidence(N, count)

    else:
        received = False

# Use information from past texts to predict future probability
for Name in Names:
    Returns = Contacts.loc[Contacts['Names'] == Name, 'Returns']
    Total = Contacts.loc[Contacts['Names'] == Name, 'Total']
    Likelihood = Contacts.loc[Contacts['Names'] == Name, 'Likelihood']
    Evidence = Contacts.loc[Contacts['Names'] == Name, 'Evidence']

    Contacts.loc[Contacts['Names'] == Name, "Bayes Probability"]\
    = (Returns * TotalSent)/ (Total * Total)

    Contacts.loc[Contacts['Names'] == Name, "Modified Bayes Probabiliy"]\
    = (Likelihood * Prior)/ Evidence

print(Contacts)
# The above code attempts to demonstrate a new method of using bayes statistics
# to determine posterior probability, without the need for storing personal 
# information


def Incoming_Text(Name):
    Posterior = Contacts.loc[Contacts['Names'] == Name, 'Modified Bayes Probabiliy']
    if  0.5 < float(Posterior):
        print("Message received from "+ Name +", ringer is on")
    else:
        print('Message received from '+ Name + ', ringer is off')