import numpy as np
import random

class LDPCgraph:

    def __init__(self, N, dv, dc):
        M = int((N * dv) / dc)
        self.N = N
        self.M = M

        self.table = np.array((M,N), dtype=int) # row = c-node, column = v-node
        vnodes_num_conections = [0 for _ in range(N)]
        for m in range(M):
            chooseable_vnodes = [node for node in range(N) if vnodes_num_conections[node] == min(vnodes_num_conections)]
            chosen_vnodes = sorted(random.sample(chooseable_vnodes, dc))
            for vnode in chosen_vnodes:
                self.table[m][vnode] = 1
                vnodes_num_conections[vnode] += 1

        self.vnodes_fails = np.array(N, dtype=int)

    def check_node(self, m, input_bits):
        result = np.dot(np.array(self.table[m]).T, input_bits) % 2
        if result == 1:
            for n in range(self.N):
                if self.table[m][n] == 1:
                    self.vnodes_fails[n] += 1

    def reset_fails(self):
        self.vnodes_fails = np.array(self.N, dtype=int)
