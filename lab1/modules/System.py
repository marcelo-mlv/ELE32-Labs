class Channel:
    """
    Represents a communication channel through which data is transmitted.
    """
    def transmit(self, *args, **kwargs):
        """
        Simulates the transmission of data through the channel.
        """
        pass

class Encoder:
    """
    Represents an encoder that encodes data before transmission.
    """
    def encode(self, *args, **kwargs):
        """
        Encodes the input data.
        """
        pass

class Decoder:
    """
    Represents a decoder that decodes received data.
    """
    def decode(self, *args, **kwargs):
        """
        Decodes the received data.
        """
        pass

class System:
    """
    Represents a communication system that includes an encoder, a channel, and a decoder.
    """
    def __init__(self, encoder, decoder, channel):
        """
        Initializes the System with an encoder, a decoder, and a channel.

        Params:
            encoder (Encoder): The encoder to be used in the system.
            decoder (Decoder): The decoder to be used in the system.
            channel (Channel): The channel to be used in the system.
        """
        self.encoder = encoder
        self.decoder = decoder
        self.channel = channel

    def process(self, data, p):
        """
        Processes the input data by encoding it, transmitting it through the channel, and decoding it.

        Params:
            data (list): The input data to be processed.
            p (float): The probability of a bit being flipped during transmission.

        Returns:
            decoded_data (list): The decoded data after transmission through the channel.
        """
        encoded_data = self.encoder.encode(data)
        transmitted_data = self.channel.transmit(encoded_data, p)
        decoded_data = self.decoder.decode(transmitted_data)
        return decoded_data
