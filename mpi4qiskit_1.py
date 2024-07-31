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

digidict = {'0':['00', '11'], '1':['01', '10']}

with open("superenc_"+str(sys.argv[1])+".txt", 'r') as file:
    superenc = file.read()

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

print(fullenc, "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))

qc = QuantumCircuit(int(sys.argv[1]))
qc.h([j for j in range(int(sys.argv[1]))])
qc.barrier()
   
for j in range(int(sys.argv[1])):
    qc.p(Parameter('θ['+str(j)+']'), j)
qc.barrier()

try:
    qc.sdg([int(sys.argv[1])-j-1 for j in range(int(sys.argv[1])) if fullenc[j]=='1'])
except:
    pass
qc.barrier()

qc.h([j for j in range(int(sys.argv[1]))])
qc.measure_all()

parameters = list(qc.parameters)
params = np.load('params_'+str(sys.argv[1])+'.npy')
param_dict = {parameter: params[parameters.index(parameter)] for parameter in parameters}
qc = qc.assign_parameters(parameters = param_dict)

qc.draw(output='mpl', filename=str(sys.argv[1])+'/'+fullenc+'_circ.pdf')

shots = int(sys.argv[2])
sim = Aer.get_backend('aer_simulator')
qc_trans = transpile(qc, sim)
counts = sim.run(qc_trans, shots=shots).result().get_counts()

bitstrings = [format(j, '0'+str(sys.argv[1])+'b') for j in range(2**int(sys.argv[1]))]
probs = {}
for output in bitstrings:
    if output in counts:
        probs[output] = counts[output]/shots
    else:
        probs[output] = 0

plot_histogram(probs, title="processor {}, rank {:d} out of {:d} processors".format(procname, rank, size), filename=str(sys.argv[1])+'/'+fullenc+'_hist.pdf')
# print(probs, "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))

zyndex = fullenc.find('1')
if zyndex == -1:
    expecs = ['I'*(int(sys.argv[1])-j-1) + 'Z'*(j+1) for j in range(int(sys.argv[1]))]
else:
    expecs = ['I'*(zyndex-j) + 'Z'*(int(sys.argv[1])-zyndex+j) for j in range(zyndex+1)]
# print(expecs, "on processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))

l = 0
for expec in expecs:
    val = expectationVal(expec, probs)
    print(val, "pass "+str(l)+" expec for "+fullenc+'_'+expec+" with probs from processor {}, rank {:d} out of {:d} processors".format(procname, rank, size))
    with open(str(sys.argv[1])+'/'+fullenc+'_'+expec+".txt", 'w') as text_file:
        text_file.write(str(val))
    l = l + 1