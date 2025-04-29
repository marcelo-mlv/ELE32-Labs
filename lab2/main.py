import numpy as np
import random

def gerar_matriz_paridade(N, dv, dc):
    """Gera matriz de paridade H para código LDPC regular."""
    M = (N * dv) // dc
    H = np.zeros((M, N), dtype=int)
    
    edges = []
    for i in range(N):
        for _ in range(dv):
            edges.append(i)
    
    check_nodes = list(range(M)) * dc
    if len(edges) != len(check_nodes):
        raise ValueError("Parâmetros inválidos: número de arestas não bate.")

    random.shuffle(check_nodes)
    
    for v, c in zip(edges, check_nodes):
        while H[c, v] == 1:  # evitar múltiplas conexões
            c = random.choice(range(M))
        H[c, v] = 1

    return H

def bsc_transmit(codeword, p):
    """Simula transmissão em canal BSC com probabilidade de erro p."""
    errors = np.random.rand(len(codeword)) < p
    return (codeword + errors.astype(int)) % 2

def bit_flipping(H, y, max_iter=50):
    """Algoritmo Bit-Flipping."""
    y = y.copy()
    for _ in range(max_iter):
        syndrome = (H @ y) % 2
        if np.all(syndrome == 0):
            break

        unsat = H @ y % 2
        erro_por_bit = H.T @ unsat
        max_erros = np.max(erro_por_bit)

        if max_erros == 0:
            break

        flip_indices = np.where(erro_por_bit == max_erros)[0]
        y[flip_indices] = 1 - y[flip_indices]
    
    return y

# Parameters for LDPC code
N_values = [100, 200, 500, 1000]  # Code lengths
dv = 3  # Edges per v-node
dc = 6  # Edges per c-node (Rate = 1 - dv/dc = 0.5)
p_values = [0.1, 0.05, 0.02, 0.01, 0.001, 0.0001]  # BSC error probabilities

# Simulate for different code lengths
for N in N_values:
    print(f"\nSimulating for N = {N}")
    results = simulate_ldpc(N, dv, dc, p_values)
    for p, ber in results.items():
        print(f"p = {p:.5f}, BER = {ber:.5e}")