
class System:
    """
    Represents a communication system that includes an encoder, a channel, and a decoder.
    """
    def __init__(self, encoder, decoder, channel):
        """
        Initializes the System with an encoder, a decoder, and a channel.

        Params:
            encoder (Encoder or None): The encoder to be used in the system.
            decoder (Decoder or None): The decoder to be used in the system.
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
            processed_data (list): The processed data after transmission through the channel.
        """
        if self.encoder:
            data = self.encoder.encode(data)
        data = self.channel.transmit(data, p)
        if self.decoder:
            data = self.decoder.decode(data)
        return data
