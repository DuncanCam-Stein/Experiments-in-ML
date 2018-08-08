## Experiments-in-ML
My first trials in applying ML

# SmartSilent - A machine learning algorithm to predict behavior.
## Author: Duncan Cameron-Steinke

### Problem: People want a personalised user experience, but don't want their data being tracked.
### Solution: Develop ML software that does not require intrusive data storage.

* Open SmartSilentJupyter.ipynb to view the rendered code.

#### What the program does:

The following code creates a personalised user experience by calculating the probability that a text will be responded to. Based on probability it could chose whether or not the phone should be on silent.

This is accomplished twice, the first time stores data on each text that is received and sent, Bayes theorm is then used to derive the probability of the user wanting to receive the next text from that person.

Seccond, the same insights are attempted to be drawn however data from each text is NOT recorded. Instead a probability value is updated with each iteration

Updated: Aug 7th 2018
