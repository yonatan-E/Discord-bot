class tictactoe_board:

	WINNING_STATES = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

	def __init__(self):
		self.__board = [''] * 9

	def __getitem__(self, place):
		if place - 1 not in range(0, len(self.__board)):
			raise IndexError(f'Place {place} is not in range.')

		return self.__board[place - 1]

	def __setitem__(self, place, symbol):
		if self[place]:
			raise IndexError(f'Place {place} is already taken.')

		self.__board[place - 1] = symbol

	def __len__(self):
		return len(self.__board)

	def has_winning_state(self, symbol):
		for state in self.WINNING_STATES:
			if len([place for place in state if self.__board[place] == symbol]) == len(state):
				return True
		return False

	def is_full(self):
		return '' not in self.__board