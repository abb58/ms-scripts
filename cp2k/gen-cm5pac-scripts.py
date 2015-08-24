#!/usr/bin/python
# Author - Abhishek Bagusetty
# University of Pittsburgh
# Prepare input files for CM5PAC partial charges by reading the 
# Hirshfeld charges. This requires CM5PAC software from 
# Don Truhlar group at University of Minnesota

import os
import os.path
found = True

mylist=["%.2d" % i for i in range(1,24)]
x=[]
for i in mylist:
    os.chdir("./replica_{0}".format(i))
    if( os.path.isfile('CM5_replica-{0}'.format(i)) ):
        os.remove('CM5_replica-{0}'.format(i))
    print os.getcwd()

    # Read the coordinates
    file=open('final-replica-{0}.xyz'.format(i),'r')
    file.readline()
    file.readline()
    list=file.readlines()
    file.close()

    file=open('CM5_replica-{0}'.format(i),'a')
    file.write('H++ System'+"\n")
    file.write('1.0'+"\n")
    file.write('        9.8559999999999999    0.0000000000000000    0.0000000000000000 '+"\n")
    file.write('       -3.6959999999999997    6.4016597847745800    0.0000000000000000'+"\n")
    file.write('        0.0000000000000000    0.0000000000000000   20.0000000000000000'+"\n")
    file.write('Cartesian'+"\n")

    # Put the position Coordinates
    for j in range(len(list)):
        data=list[j]
        if data.strip():   # Ignore any blank lines
            a,x,y,z=data.split()
            if(a=='C'):
                file.write('6  {0}  {1}  {2}'.format(x,y,z)+"\n")   
            elif(a=='O'):
                file.write('8  {0}  {1}  {2}'.format(x,y,z)+"\n")   
            else:
                file.write('1  {0}  {1}  {2}'.format(x,y,z)+"\n")   
                
    file.write('----'+"\n")
    
    ## Hershfeld Charge ##
    # Read and write the Hershfeld Population analysis from *.out file
    file1=open('SPEC-{0}.out'.format(i),'r')
    list1=file1.readlines()
    file1.close()
    for i in range(len(list1)):
        if("  #Atom  Element  Kind  Ref Charge     Population                     Net charge" in list1[i] and found):
            for k in range(1,55):
                data=list1[i+k]
                a,e,k,rchg,pop,hchg=data.split()
                file.write('{0}'.format(hchg)+"\n")

    file.close()
    os.chdir("/gscratch1/kjohnson/abb58/proton-cp2k/1by1by1/multiProton/NEB-1/cp2k/charge-dist/CM5PAC/")
    #print('...Executing...')
    #os.system('/gscratch1/kjohnson/abb58/proton-cp2k/chgdist/cm5pac ')


