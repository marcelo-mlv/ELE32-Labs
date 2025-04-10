import numpy as np

def bit_flipping_decoder(H, y, max_iter=50):
    """
    Decodes a received word using the Bit-Flipping algorithm.

    Params:
        H (np.ndarray): Parity-check matrix.
        y (np.ndarray): Received word.
        max_iter (int): Maximum number of iterations.

    Returns:
        np.ndarray: Decoded word.
    """
    y = y.copy()
    for _ in range(max_iter):
        syndrome = (H @ y) % 2
        if np.all(syndrome == 0):
            break

        unsat = H @ y % 2
        error_per_bit = H.T @ unsat
        max_errors = np.max(error_per_bit)

        if max_errors == 0:
            break

        flip_indices = np.where(error_per_bit == max_errors)[0]
        y[flip_indices] = 1 - y[flip_indices]

    return y