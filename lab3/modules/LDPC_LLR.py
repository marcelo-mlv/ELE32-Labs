import numpy as np
import random
import csv   

class LDPC_LLR:

    def __init__(self, dv, dc, channel_input):
        
        N = len(channel_input)
        M = int((N * dv) / dc)
        self.N = N
        self.M = M

        self.bits = channel_input
        self.channel_llrs = self.llr(channel_input)
        # LLRs from the channel input

        self.table = np.array([[(0, 0) for _ in range(N)] for _ in range(M)], dtype=object)
        # adjacency matrix (M x N)  
        # rows = c-nodes (M), columns = v-nodes (N), 
        # tuple[0] = {1 if conected, else 0}, tuple[1] = LLR (message)
        
        vnodes_num_conections = np.zeros(N)
        for m in range(M):
            chooseable_vnodes = [node for node in range(N) if vnodes_num_conections[node] == min(vnodes_num_conections)]
            chosen_vnodes = sorted(random.sample(chooseable_vnodes, dc))
            for vnode in chosen_vnodes:
                self.table[m][vnode][0] = 1
                vnodes_num_conections[vnode] += 1


    def llr(self, channel_input):

        ####################
        ###### to do ######
        ###################

        output = np.zeros(self.N, dtype=int)
        return output
    

    def export_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            for n in range(self.N):
                connected_cnodes = [(m+1) for m in range(self.M) if self.table[m][n][0] == 1]   # i = 1,...,N
                writer.writerow(connected_cnodes)
    
    # decode
    
    def decode(self, max_iter=20):
        for _ in range(max_iter):

            for n in range(self.N):
                self.consensus_propagation(n)

            is_word_valid = True
            for m in range(self.M):
                if self.is_cnode_valid(m) == False:
                    is_word_valid = False
                    break
            if is_word_valid == True: break

            for m in range(self.M):
                self.discord_propagation(m)

        for n in range(self.N):
            self.bit_decision(n)

        return self.bits
    
    def consensus_propagation(self, n):
        conections_idx = np.array([], dtype=int)
        sum = self.channel_llrs[n]
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
    
    def is_cnode_valid(self, m):
        product = 1
        valid = True
        for n in range(self.N):
            if self.table[m][n][0] == 1:
                product *= np.sign(self.table[m][n][1])
        if product == -1:
            valid = False
        return valid
    
    def bit_decision(self, n):
        sum = self.channel_llrs[n]
        for m in range(self.M):
            if self.table[m][n][0] == 1:
                sum += self.table[m][n][1]
        if sum >= 0:
            self.bits[n] = 0
        else:
            self.bits[n] = 1