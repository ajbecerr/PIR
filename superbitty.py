import numpy as np
import sys

def bittynot(stwing):
    notstwing = ''
    for i in range(len(stwing)):
        notstwing = notstwing+str((int(stwing[i])+1)%2)
    return(notstwing)

def supeydupey(num_qubits):
    if num_qubits == 3:
        superenc = '0'
    else:
        superenc = supeydupey(num_qubits-1) + bittynot(supeydupey(num_qubits-1))
    return(superenc)

phase_params = np.array([0 for j in range(int(sys.argv[1]))])
# phase_params[-1] = np.pi
# phase_params[-2] = np.pi/2
# phase_params[-3] = np.pi/4

np.save('params_'+str(sys.argv[1])+'.npy', phase_params)

with open("superenc_"+str(sys.argv[1])+".txt", 'w') as text_file:
    text_file.write(supeydupey(int(sys.argv[1])))