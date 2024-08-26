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
    
digidict = {'0':['00', '11'], '1':['01', '10']}

def encs(num_qubits):
    fullencs = []
    superenc = supeydupey(num_qubits)
    for i in range(len(superenc)):
        leadenc = format(int(i), '0'+str(num_qubits-2)+'b')
        for j in range(2):
            fullencs.append(leadenc+digidict[superenc[int(i)]][j])
    return(fullencs)

def XYconv(stwing):
    convertedXY = ''
    for letter in stwing:
        if letter == '1':
            convertedXY = convertedXY + 'Y'
        else:
            convertedXY = convertedXY + 'X'
    return convertedXY

def weighty_dict(num_qubits):
    if num_qubits == 2:
        return {'00':{'IX':-1, 'XX':-1}}
    else:
        wd40 = {}
        for key_i in list(weighty_dict(num_qubits-1).keys()):
            wd400 = {}
            for key_j in list(weighty_dict(num_qubits-1)[key_i].keys())[:-1]:
                wd400['I'+key_j] = weighty_dict(num_qubits-1)[key_i][key_j]
            key_j = list(weighty_dict(num_qubits-1)[key_i].keys())[-1]
            wd400['I'+key_j] = weighty_dict(num_qubits-1)[key_i][key_j]/2
            wd400['X'+key_j] = weighty_dict(num_qubits-1)[key_i][key_j]/2
            wd40['0'+key_i] = wd400
        for fullenc in encs(num_qubits):
            if fullenc not in list(wd40.keys()):
                if fullenc.count('1') % 4 == 0:
                    wd40[fullenc] = {'I'+XYconv(fullenc[1:]):2**(2-num_qubits), 'X'+XYconv(fullenc[1:]):-(2**(2-num_qubits))}
                else:
                    wd40[fullenc] = {'I'+XYconv(fullenc[1:]):-(2**(2-num_qubits)), 'X'+XYconv(fullenc[1:]):2**(2-num_qubits)}
        return(wd40)
        
np.save('weights_'+str(sys.argv[1])+'.npy', np.array([weighty_dict(int(sys.argv[1]))]))