#!/bin/python

import matplotlib.pylab as plt
import numpy as np
from matplotlib import pyplot
from matplotlib import rcParams
from pylab import *

#===================================

rc('axes', linewidth=4)
fullpage = {'axes.labelsize'  : 14,
            'axes.labelweight': 'normal',
            'axes.labelcolor' : 'black',
            'axes.linewidth'  : 2,
            'text.color'      : 'black',
            'font.size'       : 8,
            #            'text.usetex'     : True,
            'legend.fontsize' : 15,
            'lines.markersize': 8,
            'xtick.labelsize' : 10,
            'ytick.labelsize' : 10,
            'xtick.major.size': 5,
            'xtick.major.width': 2,
            'ytick.major.size': 5,
            'ytick.major.width': 2,
            'font.family'     : 'serif'
}

aps = {'backend'        : 'ps',
       'axes.labelsize' : 10,
       'text.fontsize'  : 10,
       'legend.fontsize': 10,
       'xtick.labelsize': 12,
       'ytick.labelsize': 12,
       'figure.figsize' : (3.4039, 2.1037),
       'axes'           : [0.125, 0.2, 0.95-0.125, 0.95-0.2]
}

plt.matplotlib.rcParams.update(fullpage)
hfont = {'fontname':'Helvetica'}

#===================================

def moving_avg(x):
    y = np.zeros(len(x))
    current_sum=0.0
    for i in range(len(x)):
        current_sum+= x[i]
        y[i] = current_sum/(i+1.0)
    return y

#===================================

data280=np.loadtxt('peo-nvtpgl-320k.kin')
ekHB_280 =data280[:,6]
ekHBc_280=moving_avg(ekHB_280)
t280=np.asarray(range(len(ekHB_280)))

#===================================

##== Plotting Convergence of <E_k> ==
fig, ax = plt.subplots(1,1)

ax.plot(t280,ekHB_280,'--b',lw=1.0, label='P=1.0 bar')
ax.hold(True)
ax.plot(t280,ekHBc_280,'-k',lw=2.0)
ax.hold(True)

#ax.set_ylabel('E_k [meV]',fontsize=18)
#ax.set_xlabel('time [ps]',fontsize=18)
#ax.set_ylim([0.00545, 0.00565])

setp(ax.get_xticklabels(), fontsize=18, weight='normal')
setp(ax.get_yticklabels(), fontsize=18, weight='normal')
setp(ax.yaxis.get_minorticklines(), 'markersize',      5)
setp(ax.yaxis.get_minorticklines(), 'markeredgewidth', 2)

plt.legend(loc='best')
plt.tight_layout()

################################################################################

# ##== Save Figure ==
# for i in ['eps','jpg']:
#     plt.savefig('PEO-Ek-conv.{0}'.format(i),dpi=600,format='{0}'.format(i))
#     #plt.savefig('inter_energy.{0}'.format(),dpi=600,format='{0}'.format(i))

    
plt.show()
