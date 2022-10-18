import numpy as np
from qiskit import QuantumCircuit, execute, Aer, assemble, transpile
from qiskit.visualization import plot_histogram
import qiskit.quantum_info as qi

missing_list = [1, 2, 3]


encoding_list = np.zeros(len(missing_list) + 1)
n = int(np.log2(len(missing_list) + 1))
for i in missing_list:
    encoding_list[i] = 1/np.sqrt(len(missing_list))
qc = QuantumCircuit(3*n + 1, n)
qc.initialize(encoding_list, list(n+ np.arange(n)))
qc.h(range(n))


checking_oracle = QuantumCircuit(3*n+1)
check_bits = [(2*n + i) for i in range(n)]

for i in range(n):
    checking_oracle.cnot([i, i+n], 2*n + i)

checking_oracle.x(check_bits)
checking_oracle.mcx(check_bits, 3*n, mode = "noancilla")
checking_oracle.z(3*n)
checking_oracle.mcx(check_bits, 3*n, mode = "noancilla")
checking_oracle.x(check_bits)

for i in range(n):
    checking_oracle.cnot([n-1-i+n, n-1-i], 2*n + n-1-i)

print(checking_oracle)

oracle = checking_oracle.to_gate()
oracle.name = "Oracle"


diffuser = QuantumCircuit(n)
diffuser.h(range(n))
diffuser.x(range(n))
diffuser.h(0)
diffuser.mcx(list(range(1,n)), 0)
diffuser.h(0)
diffuser.x(range(n))
diffuser.h(range(n))
diff = diffuser.to_gate()
diff.name = "Diffuser"
# print(diffuser)

for i in range(int(np.pi*np.sqrt(len(missing_list) + 1)/4)):
    qc.append(oracle, range(3*n + 1))
    qc.append(diff, range(n))
 


qc.measure(range(n), range(n))

# print(qc.decompose())

aer_sim = Aer.get_backend('aer_simulator')
transpiled_grover_circuit = transpile(qc, aer_sim)
qobj = assemble(transpiled_grover_circuit)
results = aer_sim.run(qobj).result()
counts = results.get_counts()
print(counts)
