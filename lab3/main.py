from modules.Encoder import HammingEncoder, MyEncoder
from modules.Decoder import HammingDecoder, MyDecoder
from modules.Channel import BinarySymmetricChannel
from modules.System import System
from modules.LDPC import LDPCgraph, bit_flipping_decoder
from modules.LDPC_LLR import LDPC_LLR_graph

import random
import numpy as np
import matplotlib.pyplot as plt


# # System declaration

# # Hamming
# hamming_encoder = HammingEncoder()
# hamming_decoder = HammingDecoder()
# bsc = BinarySymmetricChannel()

# channel_only = System(None, None, bsc)
# hamming_system = System(hamming_encoder, hamming_decoder, bsc)


# # LDPC

dv = 3
dc = 7
N = 98
graph = LDPC_LLR_graph(N,dv,dc)
graph.export_to_csv('ldpc_graph.csv')



# N_values = [98, 196, 497, 994]         
# bit_flipping_max_iter = 50 

# # plots

# n_iterations = 20
# p_values = np.logspace(-5, np.log10(0.5), n_iterations)       # Probability of a bit being flipped during transmission
# co_pb_values = np.zeros(p_values.size)                        # System bit error probability (channel only)
# hamming_pb_values = np.zeros(p_values.size)                   # System bit error probability (hamming)             
# LDPC_pb_values = np.zeros((len(N_values), p_values.size))     # System bit error probability (LDPC: N~100, N~200, N~500, N~1000)

# sample_size = np.logspace(4, 6.5, p_values.size, dtype=int)[::-1]

# for k in range(p_values.size):
    
#     num_of_flipped_bits = np.zeros(len(N_values) + 2)

#     # LDPCs
#     for i in range(len(N_values)):
#         N = N_values[i]
#         input_bits = np.zeros(N, dtype=int)
#         channel_bits = bsc.transmit(input_bits, p_values[k])
#         decoded_bits = bit_flipping_decoder(LDPCgraph(N,dv,dc), channel_bits, bit_flipping_max_iter)
#         for bit in decoded_bits:
#             if bit == 1:
#                 num_of_flipped_bits[i] += 1
#         LDPC_pb_values[i][k] = num_of_flipped_bits[i] / N
       
#     # channel only
#     random_bits = [random.randint(0, 1) for _ in range(sample_size[k] - sample_size[k]%20)]

#     channel_bits = channel_only.process(random_bits.copy(), p_values[k])

#     for j in range(len(random_bits)):
#         if random_bits[j] != channel_bits[j]:
#             num_of_flipped_bits[4] += 1
    
#     co_pb_values[k] = num_of_flipped_bits[4] / len(random_bits)

#     # hamming
#     for i in range(0, len(random_bits), 4):

#         u = random_bits[i:i+4]
    
#         v_hat = hamming_system.process(u.copy(), p_values[k])
#         u_hat = v_hat[:4]

#         for j in range(len(u)):
#             if u[j] != u_hat[j]:
#                 num_of_flipped_bits[5] += 1

#     hamming_pb_values[k] = num_of_flipped_bits[5] / len(random_bits)


#     print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
#     print(f"Iteration no. {k+1}")
#     print(f"Sample size: {sample_size[k]}")
#     print(f"p: {p_values[k]}")
#     print(f"\tCHANNEL ONLY: pb = {co_pb_values[k]:.7f}")
#     print(f"\tHAMMING:      pb = {hamming_pb_values[k]:.7f}")
#     print(f"\tLDPC, N~100:   pb = {LDPC_pb_values[0][k]:.7f}")
#     print(f"\tLDPC, N~200:   pb = {LDPC_pb_values[1][k]:.7f}")
#     print(f"\tLDPC, N~500:   pb = {LDPC_pb_values[2][k]:.7f}")
#     print(f"\tLDPC, N~1000:   pb = {LDPC_pb_values[3][k]:.7f}")

# """
# Plots the bit error probability as a function of the probability of a bit being flipped during transmission.
#     x axis: p_values (list), reversed, in logarithmic scale
#     y axis: pb_values (list), in logarithmic scale
# """
# plt.figure()
# plt.plot(p_values, co_pb_values, label='Somente Canal')
# plt.plot(p_values, hamming_pb_values, label='Hamming')
# plt.plot(p_values, LDPC_pb_values[0], label='LDPC N~100')
# plt.plot(p_values, LDPC_pb_values[1], label='LDPC N~200')
# plt.plot(p_values, LDPC_pb_values[2], label='LDPC N~500')
# plt.plot(p_values, LDPC_pb_values[3], label='LDPC N~1000')
# plt.xscale('log')
# plt.yscale('log')
# plt.xlabel('P')
# plt.ylabel('Pb')
# plt.title("Prob. inversão de bit pós decodificação x prob. inversão de bit no canal")
# plt.grid(True)
# plt.legend()
# plt.gca().invert_xaxis()

# # Save the plot as a PNG file
# plt.savefig("plot_vsHamming.png", format="png")

# plt.show()