import numpy as np
from ParityMatrixGenerator import generate_parity_matrix
from LDPCDecoder import bit_flipping_decoder

def simulate_ldpc(N, dv, dc, p_values, max_iter=50):
    """
    Simulates the performance of an LDPC code over a BSC.

    Params:
        N (int): Number of variable nodes (v-nodes).
        dv (int): Number of edges per v-node.
        dc (int): Number of edges per c-node.
        p_values (list): List of BSC error probabilities.
        max_iter (int): Maximum number of iterations for decoding.

    Returns:
        dict: BER results for each p in p_values.
    """
    H = generate_parity_matrix(N, dv, dc)
    info = np.zeros(N, dtype=int)  # All-zero codeword for simplicity
    codeword = info.copy()

    ber_results = {}
    for p in p_values:
        errors = 0
        trials = 1000  # Number of codewords to simulate

        for _ in range(trials):
            received = (codeword + (np.random.rand(len(codeword)) < p).astype(int)) % 2
            decoded = bit_flipping_decoder(H, received, max_iter)
            errors += np.sum(decoded != codeword)

        ber = errors / (trials * len(codeword))
        ber_results[p] = ber

    return ber_results