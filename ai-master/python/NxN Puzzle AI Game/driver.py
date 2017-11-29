import sys
import time
import os
#import resource
from time import clock
import search_algorithms


initial_time = time.time()

if(sys.argv[1]=="bfs"):
	result = search_algorithms.breadth_first_search(sys.argv[2])
elif(sys.argv[1]=="dfs"):
	result = search_algorithms.depth_first_search(sys.argv[2])
elif(sys.argv[1]=="ast"):
	result = search_algorithms.a_star(sys.argv[2])
elif(sys.argv[1]=="ida"):
	result = search_algorithms.ida_star(sys.argv[2])


max_fringe_size = result[1]
fringe_size = result[2]
max_search_depth = result[3]
nodes_expanded = result[4]

path_to_goal = []
node = result[0]
while node.parent != None:
	path_to_goal.insert(0, node.direction)
	node = node.parent


end_time = time.time()

running_time = end_time - initial_time
running_time = round(running_time,8)

max_ram_usage = 0
#resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000

output = ""
output += 'path_to_goal: '+ str(path_to_goal)+'\n'
output += 'cost_of_path: '+ str(result[0].depth)+'\n'
output += 'nodes_expanded: '+ str(nodes_expanded)+'\n'
output += 'fringe_size: '+ str(fringe_size)+'\n'
output += 'max_fringe_size: '+ str(max_fringe_size)+'\n'
output += 'search_depth: '+ str(result[0].depth)+'\n'
output += 'max_search_depth: '+str(max_search_depth)+'\n'
output += 'running_time: '+ str(running_time)+'\n'
output += 'max_ram_usage: '+ str(max_ram_usage)

file = open('output.txt', 'w')
file.write(output)

file.close()
