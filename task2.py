from tabnanny import check
import numpy as np
from qiskit import QuantumCircuit, execute, Aer, assemble
from qiskit.visualization import plot_histogram
import qiskit.quantum_info as qi

missing_list = [1, 0, 3]


encoding_list = np.zeros(len(missing_list) + 1)
n = int(np.log2(len(missing_list) + 1))
for i in missing_list:
    encoding_list[i] = 1/np.sqrt(len(missing_list))
qc = QuantumCircuit(3*n + 1)
qc.initialize(encoding_list, list(n+ np.arange(n)))
qc.h(range(n))
#qc.h(n + np.array(range(n)))
print(qc)

checking_oracle = QuantumCircuit(3*n+1)
#checking_oracle.h(range(2*n))
checking_oracle.x(3*n)
checking_oracle.h(3*n)
# checking_oracle.x(3*n)
# checking_oracle.x(n)
# checking_oracle.x([0,1])
for i in range(n):
    checking_oracle.cnot([i, i+n], 2*n + i)
check_bits = [(2*n + i) for i in range(n)]
checking_oracle.mcx(check_bits, 3*n, mode = "noancilla")
# checking_oracle.z(3*n)
# checking_oracle.mcx(check_bits, 3*n, mode = "noancilla")
for i in range(n):
    checking_oracle.cnot([n-1-i+n, n-1-i], 2*n + n-1-i)

checking_oracle.h(3*n)
checking_oracle.x(3*n)
# print(checking_oracle)

oracle = checking_oracle.to_gate()
oracle.name = "Oracle"

#Changing the simulator 
# backend = Aer.get_backend('unitary_simulator')

#job execution and getting the result as an object
# job = execute(checking_oracle, backend)
# result = job.result()
op = qi.Operator(checking_oracle)
#get the unitary matrix from the result object
# print(result.get_unitary(checking_oracle, decimals=3))

diffuser = QuantumCircuit(n + 1)
diffuser.h(range(n))
diffuser.x(range(n))
diffuser.h(n)
diffuser.mcx(list(range(n)), n)
diffuser.h(n)
diffuser.x(range(n))
diffuser.h(range(n))
diff = diffuser.to_gate()
diff.name = "diffuser"
# print(diffuser)

qc.append(oracle)