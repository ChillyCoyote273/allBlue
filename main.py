import numpy as np
import scipy as sp


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

def compute_valid_states(edge_matrix: np.ndarray[int]) -> "list[np.ndarray[int]]":
	states = []
	for num in range(2 ** 10):
		move_array = np.array([0] * 10)
		for idx in range(10):
			move_array[idx] = num % 2
			num >> 1
		state = edge_matrix.dot(move_array) % 2
		states.append(state)
	return states

def main():
	#                 0  1  2  3  4  5  6  7  8  9
	# moves = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
	edge_matrix = []
	with open('edgeMatrix.txt') as file:
		edge_matrix = file.read()
		edge_matrix = np.array([[int(elem) for elem in line.split(' ')] for line in edge_matrix.split('\n')])
	while True:
		(moves, should_break) = get_moves_from_string(input('Enter a sequence of moves: '))
		if should_break: 
			break
		state = edge_matrix.dot(moves) % 2
		print(f'Flipped nodes: {get_flipped_nodes(state)}')
		with open("graph.dot", "w") as file:
			file.write("digraph G {\n")
			node_counter = 0
			for i, node in enumerate(state):
				if node == 1:
					file.write(f'{i} [color="red"]\n')
				else:
					file.write(f'{i} [color="blue"]\n')
			for i, row in enumerate(edge_matrix):
				for j, elem in enumerate(row):
					if i <= j:
						continue
					if elem == 1:
						file.write(f"{i} -> {j} [dir=none]\n")
			file.write("}\n")
	for state in compute_valid_states(edge_matrix):
		if len(get_flipped_nodes(state)) == 4:
			print(f"Found state with 2 nodes flipped: {get_flipped_nodes(state)}")
if __name__ == '__main__':
	main()
