#!/usr/bin/python

import matplotlib.pylab as plt
import numpy as np

def moving_avg(x):
    y = np.zeros(len(x))
    current_sum=0.0
    for i in range(len(x)):
        current_sum+= x[i]
        y[i] = current_sum/(i+1.0)
    return y

# Load the file
file=open('out.lammps','r')

f, axarr = plt.subplots(2, 2)

# Analyze and Collect the data columns


# Energy
plt.figure(1)
t_sample=data[10:,0]; U_sample=data[10:,4];  U_cavg=moving_avg(U_sample)
t1_sample=data1[10:,0]; U1_sample=data1[10:,2]; U1_cavg=moving_avg(U1_sample)
t2_sample=data2[10:,0]; U2_sample=data2[10:,2]; U2_cavg=moving_avg(U2_sample)
t3_sample=data3[10:,0]; U3_sample=data3[10:,2]; U3_cavg=moving_avg(U3_sample)
print(U_cavg)
print(U1_cavg)
plt.plot(t1_sample, U1_cavg, '-r', lw=2.0, label='0.05')
plt.plot(t2_sample, U2_cavg, '-g', lw=2.0, label='0.01')
plt.plot(t3_sample, U3_cavg, '-b', lw=2.0, label='0.5')
plt.plot(t_sample, U_cavg, '-k', lw=2.0, label='MD-NVT')
plt.legend(loc='best', fontsize=16)
plt.xlabel('Time', fontsize=16)
plt.ylabel('$\\langle U \\rangle$', fontsize=16)
plt.savefig('LJ-md-Ener.png',dpi=300)
plt.show()

# Pressure
plt.figure(2)
P_sample=data[10:,3]
P_cavg=moving_avg(P_sample)
P1_sample=data1[10:,1]
P1_cavg=moving_avg(P1_sample)
#print(P_cavg)
plt.plot(t1_sample, P1_cavg, '-r', lw=2.0, label='MC-NVT')
plt.hold(True)
plt.plot(t_sample, P_cavg, '-b', lw=2.0, label='MD-NVT')
plt.legend(loc='best', fontsize=16)
plt.title('LJ Argon Liquid Simulation (Pressure)', fontsize=18)
plt.xlabel('Moves',fontsize=16)
plt.ylabel('$\\langle P \\rangle$', fontsize=16)
plt.savefig('LJ-md-Pressure.png',dpi=300)
plt.show()
