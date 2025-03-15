import numpy as np

class BinarySymmetricChannel:
    """Simulates data transmission through a binary symmetric channel.

    Typical usage example:

    transmitted_data = channel.transmit(encoded_data)
    """

    def transmit(input_bits, p):
        output_bits = []
        for bit in input_bits:
            if np.random.rand() < p:
                output_bits.append(1 - bit)
            else:
                output_bits.append(bit)
        return output_bits
