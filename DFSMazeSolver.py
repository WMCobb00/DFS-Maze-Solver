'''
***********************************
Author: Billy Cobb
Date: 2/27/20
Project: 2D Depth First Search
Disc: Python script to find a 
		path through a maze read 
		in from a .txt file using 
		DFS
***********************************
'''

from sys import exit
import time

#builds matrix from Maze.txt
def build_matrix():
	m = open('Maze.txt', 'r')
	ma = m.read()
	mat = ma.split('\n')
	matr = []
	for i in mat:
		j = i.split(' ')
		matr.append(j)
	for row in range(len(matr)):
		for col in range(len(matr[row])):
			matr[row][col] = int(matr[row][col])
	return(matr)

matrix = build_matrix()
visited = set()
stack = []
path = []

#main method
def main():
	start = get_start()
	if start:
		print('*NOTE: DEPTH FIRST SEARCH is an UNWEIGHTED search. The shortest path is NOT guarunteed*')
		print(f'Start Node: {start}\n')
		print('Generating Solution...\n')
		t1 = time.time()
		stack.append(start)
		dfs_path_find()
		t2 = time.time()
		print(f'End Node: {path[-1]}')
		print(f'Path: {path}')
		print(f'Solve time: {t2 - t1} sec')
		print('Building visual...\n')
		for row in range(len(matrix)):
			for col in range(len(matrix[row])):
				matrix[row][col] = str(matrix[row][col])
		for i in visited:
			y, x = i
			matrix[y][x] = ' '
		for i in path:
			if i is path[0]:
				y, x = i
				matrix[y][x] = 's'
			elif i is path[-1]:
				y, x = i
				matrix[y][x] = 'e'
			elif i in path[1:len(path)-1]:
				y, x = i
				matrix[y][x] = '_'
		print("KEY: s = Start Node, e = End Node, '_' = Successful Path, 0 = Unvisited Path Node, ' ' = Visited Path Node\n")
		for row in matrix:
			print(row)
		exit(0)
	else:
		print('ERROR: No Defined Start Node')
		exit(-1)
	
#finds and returns shortest pat from start node to end node	
def dfs_path_find():
	while stack != []:
		current = stack.pop()
		path.append(current)
		visited.add(current)
		if end_check(current) == 1:
			break
		adj = get_adj(current)
		if adj == []:
			backtrack()
		while adj != []:
			stack.append(adj.pop())		

#returns start node
def get_start():
	start = None
	for row in range(len(matrix)):
		for col in range(len(matrix[row])):
			if matrix[row][col] == 2:
				if start:
					print('ERROR: Multiple Start Nodes Found')
					exit(-1)
				start = (row, col)
	if start:
		return start
	return None

#returns list of valid & unvisited adjacent nodes in counter-clockwise order *Need to make it check for end node before return*
def get_adj(pos):
	y, x = pos
	adj = []
	#up
	if y >= 1 and matrix[y-1][x] in {0, 3} and (y-1, x) not in visited:
		adj.append((y-1, x))
	#left
	if x >= 1 and matrix[y][x-1] in {0, 3} and (y, x-1) not in visited:
		adj.append((y, x-1))
	#right
	if x < len(matrix[0]) - 1 and matrix[y][x+1] in {0, 3} and (y, x+1) not in visited:
		adj.append((y, x+1))
	#down
	if y < len(matrix) - 1 and matrix[y+1][x] in {0, 3} and (y+1, x) not in visited:
		adj.append((y+1, x))
	

	return adj

#backtracks to last valid node
def backtrack():
	while True:
		if get_adj(path[len(path)-1]) == []:
			path.remove(path[len(path)-1])
			if path == []:
				print('ERROR: End Node Unreachable or Undefined')
				exit(-1)
		else:
			break

#checks to see if current node is end node
def end_check(pos):
	y, x = pos
	if matrix[y][x] == 3:
		return 1

main()