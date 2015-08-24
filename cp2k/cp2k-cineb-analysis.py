#!/usr/bin/python

import numpy as np
import matplotlib.pylab as plt
import datetime
from scipy.interpolate import interp1d
now = datetime.datetime.now()
print "TIME :",now

found = True
x1=[]
energy=[]

file=open("CI-NEB.out","r")
list=file.readlines()
for i in range(len(list)-1,-1,-1):
    if("DISTANCE" in list[i] and found):
        data=list[i]
        distance=data.split()
        distance.pop(0)
        distance.pop(1)
        distance.pop(0)

        data1=list[i+1]
        distance1=data1.split()
        data2=list[i+2]
        distance2=data2.split()
        data3=list[i+3]
        distance3=data3.split()
        data4=list[i+4]
        distance4=data4.split()

        distance=distance+distance1+distance2+distance3+distance4

        dist = (map(float,distance)) # convert num strings to float
        print dist
        x=np.asarray(dist)*0.529177
        temp=0;
        for ii in x:
            temp = temp+ii
            x1.append(temp)
            
        x1.insert(0,0)
        found = False

file=open("CI-NEB.out","r")
found = True
list=file.readlines()
for i in range(len(list)-1,-1,-1):
    if("ENERGIES" in list[i] and found):
        data=list[i]
        energy=data.split()
        energy.pop(0)
        energy.pop(1)
        energy.pop(0)

        data1=list[i+1]
        energy1=data1.split()
        data2=list[i+2]
        energy2=data2.split()
        data3=list[i+3]
        energy3=data3.split()
        data4=list[i+4]
        energy4=data4.split()

        energy=energy+energy1+energy2+energy3+energy4
        energy = (map(float,energy)) # convert num strings to float
        print(energy)
        energy = 27.211*(energy-np.min(energy))
        found = False

# Plot Information
X = np.linspace(np.min(x1), np.max(x1), 50)
Y = interp1d(x1,energy, kind='cubic')

#fig = plt.figure()
ax = plt.gca()
#ax.set_yticks(np.arange(0,0.9,0.01)
print(energy)
plt.plot(x1,energy,'ko')
plt.hold(True)
plt.plot(X,Y(X),'-k')
ax.set_ylim([0,0.10])
#plt.yticks(np.arange(0, 0.1, 0.01))
plt.xlabel('Reaction Coordinate (A$^\circ$)')
plt.ylabel('Relative Energy (eV)')
#plt.grid()
plt.tight_layout()

# Save Figure in eps format
plt.savefig('mep-cp2k.eps')

