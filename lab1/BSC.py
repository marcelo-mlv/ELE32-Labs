import numpy as np

def BSC(input_bits, p):
    output_bits = []
    for bit in input_bits:
        if np.random.rand() < p:
            output_bits.append(1 - bit)  # Flip the bit
        else:
            output_bits.append(bit)  # Keep the bit unchanged
    return output_bits
