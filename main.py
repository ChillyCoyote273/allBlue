import numpy as np
import scipy as sp
import graphviz
import os
from tqdm import tqdm


def get_moves_from_string(move_string: str):
	moves = [c for c in move_string if c != ' ']
	try:
		moves = [int(move) for move in moves]
	except:
		return (np.array([]), True)
	move_array = np.array([0] * 10)
	for move in moves:
		move_array[move] = 1
	return (move_array, False)


def get_moves_from_file():
	with open('moveString.txt') as file:
		moves = file.read()
		return get_moves_from_string(moves)


def get_flipped_nodes(state: np.ndarray[int]) -> str:
	readout = ''
	for i, node in enumerate(state):
		if node == 1:
			readout += f'{i} '
	return readout

def compute_valid_states(edge_matrix: np.ndarray[int, int], num_colors: int = 2) -> np.ndarray[int]:
	for num in tqdm(range(num_colors ** 10)):
		move_array = np.array([0] * 10)
		for idx in range(10):
			move_array[idx] = num % num_colors
			num >>= 1
		state = edge_matrix.dot(move_array) % num_colors
		yield state


def get_node_position(index: int) -> str:
	INNER_RADIUS = 1
	OUTER_RADIUS = 2
	angle = ((index % 5) * 0.4 + 0.5) * np.pi
	radius = INNER_RADIUS if index > 4 else OUTER_RADIUS
	x = radius * np.cos(angle)
	y = radius * np.sin(angle)
	return f'{-x}, {y}!'


def create_graph(edge_matrix: np.ndarray[np.ndarray[int]], state: np.ndarray[int], name: str = 'Petersen Graph', dir: str = 'graphs'):
	colors = ['blue', 'red', 'green']
	graph = graphviz.Graph(name, directory=dir, filename=f'{name}.dot', engine='neato', format='png')
	for i, vertex in enumerate(state):
		graph.node(f'{i}', f'{i}', color = colors[vertex], pos = get_node_position(i))
	for i, row in enumerate(edge_matrix):
		for j, edge in enumerate(row):
			if i < j and edge == 1:
				graph.edge(f'{i}', f'{j}', constraint='false')
	graph.render()


def clean_graph_directory(dir: str = 'graphs'):
	dir_name = f'C:\\Users\\Alex Prichard\\VSCodeProjects\\Python\\allBlue\\{dir}\\'
	directory = os.listdir(dir_name)
	for file in directory:
		if file.endswith('.dot'):
			os.remove(os.path.join(dir_name, file))


def clear_graph_directory(dir: str = 'graphs'):
	dir_name = f'C:\\Users\\Alex Prichard\\VSCodeProjects\\Python\\allBlue\\{dir}\\'
	directory = os.listdir(dir_name)
	for file in directory:
		os.remove(os.path.join(dir_name, file))


def s5(state: np.ndarray[int]) -> np.ndarray[int]:
	permutation = np.array([
		[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
	])
	return permutation.dot(state)


def s4(state: np.ndarray[int]) -> np.ndarray[int]:
	permutation = np.array([
		[0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
		[0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
		[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
		[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
		[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
		[0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
		[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
		[0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
	])
	return permutation.dot(state)


def hash_single_state(state: np.ndarray[int], num_colors: int = 2) -> int:
	acc = 0
	for node in state:
		acc *= num_colors
		acc += node
	return acc


def hash_state(state: np.ndarray[int]) -> int:
	hashes = []
	four_symmetry = state.copy()
	for i in range(4):
		four_symmetry = s4(four_symmetry)
		five_symmetry = four_symmetry.copy()
		for j in range(5):
			five_symmetry = s5(five_symmetry)
			hashes.append(hash_single_state(five_symmetry))
	return min(hashes)


def main():
	num_colors = 2
	dir = f'{num_colors}_graphs'
	edge_matrix = []
	with open('edgeMatrix.txt') as file:
		edge_matrix = file.read()
		edge_matrix = np.array([[int(elem) for elem in line.split(' ')] for line in edge_matrix.split('\n')])

	states = {}
	for state in compute_valid_states(edge_matrix, num_colors):
		state_hash = hash_state(state)
		if state_hash in states:
			continue
		states |= {state_hash: state.copy()}
	
	print(f'Found {len(states)} states.')
	state_values = list(states.values())
	clear_graph_directory(dir)
	for i, state in tqdm(enumerate(state_values)):
		create_graph(edge_matrix, state, f'graph_{i}', dir)
	clean_graph_directory(dir)

if __name__ == '__main__':
	main()
