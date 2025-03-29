import numpy as np

class Decoder:
    """
    Represents a decoder that decodes received data.
    """
    def decode(self, *args, **kwargs):
        """
        Decodes the received data.
        """
        pass

class HammingDecoder(Decoder):
    """
    Decodes the received message by correcting the errors using a parity-check matrix H.

    Typical usage example:

    decoder = Decoder()
    decoded_data = decoder.decode(received_data)
    """

    def __init__(self):
        """
        Initializes the Decoder with parity-check matrix H based on Hamming(7, 4) code
        """
        self.H = np.array([
            [1, 1, 1, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 1, 0],
            [1, 1, 0, 1, 0, 0, 1]
        ])

    def getSyndrome(self, r):
        """
        Computes the syndrome of a list of bits using the parity-check matrix H.

        Params:
            r (list): List of bits received.

        Returns:
            s (list): Syndrome of the received message
        """
        return (np.dot(r, self.H.T) % 2).astype(int)

    def getError(self, r):
        """
        Determines the most likely error pattern in the received message r.

        Params:
        r (list):
            Received list of bits.

        Returns:
        e (list):
            Most likely error pattern based on the syndrome.
        """
        s = self.getSyndrome(r)
        e = np.zeros(7, dtype=int)
        if np.all(s == 0):
            return e
        for i in range(0, len(self.H.T)):
            if np.all(s == self.H.T[i]):
                e[i] = 1 - e[i]
                return e

    def decode(self, r, *args, **kwargs):
        """
        Decodes the received message r by correcting the errors

        Params:
            r (list): Received message

        Returns:
            v_hat(list): Decoded message
        """
        e = self.getError(r)
        v_hat = (r + e) % 2
        return v_hat.astype(int)


class MyDecoder(Decoder):
    """
    Decodes the received message by correcting the errors using a parity-check matrix H.

    Typical usage example:

    decoder = Decoder()
    decoded_data = decoder.decode(received_data)
    """

    def __init__(self):
        """
        Initializes the Decoder with parity-check matrix H based on Hamming(7, 4) code
        """
        self.H = np.array([
            [1, 0, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 0, 0, 1, 0],
            [1, 1, 0, 1, 1, 0, 0, 0, 1]
        ])

    def getSyndrome(self, r):
        """
        Computes the syndrome of a list of bits using the parity-check matrix H.

        Params:
            r (list): List of bits received.

        Returns:
            s (list): Syndrome of the received message
        """
        return (np.dot(r, self.H.T) % 2).astype(int)

    def getError(self, r):
        """
        Determines the most likely error pattern in the received message r.

        Params:
        r (list):
            Received list of bits.

        Returns:
        e (list):
            Most likely error pattern based on the syndrome.
        """
        s = self.getSyndrome(r)
        e = np.zeros(9, dtype=int)
        if np.all(s == 0):
            return e
        for i in range(0, len(self.H.T)):
            if np.all(s == self.H.T[i]):
                e[i] = 1 - e[i]
                return e

    def decode(self, r, *args, **kwargs):
        """
        Decodes the received message r by correcting the errors

        Params:
            r (list): Received message

        Returns:
            v_hat(list): Decoded message
        """
        e = self.getError(r)
        v_hat = (r + e) % 2
        return v_hat.astype(int)