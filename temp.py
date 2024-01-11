# -*- codeing = utf-8 -*-
# @Time: 2023/4/10 22:51
# @Author: Jasmin
# @File: temp.py
# @Software: PyCharm

import pandas as pd
import networkx as nx
import netwulf
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex


#for weight, use 1)frequency 2)total transaction volumn

# load data - with sampling
before_sampling = pd.read_csv('Data_API.csv', usecols=['Seller_address', 'Buyer_address', 'Datetime_updated'])
data1 = before_sampling[(before_sampling['Datetime_updated'] >= '2019-01-01 00:00:00') & (before_sampling['Datetime_updated'] < '2019-01-02 00:00:00')]
data = data1.sample(frac=0.001)


# get unique seller and buyer addresses
unique_addresses = set(data['Seller_address']) | set(data['Buyer_address'])
# unique_addresses = pd.unique(pd.concat([data['Seller_address'], data['Buyer_address']]))
print ("Number of Node",len(unique_addresses))

# create graph
print ("create graph")
G = nx.Graph()

# add nodes to the graph
print ("add nodes and edges to the graph")
for addr in unique_addresses:
    G.add_node(addr)

# add edges to the graph
for index, row in data.iterrows():
    seller = row['Seller_address']
    buyer = row['Buyer_address']
    if G.has_edge(seller, buyer):
        # edge already exists, increment weight
        G[seller][buyer]['weight'] += 1
    else:
        # new edge, add with weight=1
        G.add_edge(seller, buyer, weight=1)


##################################################################################################
############################################# features  ##########################################
##################################################################################################
cc = nx.average_clustering(G)
print("Clustering coefficient:", cc)

diameter = nx.diameter(G)
print("Diameter:", diameter)

print ("Number of Node",len(unique_addresses))

num_edges = G.number_of_edges()
print("Number of edges:", num_edges)

degree_corr = nx.degree_assortativity_coefficient(G)
print("Degree assortativity coefficient:", degree_corr)

density = nx.density(G)
print("Density:", density)

##################################################################################################
########################################## visualization  ########################################
##################################################################################################

'''
# node color\
print ("add the property of profit")
profit_data = pd.read_csv('profit_with_group.csv')
# profit_data.set_index('Buyer_address', inplace=True)
profit_data.set_index('Buyer_address', inplace=True)


print ("start loop")
for i, node in enumerate(G.nodes()):
    if node in profit_data.index:
        G.nodes[node]['group'] = profit_data.at[node, 'Group']
        print("Finished loop", i+1)
    else:
        G.nodes[node]['group'] = -1
print("Finished merging profits to graph")

# create a dictionary that maps each node to its corresponding attribute value
group_dict = {node: G.nodes[node]['group'] for node in G.nodes()}
print(G.nodes(data=True))
# set the 'group' attribute for each node in the graph
nx.set_node_attributes(G, group_dict, 'group')



# node size\
# Set node 'size' attributes
# degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
# Eigenvector_centrality = nx.eigenvector_centrality(G)
# PageRank_centrality = nx.pagerank(G)

node_size = {n: 5000 * betweenness_centrality[n] for n in G.nodes()}
nx.set_node_attributes(G, node_size, 'size')
print("Finished size assignment")

# visualize the graph using netwulf with node size based on degree centrality
netwulf.visualize(G)

'''


