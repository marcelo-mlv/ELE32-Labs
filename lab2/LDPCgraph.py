import numpy as np
import random

class LDPCgraph:

    def __init__(self, N, dv, dc):
        M = int((N * dv) / dc)
        self.N = N
        self.dv = dv
        self.dc = dc
        self.M = M

        table = [[0 for _ in range(N)] for _ in range(M)] # row = c-node, column = v-node
        vnodes_num_conections = [0 for _ in range(N)]
        for i in range(M):
            chooseable_vnodes = [node for node in range(N) if vnodes_num_conections[node] == min(vnodes_num_conections)]
            chosen_vnodes = sorted(random.sample(chooseable_vnodes, dc))
            for vnode in chosen_vnodes:
                table[i][vnode] = 1
                vnodes_num_conections[vnode] += 1

        self.table = table
