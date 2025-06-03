import numpy as np
import random
import os
import csv   

CONNECTED = 0
MESSAGE = 1

class LDPC_LLR:

    def __init__(self, dv, dc, N, init_random=True):
        
        M = int((N * dv) / dc)
        self.N = N
        self.M = M

        self.table = np.zeros((M, N, 2))
        # table[m][n] = edge(m,n), m = c-node (M), n = v-node (N) 
        # table[m][n][0] = 'is connected?' (0 [false] or 1 [true])
        # table[m][n][1] = 'message' (LLR)
        
        # randomly generated connections
        if init_random:
            vnodes_num_conections = np.zeros(N)
            for m in range(M):
                chooseable_vnodes = [node for node in range(N) if vnodes_num_conections[node] == min(vnodes_num_conections)]
                chosen_vnodes = sorted(random.sample(chooseable_vnodes, dc))
                for n in chosen_vnodes:
                    self.table[m][n][CONNECTED] = 1
                    vnodes_num_conections[n] += 1

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
                obj.table[c_node][v_node][CONNECTED] = 1

        return obj
    

    def export_to_csv(self, filename):
        path = os.path.join("output", filename)
        with open(path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for n in range(self.N):
                connected_cnodes = np.where(self.table[:, n, CONNECTED] == 1)[0]
                writer.writerow(connected_cnodes + 1)    # i = 1,...,M
    
    # decode
    
    def decode(self, channel_input, Nzero, max_iter=20):

        self.calculate_symbols_llrs(channel_input, Nzero)

        for _ in range(max_iter):

            self.consensus_propagation()

            if self.is_word_valid(): break

            self.discord_propagation()

        output = self.symbols_decision()

        self.reset_messages()

        return output
    
    def calculate_symbols_llrs(self, symbols, Nzero):
        self.llrs = symbols * 4 / Nzero
    
    def consensus_propagation(self):
        for n in range(self.N):
            # Índices dos c-nodes conectados ao v-node n
            cnodes = np.where(self.table[:, n, CONNECTED] == 1)[0]  # pega todos m tal que table[m][n][0] == 1
            # Mensagens recebidas de cada c-node para o v-node n
            cnodes_messages = self.table[cnodes, n, MESSAGE]
            # Soma total das mensagens + LLR do canal
            total = np.sum(cnodes_messages, axis=0) + self.llrs[n]
            # Para cada c-node conectado, atualiza mensagem extrínseca
            self.table[cnodes, n, MESSAGE] = total - cnodes_messages
        return
    
    def discord_propagation(self):
        for m in range(self.M):
            vnodes = np.where(self.table[m, :, CONNECTED] == 1)[0]
            vnodes_messages = self.table[m, vnodes, MESSAGE]
            new_vnodes_messages = np.copy(vnodes_messages)
            for i in range(len(vnodes)):
                others_messages = np.delete(vnodes_messages, i)
                discord = np.prod(np.sign(others_messages)) * np.min(np.abs(others_messages))
                new_vnodes_messages[i] = discord
            self.table[m, vnodes, MESSAGE] = new_vnodes_messages
        return
    
    def is_cnode_valid(self, m):
        vnodes = np.where(self.table[m, :, CONNECTED] == 1)[0]
        vnodes_messages = self.table[m, vnodes, MESSAGE]
        product = np.prod(np.sign(vnodes_messages))
        if product == 1:
            valid = True
        else:
            valid = False
        return valid
    
    def is_word_valid(self):
        valid = True
        for m in range(self.M):
            if self.is_cnode_valid(m) == False:
                valid = False
                break
        return valid
    
    def symbols_decision(self):
        output = np.zeros(self.N)
        for n in range(self.N):
            cnodes = np.where(self.table[:, n, CONNECTED] == 1)[0]  
            cnodes_messages = self.table[cnodes, n, MESSAGE] 
            total = np.sum(cnodes_messages, axis=0) + self.llrs[n]
            if total >= 0:
                output[n] = 1
            else:
                output[n] = -1
        return output

    def reset_messages(self):
        mask = self.table[:, :, CONNECTED] == 1
        self.table[:, :, MESSAGE][mask] = 0
        return