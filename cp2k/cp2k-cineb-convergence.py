#!/usr/bin/python

import numpy as np
import matplotlib.pylab as plt
import datetime
import sys
from scipy.interpolate import interp1d
now = datetime.datetime.now()
print('TIME : {0}'.format(now))

#x1=[]
energy=[]

# Open the file and read it
filename=sys.argv[1]
file=open(filename,'r')
list=file.readlines()

# ------------ COLLECT RSD ------------#

# ------------ COLLECT ENERGY ------------#
stop=0
start=0
for i in range(len(list)-1,-1,-1):
    if 'BAND TOTAL ENERGY' in list[i]:
        print(list[i])
        stop = i
    if 'ENERGIES' in list[i]:
        print(list[i])
        start = i
        break

count = 0
n_ener = 0
for i in range(start, stop):
    count=count+1
    data=list[i]
    fields=data.split()

    if count==1:  # Energies line
        for i in range(3,7):
            n_ener = n_ener + 1
            energy.append(float(fields[i]))
    else: # for rest of the lines
        for i in range(len(fields)):
            n_ener = n_ener + 1
            energy.append(float(fields[i]))

energy = np.asarray(energy)
print('Energies for each image [a.u.] : {0}'.format(energy))
energy = 27.2114 * (energy - energy[0])
print('Energies for each image [eV] : {0}'.format(energy))


x1=range(n_ener)
x1=np.asarray(x1)

# ---- Plot Information -----
X = np.linspace(np.min(x1), np.max(x1), 50)
Y = interp1d(x1,energy, kind='cubic')

#fig = plt.figure()
ax = plt.gca()
#ax.set_yticks(np.arange(0,0.9,0.01)
print(energy)
plt.plot(x1,energy,'ko')
plt.hold(True)
plt.plot(X,Y(X),'-k', lw=2.0)
#ax.set_ylim([0,0.10])
#plt.yticks(np.arange(0, 0.1, 0.01))
plt.xlabel('Reaction Coordinate (A$^\circ$)')
plt.ylabel('Energy (eV)')
#plt.grid()
plt.tight_layout()
plt.show()
# Save Figure in eps format
plt.savefig('mep-cp2k-{0}.eps'.format(now))

