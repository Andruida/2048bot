#!/usr/bin/python3

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
				


def equalize_number_length(num, length):
	num = str(num) if num != 0 else " "
	if len(num) >= length:
		return num
	else:
		return " "*(length - len(num)) + num
			
	
def render_game(board, length=6):
	txt = ""
	for row in board:
		# sor = [equalize_number_length(x, length) for x in row]
		txt += (" | ".join(["{"+str(x)+"}" for x in range(len(row))]).format(*[equalize_number_length(x, length) for x in row])) +" |\n"
		
	return txt + ""
	
	
if __name__ == "__main__":
	game = create_game()
	import os
	from getch import getch
	# height, width = os.popen('stty size', 'r').read().split()
	points = 0
	length = 5
	winCondition = False
	height, width = tuple(map(int, os.popen('stty size', 'r').read().split()))
	gamestr = "Points: 0\nThe greatest number: 0\n\n"
	gamestr += "-"*(length*BOARD_SIZE+4*(BOARD_SIZE-1)-1)
	gamestr += "\n"
	gamestr += render_game(game, length)
	gamestr += "-"*(length*BOARD_SIZE+4*(BOARD_SIZE-1)-1)
	gamestr += "\n"
	gamestr += "\n"*(height-(BOARD_SIZE+6))
	print(gamestr, end="")
	quitScreen = False
	while True:
		point = 0
		inp = getch()
		# print(inp, end="")
		if quitScreen:
			if inp == b'y':
				break
			elif inp == b'n':
				quitScreen = False
		else:
			if inp == b'w':
				game, _, point = move_up(game)
			elif inp == b's':
				game, _, point = move_down(game)
			elif inp == b'a':
				game, _, point = move_left(game)
			elif inp == b'd':
				game, _, point = move_right(game)
			elif inp == b'q' or inp == b'\x03':
				quitScreen = True
			else:
				# continue
				pass
		points += point
		over, win = is_over(game)
		height, width = tuple(map(int, os.popen('stty size', 'r').read().split()))
		if quitScreen == True:
			gamestr = "Do you want to leave this game? (y/n)\n"
			gamestr += "\n"*(height-2)
		else:
			gamestr = "Points: {0}\nThe greatest number: {1}\n\n".format(str(points)+(" (+"+str(point)+")" if point != 0 else ""), highest_number(game))
			gamestr += "-"*(length*BOARD_SIZE+4*(BOARD_SIZE-1)-1)
			gamestr += "\n"
			gamestr += render_game(game, length)
			gamestr += "-"*(length*BOARD_SIZE+4*(BOARD_SIZE-1)-1)
			gamestr += "\n"
			if (not over and not win) or (not over and win and winCondition):
				gamestr += "\n"*(height-(BOARD_SIZE+6))
			else:
				gamestr += "\n"
				if over and not win:
					gamestr += "There are no more valid moves!\n"
					gamestr += "Your score: {0} | Your greatest number: {1}\n".format(str(points), highest_number(game))
					gamestr += "\n"*(height-(BOARD_SIZE+6+2+2))
					print(gamestr, end="")
					break
				elif not over and win and not winCondition:
					gamestr += "Congratulations! You reached 2048! You can still play until there are no valid moves left.\n"
					gamestr += "\n"*(height-(BOARD_SIZE+4))
					winCondition = True
				elif over and win:
					gamestr += "There are no more valid moves! But don't worry, you've already won the game!\n"
					gamestr += "Your score: {0} | Your greatest number: {1}\n".format(str(points), highest_number(game))
					gamestr += "\n"*(height-(BOARD_SIZE+6+2+2))
					print(gamestr, end="")
					break
		print(gamestr, end="")
	print("Goodbye!", end="")
		
		
		
		
		
	