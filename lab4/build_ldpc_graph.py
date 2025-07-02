from modules.LDPC_BP import LDPC_BP

# rate = 4/7 #
dv = 3      
dc = 7
N = 1001   

# # rate = 1/2 #
# dv = 4     
# dc = 8
# N = 1000   


graph = LDPC_BP(dv, dc, N)

# OUTPUT - .CSV #
graph.export_to_csv("graph_3_7.csv")
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"graph_3_7.csv [OK]\n")
