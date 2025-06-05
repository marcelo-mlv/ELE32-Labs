import numpy as np

class Channel:
    """
    Represents a communication channel through which data is transmitted.
    """
    def transmit(self, *args, **kwargs):
        """
        Simulates the transmission of data through the channel.
        """
        pass

class BinarySymmetricChannel(Channel):
    """
    Simulates data transmission through a Binary Symmetric Channel (BSC).

    Typical usage example:

    transmitted_data = channel.transmit(encoded_data)
    """

    def transmit(self, input_bits, p, *args, **kwargs):
        """
        Simulates the transmission of bits through a BSC.

        Params:
            input_bits (list): List of bits to be transmitted.
            p (float): Probability of a bit being flipped during transmission.

        Returns:
            output_bits (list): List of bits after transmission through the channel.
        """
        output_bits = []
        for bit in input_bits:
            if np.random.rand() < p:
                output_bits.append(1 - bit)
            else:
                output_bits.append(bit)
        return np.array(output_bits, dtype=int)
    
class AWGNChannel(Channel):
    """
    Simulates data transmission through a AWGN Channel.

    Typical usage example:

    transmitted_data = channel.transmit(encoded_data)
    """

    def transmit(self, input_symbols, Nzero, *args, **kwargs):
        """
        Simulates the transmission of symbols through a AWGN Channel.

        Params:
            input_symbols (list): List of symbols to be transmitted.
            Nzero (float): parameter for the Gaussian distribution, var = N0/2

        Returns:
            output_symbols (list): List of symbols after transmission through the channel.
        """
        noise = np.random.normal(loc=0, scale=np.sqrt(Nzero/2), size=len(input_symbols))
        output_symbols = noise + input_symbols
        return output_symbols
