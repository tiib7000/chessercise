import argparse

class Position:
	def __init__(self, line, column):
		self.line = line
		self.column = column
	
	def north(self):
		self.line += 1

	def south(self):
		self.line -= 1

	def west(self):
		self.column -= 1

	def east(self):
		self.column += 1

	def ne(self):
		self.north()
		self.east()

	def nw(self):
		self.north()
		self.west()

	def se(self):
		self.south()
		self.east()

	def sw(self):
		self.south()
		self.west()

	def validate(self):
		return self.line >= 0 and self.line <= 7 and \
			self.column >= 0 and self.column <= 7

	def __str__(self):
		return str("Position " + chr(self.line + ord('1')) + " " + chr(self.column+ord('a')))

	@staticmethod
	def parse(s):
		return Position(ord(s[1])-ord('1'), ord(s[0])-ord('a'))

class Step:
	REPEAT_MAX=8
	REPEAT_MIN=1
	REPEAT_WILDCARD=0

	def __init__(self, direction, repeat):
		self.direction = direction
		self.repeat = repeat

	def apply(self, positions):
		newPositions = []
		for p in positions:
			newPosition = Position(p.line, p.column)
			if self.repeat >= Step.REPEAT_MIN and self.repeat <= Step.REPEAT_MAX:
				for i in range(self.repeat):
					self.direction(newPosition)
				newPositions.append(newPosition)
			elif self.repeat == Step.REPEAT_WILDCARD:
				for i in range(Step.REPEAT_MIN, Step.REPEAT_MAX):
					self.direction(newPosition)
					clone = Position(newPosition.line, newPosition.column)
					newPositions.append(clone)
		return newPositions

class Move:
	def __init__(self, steps):
		self.steps = steps

	def apply(self, position):
		validPositions = [position]
		for s in self.steps:
			positions = s.apply(validPositions)
			validPositions = []
			for p in positions:
				if p.validate():
					validPositions.append(p)
		return validPositions

class Piece:
	moves=()

	def __init__(self, position):
		self.position = position

	@staticmethod
	def factory(type, position):
		if type == 'Pawn': return Pawn(position)
		if type == 'Queen': return Queen(position)
		if type == 'Rook': return Rook(position)
		if type == 'Knight': return Knight(position)
		assert 0, "Bad piece type: " + type


class Pawn(Piece):
	moves = (Move((Step(Position.north,1),)),\
		 Move((Step(Position.north,2),)),\
		)

	def __str__(self):
		return str("Pawn " + str(self.position))


class Queen(Piece):
	moves = (\
		Move((Step(Position.north,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.south,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.east,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.west,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.ne,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.se,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.sw,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.nw,Step.REPEAT_WILDCARD),)),\
		)

	def __str__(self):
		return str("Queen " + str(self.position))


class Rook(Piece):
	moves = (\
		Move((Step(Position.north,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.south,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.east,Step.REPEAT_WILDCARD),)),\
		Move((Step(Position.west,Step.REPEAT_WILDCARD),)),\
		)

	def __str__(self):
		return str("Rook " + str(self.position))


class Knight(Piece):
	moves = (\
		Move((Step(Position.north,1),Step(Position.west,2),)),\
		Move((Step(Position.north,1),Step(Position.east,2),)),\
		Move((Step(Position.south,1),Step(Position.west,2),)),\
		Move((Step(Position.south,1),Step(Position.east,2),)),\
		Move((Step(Position.north,2),Step(Position.west,1),)),\
		Move((Step(Position.north,2),Step(Position.east,1),)),\
		Move((Step(Position.south,2),Step(Position.west,1),)),\
		Move((Step(Position.south,2),Step(Position.east,1),)),\
		)

	def __str__(self):
		return str("Knight " + str(self.position))

parser = argparse.ArgumentParser()
parser.add_argument("-piece", help="Type of chess piece (Queen, Rook, Knight)", required=True)
parser.add_argument("-position", help="Current position on a chess board (for example: d2)", required=True)
parser.parse_args()
args = parser.parse_args()

pos = Position.parse(args.position)
#print(pos)

piece = Piece.factory(args.piece, pos)
#print(piece)

#pos.north()
#print(pos)

#b = pos.validate()

#print(b)

for m in piece.moves:
#	print(m)
#	for s in m.steps:
#		print(s)
	positions = m.apply(piece.position)
	if positions != None:
		for p in positions:
			print(p)








