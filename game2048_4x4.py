import math
import random

random.seed()

BOARD_SIZE = 4

POWERS = [2**x for x in range(1, 30)]

def free_space(game):
	free = [0 in game[x] for x in range(BOARD_SIZE)]
	#print(free)
	if True in free:
		return True
	else:
		return False

def put_number_on_board(game, number=-1, x=-1, y=-1):
	if number < 0 or not number in POWERS:
		if random.randrange(10) == 4:
			number = 4
		else:
			number = 2
	if not free_space(game):
		return False
	if (x < 0 or x > 3) and (y < 0 or y > 3):
		loops = 0
		while True:
			loops += 1
			x = random.randrange(BOARD_SIZE)
			y = random.randrange(BOARD_SIZE)
			if game[y][x] == 0:
				break
			if loops >= BOARD_SIZE**2*10:
				return False
	game[y][x] = number # Nem
	return game
	

def highest_number(game):
	return max([max(row) for row in game])

	
def is_over(game):
	win = [2048 in game[x] for x in range(BOARD_SIZE)]
	winner = False
	over = False
	if True in win:
		#return True, True
		winner = True
	if not free_space(game):
		import copy
		gameCopy = copy.deepcopy(game)
		_, succes_r, _ = move_right(gameCopy)
		gameCopy = copy.deepcopy(game)
		_, succes_l, _ = move_left(gameCopy)
		gameCopy = copy.deepcopy(game)
		_, succes_d, _ = move_down(gameCopy)
		gameCopy = copy.deepcopy(game)
		_, succes_u, _ = move_up(gameCopy)
		if succes_r or succes_l or succes_d or succes_u:
			over = False
			#return False, None
		else:
			over = True
			#return True, False
	#else:
		#return False, None
	return over, winner
		
def vertical(game):
	verticalGame = [[0 for _ in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
	for y in range(BOARD_SIZE):
		for x in range(BOARD_SIZE):
			verticalGame[x][y] = game[y][x]
	game = verticalGame
	return game
	

def create_game():
	game = [[0 for _ in range(BOARD_SIZE)] for x in range(BOARD_SIZE)]
	for _ in range(2):
		# x = random.randrange(BOARD_SIZE)
		# y = random.randrange(BOARD_SIZE)
		# game[y][x] = random.choice([2, 4])
		put_number_on_board(game)
	return game
	
def move_left(game):
	 # // Phase 1: merge numbers
    # var col = -1;
    # var length = row.Count;
    # var modified = false;
    
    # for (var y = 0; y < length; y++)
    # {
        # if (row[y] == 0)
            # continue;
        # if (col == -1)
        # {
            # col = y; // remember current col
            # continue;
        # }
        # if (row[col] != row[y])
        # {
            # col = y; // update
            # continue;
        # }
        # if (row[col] == row[y])
        # {
            # row[col] += row[y]; // merge same numbers
            # row[y] = 0;
            # col = -1; // reset
            # modified = true;
        # }
    # }
    # // Phase 2: move numbers
    # for (var i = 0; i < length * length; i++)
    # {
        # var y = i % length;
        
        # if (y == length - 1) continue;
        # if (row[y] == 0 && row[y + 1] != 0) // current is empty and next is not 
        # {
            # row[y] = row[y + 1]; // move next to current
            # row[y + 1] = 0;
            # modified = true;
        # }
    # }
    # return modified;
	modified = False
	point = 0
	for row in game:
		col = -1
		for x in range(BOARD_SIZE):
			if row[x] == 0:
				continue
			if col == -1:
				col = x
				continue
			if row[col] != row[x]:
				col = x
				continue
			if row[col] == row[x]:
				row[col] += row[x]
				point += row[col]
				row[x] = 0
				col = -1
				modified = True
		for i in range(BOARD_SIZE**2):
			x = i % BOARD_SIZE
			
			if x == BOARD_SIZE-1:
				continue
			if row[x] == 0 and row[x+1] != 0:
				row[x] = row[x+1]
				row[x+1] = 0
				modified = True
	if modified:
		put_number_on_board(game)
	return game, modified, point


def move_right(game):
	modified = False
	point = 0
	for row in game:
		col = -1
		for x in range(BOARD_SIZE-1, -1, -1):
			if row[x] == 0:
				continue
			if col == -1:
				col = x
				continue
			if row[col] != row[x]:
				col = x
				continue
			if row[col] == row[x]:
				row[col] += row[x]
				point += row[col]
				row[x] = 0
				col = -1
				modified = True
		for i in range(BOARD_SIZE**2-1, -1, -1):
			x = i % BOARD_SIZE
			
			if x == 0:
				continue
			if row[x] == 0 and row[x-1] != 0:
				row[x] = row[x-1]
				row[x-1] = 0
				modified = True
	if modified:
		put_number_on_board(game)
	return game, modified, point
	
def move_up(game):
	game = vertical(game)
	game, modified, point = move_left(game)
	game = vertical(game)
	return game, modified, point
	
def move_down(game):
	game = vertical(game)
	game, modified, point = move_right(game)
	game = vertical(game)
	return game, modified, point
				


def print_game(game):
	print("\n\n")
	for row in game:
		print("  ".join(["{"+str(x)+"}" for x in range(BOARD_SIZE)]).format(*row))
	
	
if __name__ == "__main__":
	game = create_game()
	print_game(game)
	for _ in range(10):
		game, _ = move_down(game)
		#print_game(game)
	print_game(game)
	game = vertical(game)
	print_game(game)
	game = vertical(game)
	print_game(game)
	