import numpy as np
import pickle
from qiskit import Aer, execute, QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.compiler import transpile
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_histogram
import sys

def createQC(gate_string, params):
  num_qubits = 2
  qc = QuantumCircuit(num_qubits)

  parameter_0 = Parameter('θ[0]')
  parameter_1 = Parameter('θ[1]')
  parameter_2 = Parameter('θ[2]')

  qc.rx(theta = parameter_0, qubit = 0)
  qc.ry(theta = parameter_1, qubit = 0)
  qc.ry(theta = parameter_2, qubit = 1)
  
  parameters = list(qc.parameters)
  qc.barrier()

  for i in range(num_qubits):
    if gate_string[i] == 'I':
      pass
    if gate_string[i] == 'H':
      qc.h(num_qubits-i-1)
  qc.measure_all()

  param_dict = {parameter: params[parameters.index(parameter)] for parameter in parameters}
  qc = qc.assign_parameters(parameters = param_dict)
  return qc

if int(sys.argv[2]) == 0:
  qc = createQC(str(sys.argv[1]), [0, 4*np.pi*int(sys.argv[3])/8, 4*np.pi*int(sys.argv[4])/8])
if int(sys.argv[3]) == 0:
  qc = createQC(str(sys.argv[1]), [4*np.pi*int(sys.argv[2])/8, 0, 4*np.pi*int(sys.argv[4])/8])

# qc.draw('mpl', style='clifford')

bitstrings = ['00', '01', '10', '11']

shots = 100000
sim = Aer.get_backend('aer_simulator')
qc_trans = transpile(qc, sim)
counts = sim.run(qc_trans, shots=shots).result().get_counts()

probs = {}
for output in bitstrings:
    if output in counts:
        probs[output] = counts[output]/shots
    else:
        probs[output] = 0
      
with open(str(sys.argv[1])+'_'+str(sys.argv[2])+'_'+str(sys.argv[3])+'_'+str(sys.argv[4])+'.pkl', 'wb') as fp:
    pickle.dump(probs, fp)
    print('dictionary saved successfully to file')
