from modules.LDPC_BP import LDPC_BP

# rate = 4/7 #
dv = 3      
dc = 7
N = 1001   #98, 994, 1001

graph = LDPC_BP(dv, dc, N)

# OUTPUT - .CSV #
graph.export_to_csv('ldpc_graph.csv')
print(f"=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=\n")
print(f"ldpc_graph.csv [OK]\n")
