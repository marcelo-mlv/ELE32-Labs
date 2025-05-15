import numpy as np
import random
import csv   

class LDPC_LLR_graph:

    def __init__(self, dv, dc, channel_input):
        
        N = len(channel_input)
        M = int((N * dv) / dc)
        self.N = N
        self.M = M

        self.channel_llrs = self.llr(channel_input)
        # LLRs from the channel input

        self.table = np.array([[(0, 0) for _ in range(N)] for _ in range(M)], dtype=object)
        # adjacency matrix (M x N)  
        # rows = c-nodes (M), columns = v-nodes (N), 
        # tuple[0] = {1 if conected, else 0}, tuple[1] = LLR
        
        vnodes_num_conections = np.zeros(N)
        for m in range(M):
            chooseable_vnodes = [node for node in range(N) if vnodes_num_conections[node] == min(vnodes_num_conections)]
            chosen_vnodes = sorted(random.sample(chooseable_vnodes, dc))
            for vnode in chosen_vnodes:
                self.table[m][vnode][0] = 1
                vnodes_num_conections[vnode] += 1

        self.vnodes_fails = np.zeros(N, dtype=int)


    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for n in range(self.N):
                connected_cnodes = [m for m in range(self.M) if self.table[m][n][0] == 1]
                writer.writerow(connected_cnodes)


    def reset_fails(self):
        self.vnodes_fails = np.zeros(self.N, dtype=int)

    def llr(self, channel_input):

        # to do

        output = np.zeros(self.N, dtype=int)
        return output
    
    def consensus_propagation(self, n):
        conections_idx = np.array([], dtype=int)
        sum = 0
        for m in range(self.M):
            if self.table[m][n][0] == 1:
                conections_idx = np.append(conections_idx, m)
                sum += self.table[m][n][1]
        for m in conections_idx:
            self.table[m][n][1] = sum - self.table[m][n][1]
        return
    
    def discord_propagation(self, m):
        conections_idx = np.array([], dtype=int)
        for n in range(self.N):
            if self.table[m][n][0] == 1:
                conections_idx = np.append(conections_idx, n)
        for n in conections_idx:
            discord = 1
            current_min = np.inf
            for i in conections_idx:
                if i != n:
                    llr = self.table[m][i][1]
                    discord *= np.sign(llr)
                    if llr < current_min:
                        current_min = llr
            discord *= current_min
            self.table[m][n][1] = discord
        return