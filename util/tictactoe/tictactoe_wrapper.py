class tictactoe_wrapper:

	def __init__(self, board, players):
		self.__board = board

		self.__players = players
		self.__current_player = players[0]

	def do_turn(self, place):
		self.__current_player.play_turn(self.__board, place)

	def is_winning(self):
		self.__board.has_winning_state(self.__current_player.symbol)

	def switch_player(self):
		self.__current_player = self.__players[(self.__players.index(self.__current_player) + 1) % len(self.__players)]

	@property
	def board(self):
		return self.__board

	@property
	def players(self):
		return self.__players

	@property
	def current_player(self):
		return self.__current_player