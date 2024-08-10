import matplotlib.pyplot as plt
from mpi4py import MPI
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.circuit import Parameter
from qiskit.compiler import transpile
from qiskit.visualization import plot_histogram
import sys

I = np.eye(2)
Z = np.array([[1, 0], [0, -1]])

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

def expectationVal(expec, probs):
    if expec[0] == 'I':
        expecmat = I
    else:
        expecmat = Z
    for k in range(1, len(expec)):
        if expec[k] == 'I':
            expecmat = np.kron(expecmat, I)
        else:
            expecmat = np.kron(expecmat, Z)
    return np.dot(np.diag(expecmat), np.array([probs[key] for key in list(probs.keys())]))

def omega(num_qubits, power):
    return(power*2*np.pi/(2**num_qubits))

digidict = {'0':['00', '11'], '1':['01', '10']}

superenc = supeydupey(int(sys.argv[1]))

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
procname = MPI.Get_processor_name()

if int(rank) % 2 == 0:
    leadenc = format(int(rank/2), '0'+str(int(sys.argv[1])-2)+'b') # print(leadenc)
    fullenc = leadenc+digidict[superenc[int(rank/2)]][0]
else:
    leadenc = format(int((rank-1)/2), '0'+str(int(sys.argv[1])-2)+'b') # print(leadenc)
    fullenc = leadenc+digidict[superenc[int((rank-1)/2)]][1]

fullenc = fullenc + fullenc
# print(fullenc, "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))

qc = QuantumCircuit(2*int(sys.argv[1]))
qc.h([j for j in range(2*int(sys.argv[1]))])
qc.barrier()
   
for j in range(int(sys.argv[1])):
    qc.p(Parameter('α['+str(j)+']'), j)
    qc.p(Parameter('β['+str(j)+']'), int(sys.argv[1])+j)
qc.barrier()

try:
    qc.sdg([int(sys.argv[1])-j-1 for j in range(2*int(sys.argv[1])) if fullenc[j]=='1'])
except:
    pass
qc.barrier()

qc.h([j for j in range(2*int(sys.argv[1]))])
qc.measure_all()

parameters = list(qc.parameters)
params_1 = np.array([omega(int(sys.argv[1]), int(sys.argv[3])*(2**j)) for j in range(int(sys.argv[1]))]) # 0
params_2 = np.array([omega(int(sys.argv[1]), int(sys.argv[4])*(2**j)) for j in range(int(sys.argv[1]))]) # 0
params = np.hstack((params_1, params_2))
param_dict = {parameter: params[parameters.index(parameter)] for parameter in parameters}
bound_qc = qc.assign_parameters(parameters = param_dict)

qc.draw(output='mpl', filename=str(sys.argv[1])+'/'+fullenc+'_circ.pdf')

shots = int(sys.argv[2])
sim = Aer.get_backend('aer_simulator')
qc_trans = transpile(bound_qc, sim)
counts = sim.run(qc_trans, shots=shots).result().get_counts()
# print(counts)

bitstrings = [format(j, '0'+str(2*int(sys.argv[1]))+'b') for j in range(2**(2*int(sys.argv[1])))]
print(bitstrings)
probs = {}
for output in bitstrings:
    if output in counts:
        probs[output] = counts[output]/shots
    else:
        probs[output] = 0

plot_histogram(probs, title="processor {}, rank {:d} out of {:d} processors".format(procname, rank, size), filename=str(sys.argv[1])+'/'+fullenc+'_hist.pdf')
# print(probs, "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))

zyndex = fullenc[:int(sys.argv[1])].find('1')
if zyndex == -1:
    expecs = ['I'*(int(sys.argv[1])-j-1) + 'Z'*(j+1) for j in range(int(sys.argv[1]))]
else:
    expecs = ['I'*(zyndex-j) + 'Z'*(int(sys.argv[1])-zyndex+j) for j in range(zyndex+1)]
# print(expecs, "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))

R_vals = []
L_vals = []
for expec in expecs:
    R_vals.append(expectationVal(expec.rjust(2*int(sys.argv[1]), 'I'), probs))
    L_vals.append(expectationVal(expec.ljust(2*int(sys.argv[1]), 'I'), probs))
# print(vals)

plt.clf()
plt.bar([expec.rjust(2*int(sys.argv[1]), 'I') for expec in expecs], R_vals)
plt.title("processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))
plt.savefig(str(sys.argv[1])+'/'+fullenc+'_R_expecs_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.pdf')

plt.clf()
plt.bar([expec.ljust(2*int(sys.argv[1]), 'I') for expec in expecs], L_vals)
plt.title("processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))
plt.savefig(str(sys.argv[1])+'/'+fullenc+'_L_expecs_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.pdf')

R_weights = list(np.load('weights_'+str(sys.argv[1])+'.npy', allow_pickle=True)[0]['R'][fullenc].values())
L_weights = list(np.load('weights_'+str(sys.argv[1])+'.npy', allow_pickle=True)[0]['L'][fullenc].values())

# print(np.array([np.dot(R_weights, R_vals)+np.dot(L_weights, L_vals)]), "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))
np.save(str(sys.argv[1])+'/weights_'+str(rank)+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.npy', np.array([np.dot(R_weights, R_vals)+np.dot(L_weights, L_vals)]))