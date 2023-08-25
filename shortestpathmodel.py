import numpy as np
import pandas as pd
import os
import networkx as nx
import matplotlib.pyplot as plt

data = pd.read_csv('airlinedata.csv')


#converting "sched_dep_time" to "std" - scheduled time of departure 
data['std'] = data.sched_dep_time.astype(str).str.replace('(\d{2}$)','') + ':' + data.sched_dep_time.astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

#conveting shed_arr_time to 'sta' - Scheduled time of arrival
data['sta'] = data.sched_arr_time.astype(str).str.replace('(\d{2}$)', '') + ':' + data.sched_arr_time.astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

#converting "dep_time" to "atd" - actual time of departure 
data['atd'] = data.dep_time.fillna(0).astype(np.int64).astype(str).str.replace('(\d{2}$)','') + ':' + data.dep_time.fillna(0).astype(np.int64).astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

#converting "arr_time" to "ata" - actual time of arrival 
data['ata'] = data.arr_time.fillna(0).astype(np.int64).astype(str).str.replace('(\d{2}$)','') + ':' + data.arr_time.fillna(0).astype(np.int64).astype(str).str.extract('(\d{2}$)', expand=False) + ':00'

#converting date into year/month/day
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])
data = data.drop(columns = ['year', 'month', 'day'])              

FG = nx.from_pandas_edgelist(data, source ='origin', target = 'dest', edge_attr=True,)

FG.nodes()
FG.edges()
nx.draw_networkx(FG, with_labels=True, node_size= 500, node_color='y')

nx.algorithms.degree_centrality(FG)

#averages density of the graphs
nx.density(FG)
#Average shortest path for all paths in the graph
nx.average_shortest_path_length(FG)
#for a node of degree k - what is the averahe of its neighbours degree
nx.average_degree_connectivity(FG) 

print('All possible paths:')
#finding all paths from 'JAX' to 'DFW'
for path in nx.all_simple_paths(FG, source='JAX', target='DFW'):
    print(path)

#now find the shortest (Dijkstra) path from 'JAX' to "DFW'
dijpath = nx.dijkstra_path(FG, source='JAX', target='DFW')
dijpath

shortpath = nx.dijkstra_path(FG, source='JAX', target='DFW', weight='air_time')
shortpath

total_time_minutes = 0
for i in range(len(shortpath) - 1):
    source_node = shortpath[i]
    target_node = shortpath[i+1]
    edge_data =FG[source_node][target_node]
    total_time_minutes += edge_data['air_time']

total_hours, remaining_minutes = divmod(total_time_minutes, 60)

print('Shortest path:', shortpath)
print("Total time for shortest path:", f"{total_hours} hours and {remaining_minutes} minutes")

pos = nx.spring_layout(FG)  # Layout for visualization
edge_colors = ['r' if (u, v) in zip(shortpath, shortpath[1:]) else 'b' for u, v in FG.edges()]

nx.draw_networkx_nodes(FG, pos, node_size=500, node_color='y')
nx.draw_networkx_edges(FG, pos, edge_color=edge_colors)
nx.draw_networkx_labels(FG, pos)
plt.show()





