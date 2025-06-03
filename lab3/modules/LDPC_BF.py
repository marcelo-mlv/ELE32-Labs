import numpy as np
import random
import os
import csv  

class LDPC_BF:

    def __init__(self, N, dv, dc, init_random=True):
        
        M = int((N * dv) / dc)
        self.N = N
        self.M = M

        self.table = np.zeros((M, N))
        # table[m][n] = edge(m,n), m = c-node (M), n = v-node (N) 
        # table[m][n] = (0 [false] or 1 [true])
        
        # randomly generated connections
        if init_random:
            vnodes_num_conections = np.zeros(N)
            for m in range(M):
                chooseable_vnodes = [node for node in range(N) if vnodes_num_conections[node] == min(vnodes_num_conections)]
                chosen_vnodes = sorted(random.sample(chooseable_vnodes, dc))
                for n in chosen_vnodes:
                    self.table[m][n] = 1
                    vnodes_num_conections[n] += 1

        self.vnodes_fails = np.zeros(N, dtype=int)

    @classmethod
    def from_csv(cls, filename, dv, dc):
        path = os.path.join("output", filename)
        connections = []

        with open(path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                connections.append([int(x) - 1 for x in row])  # converte para índice 0-based

        N = len(connections)
        M = max((max(cnodes) if cnodes else -1) for cnodes in connections) + 1

        # Inicializa sem rodar o random do __init__
        obj = cls(dv, dc, N=N, init_random=False)
        obj.M = M
        obj.table = np.zeros((M, N, 2))

        for v_node, c_nodes in enumerate(connections):
            for c_node in c_nodes:
                obj.table[c_node][v_node] = 1

        return obj

    def check_node(self, m, input_bits):
        result = np.dot(self.table[m].T, input_bits) % 2
        if result == 1:
            for n in range(self.N):
                if self.table[m][n] == 1:
                    self.vnodes_fails[n] += 1

    def reset_fails(self):
        self.vnodes_fails = np.zeros(self.N, dtype=int)

    def decode(Graph, y, max_iter=20):
        # bit_flipping
        for _ in range(max_iter):
            for m in range(Graph.M):
                Graph.check_node(m, y)
            max_fails_idx = np.argmax(Graph.vnodes_fails)
            max_fails = Graph.vnodes_fails[max_fails_idx]
            if max_fails == 0:
                return y
            else:
                y[max_fails_idx] = (y[max_fails_idx] + 1) % 2   # bit flip, fliping only one bit 
            Graph.reset_fails()

        return y