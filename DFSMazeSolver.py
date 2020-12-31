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


from sys import exit, argv
import time
import os


''' Takes path to selected maze file as a command line argument '''
if len(argv) < 2:
	print('ERROR: This script takes a text file as an argument | DFSMazeSolver.py <path/to/example.txt>')  # check to ensure an argument is present
	exit(-1)
if len(argv) > 2:
	print('ERROR: This script only takes one file as an argument | DFSMazeSolver.py <path/to/example.txt>')  # check to ensure only one argument is present
	exit(-1)
if not argv[1].endswith('.txt'):
	print('ERROR: The selected file is an invalid type, only .txt format is valid | DFSMazeSolver.py <path/to/example.txt>')  # check to ensure an argument is of a valid type (.txt)
	exit(-1)
maze = argv[1]


def build_matrix():
	''' Builds matrix from user selected file '''

	try:
		m = open(maze, 'r')
	except FileNotFoundError as e:
		print('ERROR: The selected file could not be found')
		exit(-1)

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

''' Data Structures '''
try:
	matrix = build_matrix()
except ValueError as e:
	print('Invalid maze format found in '+ maze.split('\\')[-1]+ '. For examples, please refer to the samples provided in the repository.')
	exit(-1)

visited = set()
stack = []
path = []

def main():
	''' Main method '''

	start = get_start()
	if start:
		result = open('.\\'+ maze.split('\\')[-1][:-4]+ '_Results.txt', 'w')
		result.write('*NOTE: DEPTH FIRST SEARCH is an UNWEIGHTED search. The shortest path is NOT guarunteed*\n')
		result.write(f'Start Node: {start}\n')
		result.write('Generating Solution...\n')
		t1 = time.time()
		stack.append(start)
		dfs_path_find()
		t2 = time.time()
		result.write(f'End Node: {path[-1]}\n')
		result.write(f'Path: {path}\n')
		result.write(f'Solve time: {t2 - t1} sec\n')
		result.write('Building visual...\n\n')
		for row in range(len(matrix)):
			for col in range(len(matrix[row])):
				matrix[row][col] = str(matrix[row][col])
		for i in visited:
			y, x = i
			matrix[y][x] = '  '
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
		result.write("KEY: s = Start Node, e = End Node, '_' = Successful Path, 0 = Unvisited Path Node, ' ' = Visited Path Node\n")
		for row in matrix:
			result.write(str(row)+ '\n')
		result.close()

		# Checks for repeat file names in results folder and appends a sequential int value to the file name
		current_loc = result.name.split('\\')[-1]  # ignores full path name as output file is located in script folder
		new_loc = 'Results\\'+ current_loc
		copy_new_loc = new_loc[:]
		flag = True
		out_file_itr = 1
		while flag:
			try:
				os.rename(current_loc, copy_new_loc)
				flag = False
			except FileExistsError as e:
				copy_new_loc = new_loc[:-4]+ str(out_file_itr)+ new_loc[-4:]
				out_file_itr += 1

		print(copy_new_loc[8:-4]+ ' placed in .\\Results')
		exit(0)
	else:
		result.write('ERROR: No Defined Start Node')
		exit(-1)
	
	
def dfs_path_find():
	''' Finds and returns path from start node to end node '''

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


def get_start():
	''' Returns start node '''

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


def get_adj(pos):
	''' Returns list of valid & unvisited adjacent nodes in counter-clockwise order '''

	try:
		y, x = pos
		adj = []
		# up
		if y >= 1 and matrix[y-1][x] in {0, 3} and (y-1, x) not in visited:
			adj.append((y-1, x))
		# left
		if x >= 1 and matrix[y][x-1] in {0, 3} and (y, x-1) not in visited:
			adj.append((y, x-1))
		# right
		if x < len(matrix[0]) - 1 and matrix[y][x+1] in {0, 3} and (y, x+1) not in visited:
			adj.append((y, x+1))
		# down
		if y < len(matrix) - 1 and matrix[y+1][x] in {0, 3} and (y+1, x) not in visited:
			adj.append((y+1, x))
		
		return adj

	except IndexError as e:
		print('Invalid maze format found in '+ maze.split('\\')[-1]+ '. For examples, please refer to the samples provided in the repository.')
		exit(-1)


def backtrack():
	''' Backtracks to last valid node '''

	while True:
		if get_adj(path[len(path)-1]) == []:
			path.remove(path[len(path)-1])  # nonuseful nodes are removed from the path
			if path == []:
				print('ERROR: End Node Unreachable or Undefined')
				exit(-1)
		else:
			break


def end_check(pos):
	''' Checks to see if current node is end node '''

	y, x = pos
	if matrix[y][x] == 3:
		return 1


if __name__ == '__main__':
	main()