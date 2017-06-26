'''
Created on 14 juin 2017

@author: irac1
'''

import matplotlib.pyplot as plt



def factorielle (n):
    if (n==1):
        return 1
    else:
        return n*factorielle(n-1);
    
def product (n,m):
    result=1
    for i in range (n,m):
        result=result*i
    return result
    

def birthdayOnSameDay(n):
    result = 1
    for i in range (365-n+1,365):
        result*=i/365
    return 1-result


birthdayProb=[]
birthdayProb.append(0)

for i in range (1,70):
    birthdayProb.append(birthdayOnSameDay(i))
    
plt.plot(birthdayProb, 'r+', drawstyle='steps')
plt.axis([1,70,0,1])
plt.yticks([0,0.25,0.5,0.75,1])
plt.grid(True)
plt.show()