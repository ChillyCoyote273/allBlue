import numpy as np
import scipy as sp
import graphviz
import os


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

def compute_valid_states(edge_matrix: np.ndarray[int]) -> np.ndarray[int]:
	for num in range(2 ** 10):
		move_array = np.array([0] * 10)
		for idx in range(10):
			move_array[idx] = num % 2
			num >>= 1
		state = edge_matrix.dot(move_array) % 2
		yield state, move_array


def get_node_position(index: int):
	INNER_RADIUS = 1
	OUTER_RADIUS = 2
	angle = ((index % 5) * 0.4 + 0.5) * np.pi
	radius = INNER_RADIUS if index > 4 else OUTER_RADIUS
	x = radius * np.cos(angle)
	y = radius * np.sin(angle)
	return f'{-x}, {y}!'


def create_graph(edge_matrix, state, name='Petersen Graph'):
	graph = graphviz.Graph(name, directory='graphs', filename=f'{name}.dot', engine='neato', format='png')
	for i, vertex in enumerate(state):
		graph.node(f'{i}', f'{i}', color = 'red' if vertex == 1 else 'blue', pos = get_node_position(i))
	for i, row in enumerate(edge_matrix):
		for j, edge in enumerate(row):
			if i < j and edge == 1:
				graph.edge(f'{i}', f'{j}', constraint='false')
	graph.render()


def clean_graph_directory():
	dir_name = 'C:\\Users\\Alex Prichard\\VSCodeProjects\\Python\\allBlue\\graphs\\'
	directory = os.listdir(dir_name)
	for file in directory:
		if file.endswith('.dot'):
			os.remove(os.path.join(dir_name, file))


def rotate_state(state):
	


def main():
	edge_matrix = []
	with open('edgeMatrix.txt') as file:
		edge_matrix = file.read()
		edge_matrix = np.array([[int(elem) for elem in line.split(' ')] for line in edge_matrix.split('\n')])
	
	four_states = {}
	for state, moves in compute_valid_states(edge_matrix):
		state_string = get_flipped_nodes(state)
		if len(state_string) == 4 * 2:
			if state_string not in four_states:
				four_states |= {state_string: (state.copy(), moves.copy())}
	print(f'Found {len(four_states)} states with 4 blue nodes.')
	index = 0
	for state_string, state in four_states.items():
		create_graph(edge_matrix, state[0], f'graph_{index}')
		print(f'{index}: {" ".join([str(node) for node in state[1]])}, {state_string}')
		index += 1
	clean_graph_directory()

if __name__ == '__main__':
	main()
