
#%% 
# importing data
#%%
import data.mongo_setup as mongo_setup
from classes.tweeter_hashtag_manager import *

from colorama import Fore
import networkx as nx
import math
import matplotlib.pyplot as plt
import pandas as pd
import json
from pandas.io.json import json_normalize
import networkx as nx
from networkx.algorithms import community
import copy as copy


def plot_graph( G0, pos, G1 = None, labels = True, title = None):
    """ 
    plotting graph 
        *args:
            G0
                graph that contain all nodes
            pos:
                fixed possition of the edges
            G1:
                graph that contains the edges that we want to display,
                if doesn't exist take the edges of G0

    """

    if title == None:
        plt.title("Graph Image")
    else:
        plt.title(title)
    nx.draw_networkx(G0, pos,
                with_labels=labels,
                font_size = 8,
                node_size=0.5,
                node_color = 'k',
                edge_color = 'r',
                alpha = 0.3
    )
    if G1 == None:
        G1 = G0
    centrality = nx.degree_centrality(G1)
    centrality = json_normalize(centrality).transpose()
    type(centrality)
    centrality = centrality.sort_values(by = 0, ascending = False)
    centrality = pd.DataFrame(centrality)
    centrality.columns = ["centrality"]
    print(centrality.head(10))
    centrality.to_csv(f"./storage/cent_{title}.csv")

    betweenness_centrality = nx.betweenness_centrality(G1)
    betweenness_centrality = json_normalize(betweenness_centrality).transpose()
    type(betweenness_centrality)
    betweenness_centrality = betweenness_centrality[0].sort_values( ascending = False)
    betweenness_centrality = pd.DataFrame(betweenness_centrality)
    betweenness_centrality.columns = ["betweenness"]
    print(betweenness_centrality.head(10))
    #     g_comp_tag = {}
    # g_comp_tag['international'] = g_comp['0']
    #    g_comp_tag['national'] = g_comp['1']

    nx.draw_networkx_edges(G1, pos,
                            with_labels = False,
                            node_color = 'k',
                            edge_color = 'g',
                            width = 0.6
    )
    plt.savefig(f'./storage/{title}.png')
    plt.show()
#%%
# Create Tweeter Hashtag Manager


#%%
my_tweeter_hashtag_manager = Tweeter_hashtag_manager()

#%%
# Create Graph

#%%
space_names = [
    "guatemala",
    "corrupcion"
]
g = my_tweeter_hashtag_manager.graph_manager.import_graph(
                space_names = space_names
            )
print(g)

#%%

# my_tweeter_hashtag_manager.graph_manager.descrive_graph(g, space_names = space_names)

#%%
# Giant Component and Visualize the graph


#%%
layout = nx.spring_layout
print(f"number of nodes: {len(g)}")
G = g
pos = layout(G)
plt.title("First Giant Component")
nx.draw_networkx(G, pos,
        with_labels=False,
        node_size=0.5,
        node_color = 'b',
        edge_color = 'w'
        )
# identify largest connected component
Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
if len(Gcc[0]) != len(G):
    auxCount = 0
    for iG in Gcc[1:]:
        print(f"{len(iG.nodes)} filtered node = {iG.nodes}")
        auxCount += len(iG)
    print(f"{auxCount} filtered nodes: {Gcc[1:]}")
G0 = Gcc[0]
plot_graph(g, pos, G0, labels= False, title= "Complete graph")
plot_graph(g, pos, G0, labels= True, title = "Nodes within the Giant Component")
#%%
g2 = G0

#%%
## Filter the components that don't belog to the giant component

#%%
plot_graph(g2,pos, title = "graph of the selected Giant Component")


#%%
g3 = g2


#%% 
# Assorsativity analysis
## Everything is normal so let's to understand if there is a tendency assorciative or dissarosative, due that for the analysis should be assorsiative, because there exist blogers that we want to cut off

#%%
assort_degree = nx.degree_assortativity_coefficient(g3)
print(f"the assorsiativity degree of the giant component is {assort_degree}")


#%% 
## let's search the nodes with more centrality - top 4

#%%
print("centrality")
centrality = nx.degree_centrality(g3)
centrality = json_normalize(centrality).transpose()
centrality = centrality.sort_values(by = 0, ascending = False)
centrality.head(5)

#%%
## let's cut off Guatemala, because is ilogic for a context to be here, and see the assorsiativity ones more

#%%

g4 = copy.deepcopy(g3)
g4.remove_node("Guatemala")
plot_graph(g3,pos,G1 = g4, title= "Removal of Guatemala Node")



assort_degree = nx.degree_assortativity_coefficient(g4)
print(f"the assorsiativity degree of the graph is {assort_degree}")



#%%
## the assorciativity has gone up so right now it could be say, that with a assorsiativity behavior it will be principal concepts and principal bloggers, we want to erease the bloggers


#%%
## we can see that left some of nodes out-side of the giant component, let's erease them!


#%%
#%%
layout = nx.spring_layout
print(f"number of nodes: {len(g)}")
G = g4
pos = layout(G)
nx.draw_networkx(G, pos,
        with_labels=False,
        node_size=0.5,
        node_color = 'b',
        edge_color = 'w'
        )
# identify largest connected component
Gcc = sorted(nx.connected_component_subgraphs(G), key=len, reverse=True)
if len(Gcc[0]) != len(G):
    auxCount = 0
    for iG in Gcc[1:]:
        print(f"{len(iG.nodes)} filtered node = {iG.nodes}")
        auxCount += len(iG)
    print(f"{auxCount} filtered nodes: {Gcc[1:]}")
G0 = Gcc[0]
plot_graph(g4,pos,G1 = G0, labels = True, title = "Nodes outside from the Giant Component after Guatemalas node Removal")

#%%
print(len(Gcc))
g5 = copy.deepcopy(G0)


#%%


#%%
## all the elements are inside the giant component

# finding communitites

## let's see a little of centrality and betweenness to understand if it can be important nodes of different communities


#%%
centrality = nx.degree_centrality(g5)
centrality = json_normalize(centrality).transpose()
type(centrality)
centrality.sort_values(by = 0, ascending = False)
centrality = pd.DataFrame(centrality)
print(centrality.head(10))
#%%
betweenness_centrality = nx.betweenness_centrality(g5)
betweenness_centrality = json_normalize(betweenness_centrality).transpose()
type(betweenness_centrality)
betweenness_centrality = betweenness_centrality[0].sort_values( ascending = False)
betweenness_centrality = pd.DataFrame(betweenness_centrality)
print(betweenness_centrality.head(10))

#%%
# we can see that there is an evironemnt of internationals, nationals and journals/bloggers let's see wich method take the communities that we want

## the greedy community 

#%%
nx.community.greedy_modularity_communities(g4)


#%% 
## as the greedy community doesn't split weel the left nodes, let's consider the girvan_newman


#%%
comp = nx.community.girvan_newman(g5)

#%%

comp_tuple = tuple(sorted(c) for c in next(comp))
type(comp_tuple)
# print(iComp for iComp in comp_tuple)

#%%
[iComp for iComp in comp_tuple]

#%%
len(comp_tuple)


#%%

g_comp = {}
comp_tuple[0]
auxCount = 0
for iComp_tuple in comp_tuple:
    g_comp[str(auxCount)]= copy.deepcopy(g5)
    g_comp[str(auxCount)].remove_nodes_from(iComp_tuple)
    plot_graph(g5, pos, G1 =g_comp[str(auxCount)], labels= True, title= f"Giant Component community No. {str(auxCount)}")
    #print(f"Com {auxCount} has {len(iComp_tuple)} nodes in: {iComp_tuple}")
    auxCount +=1

#%%
## we have to see if there exist some tendency of each group

#%%
g_comp_tag = {}
g_comp_tag['international'] = g_comp['0']
g_comp_tag['national'] = g_comp['1']
for iG_comp in g_comp_tag:
    print(f"{iG_comp} nodes, with total of nodes {len(g_comp_tag[iG_comp].nodes)}")
    auxDf = pd.DataFrame(g_comp_tag[iG_comp].nodes)
    print(auxDf.head(10))

#%%
## we found that the there is a international tendecy and national tendecy, let's rename like that



#%%
# communities of inner groups

#%%
comp_nac = nx.community.greedy_modularity_communities(g_comp_tag['national'])

#%%

g_comp_nac = {}
auxCount = 0
print("National communities")
for iComp_nac in comp_nac:
    g_comp_nac[str(auxCount)]= copy.deepcopy(g_comp_tag['national'])
    g_comp_nac[str(auxCount)].remove_nodes_from(iComp_nac)
    left_nodes = copy.deepcopy(g_comp_nac[str(auxCount)].nodes)
    print(f"Com {auxCount} : {iComp_nac}")
    g_comp_nac[str(auxCount)]= copy.deepcopy(g_comp_tag['national'])
    g_comp_nac[str(auxCount)].remove_nodes_from(left_nodes)
    plot_graph(g_comp_tag['national'], pos, 
        G1= g_comp_nac[str(auxCount)], 
        title= f"National Community {auxCount} ")
    auxCount +=1


#%%
## national groups, divided in corrupt, help against corrupt and journals and movements, we can see that the persons are in the top of betweenness and the bloggers are in the most of the top 10 of the centrality.
#%%
comp_internac = nx.community.greedy_modularity_communities(g_comp_tag['international'])

g_comp_internac = {}
auxCount = 0
print("International Communities")
for iComp_internac in comp_internac:
    #delete the partition, so we can know which nodes left
    g_comp_internac[str(auxCount)]= copy.deepcopy(g_comp_tag['international'])
    g_comp_internac[str(auxCount)].remove_nodes_from(iComp_internac)
    #delete the nodes that are left
    left_nodes = copy.deepcopy(g_comp_internac[str(auxCount)].nodes)
    print(f"Community {auxCount}: {iComp_internac}")
    g_comp_internac[str(auxCount)]= copy.deepcopy(g_comp_tag['international'])
    g_comp_internac[str(auxCount)].remove_nodes_from(left_nodes)
    plot_graph(g_comp_tag['international'], pos, 
        G1= g_comp_internac[str(auxCount)], 
        title= f"International Community {auxCount}")
    auxCount +=1

#%%
## internaltional groups

#%%


#%%
