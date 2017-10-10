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
		north(self)
		east(self)

	def nw(self):
		north(self)
		west(self)

	def se(self):
		south(self)
		east(self)

	def sw(self):
		south(self)
		west(self)

	def validate(self):
		return self.line >= 0 and self.line <= 7 and \
			self.column >= 0 and self.column <= 7

	def __str__(self):
		return str("Position " + chr(self.line + ord('1')) + " " + chr(self.column+ord('a')))

	def parse(s):
		return Position(ord(s[1])-ord('1'), ord(s[0])-ord('a'))
	parse = staticmethod(parse)

class Step:
	COUNTER_MAX=7
	COUNTER_MIN=1
	COUNTER_WILDCARD=0

	def __init__(self, direction, counter):
		self.direction = direction
		self.counter = counter

	def apply(self, positions):
		newPositions = []
		for p in positions:
			newPosition = Position(p.line, p.column)
			for i in range(self.counter):
				self.direction(newPosition)
			newPositions.append(newPosition)
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

	def factory(type, position):
		if type == 'Pawn': return Pawn(position)
		assert 0, "Bad piece type: " + type
	factory = staticmethod(factory)


class Pawn(Piece):
	moves = (Move((Step(Position.north,1),)),\
		 Move((Step(Position.north,2),)),\
		)

	def __str__(self):
		return str("Pawn " + str(self.position))


class Queen(Piece):
	moves = (\
		Move((Step(Position.north,1),)),\
		Move((Step(Position.south,1),)),\
		Move((Step(Position.east,1),)),\
		Move((Step(Position.west,1),)),\
		Move((Step(Position.ne,1),)),\
		Move((Step(Position.se,1),)),\
		Move((Step(Position.sw,1),)),\
		Move((Step(Position.nw,1),)),\
		)

	def __str__(self):
		return str("Queen " + str(self.position))

parser = argparse.ArgumentParser()
parser.add_argument("-piece", help="Type of chess piece (Queen, Rook, Knight)", required=True)
parser.add_argument("-position", help="Current position on a chess board (for example: d2)", required=True)
parser.parse_args()
args = parser.parse_args()

pos = Position.parse(args.position)
print(pos)

piece = Piece.factory(args.piece, pos)
print()

pos.north()
print(pos)

b = pos.validate()

print(b)
for m in piece.moves:
	print(m)
	for s in m.steps:
		print(s)
	positions = m.apply(piece.position)
	if positions != None:
		for p in positions:
			print(p)








