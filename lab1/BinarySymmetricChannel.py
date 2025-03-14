import numpy as np

class BinarySymmetricChannel:

    def transmit(input_bits, p):
        output_bits = []
        for bit in input_bits:
            if np.random.rand() < p:
                output_bits.append(1 - bit)
            else:
                output_bits.append(bit)
        return output_bits
