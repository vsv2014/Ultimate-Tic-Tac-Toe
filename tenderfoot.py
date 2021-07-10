import random
import time

class Tenderfoot():

	def __init__(self):
		self.INF 	= 1000000
		self.depth 	= 3
		self.ply 	= {}
		self.normal_weights = [1, 9, 90, 900, 9000]
		self.winning_comb = []
		self.tlimit = 14
		for i in range(4):
			comb = []
			for j in range(4):
				comb.append((i, j))
			self.winning_comb.append(comb)

		for j in range(4):
			comb = []
			for i in range(4):
				comb.append((i, j))
			self.winning_comb.append(comb)

		comb = [(1, 2), (2, 1), (2, 3), (3, 2)]
		self.winning_comb.append(comb)
		comb = [(1, 1), (2, 0), (2, 2), (3, 1)]
		self.winning_comb.append(comb)
		comb = [(0, 2), (1, 1), (1, 3), (2, 2)]
		self.winning_comb.append(comb)
		comb = [(0, 1), (1, 0), (1, 2), (2, 1)]
		self.winning_comb.append(comb)

	def move(self, board, old_move, flag):

		# if old_move == (-1, -1):
		# 	return (4, 4)

		if flag == "x":			
			self.ply["max"]	= "x"
			self.ply["min"] = "o"
		else:
			self.ply["max"] = "o"
			self.ply["min"] = "x"

		self.cntp  = sum(blocks.count(self.ply["max"]) for blocks in board.block_status)
		self.cnto  = sum(blocks.count(self.ply["min"]) for blocks in board.block_status)
		self.stime = time.time()
		self.depth = 3

		max_move = (-1, -1)

		while time.time() - self.stime < self.tlimit:
			score,move,valid = self.minimax(board, self.depth, -self.INF, self.INF, old_move, True, False)
			print('valid --> ', valid, 'depth --> ',self.depth, 'time--> ',time.time() - self.stime)
			if valid == 1:
				max_move = move
			self.depth += 1

		if max_move == (-1, -1):
			return random.choice(board.find_valid_move_cells())

		return max_move


	def minimax(self, board, depth, alpha, beta, old_move, is_max_ply, is_pre_bonus):

		terminal_status = board.find_terminal_state()
		if depth == 0 or terminal_status != ('CONTINUE', '-'):
			return (self.heuristic(board, self.ply["max"]), old_move, 1)

		moves = board.find_valid_move_cells(old_move)

		if is_max_ply:
			max_score = -self.INF
			max_move  = (-1,-1)
			for mv in moves:

				if time.time() - self.stime > self.tlimit:
					return (-1, (-1, -1), 0)

				board.update(old_move, mv, self.ply["max"])
				
				flag = False
				bonus = False
				if board.block_status[mv[0]/4][mv[1]/4] == self.ply["max"]:
					if is_pre_bonus == False:
						flag = True
						bonus = True

				tupl = self.minimax(board, depth-1, alpha, beta, mv, flag, bonus)

				board.block_status[mv[0]/4][mv[1]/4]= '-'
				board.board_status[mv[0]][mv[1]] 	= '-'

				if tupl[2] == 0:
					return (-1, (-1, -1), 0)

				score = tupl[0]

				alpha = max(alpha,score)
				if(max_score < score):
					max_score = score
					max_move = mv
				if(alpha > beta):
					break
				
			return (max_score, max_move, 1)

		else:
			min_score = self.INF
			min_move = (-1,-1)
			for mv in moves:

				if time.time() - self.stime > self.tlimit:
					return (-1, (-1, -1), 0)

				board.update(old_move, mv, self.ply["min"])

				flag = True
				bonus = False
				if board.block_status[mv[0]/4][mv[1]/4] == self.ply["min"]:
					if is_pre_bonus == False:
						flag = False
						bonus = True

				tupl = self.minimax(board,depth-1,alpha,beta,mv,flag,bonus)

				board.block_status[mv[0]/4][mv[1]/4]= '-'
				board.board_status[mv[0]][mv[1]] 	= '-'

				if tupl[2] == 0:
					return (-1, (-1, -1), 0)

				score = tupl[0]

				beta = min(beta,score)
				if(min_score > score):
					min_score = score
					min_move  = mv
				if(alpha > beta):
					break
				
			return (min_score, min_move, 1)

	def heuristic(self, board, flag):

		board_prob = [[0 for i in range(4)] for j in range(4)]
		for i in range(4):
			for j in range(4):
				board_prob[i][j] = self.find_prob_cells(board.board_status, 4*i, 4*j)
		prob = self.find_prob_block(board.block_status, board_prob)

		cnt1 = sum(blocks.count(self.ply["max"]) for blocks in board.block_status)
		cnt2 = sum(blocks.count(self.ply["min"]) for blocks in board.block_status)
		if self.cntp < cnt1 and cnt2 == self.cnto:
			prob += 50
		elif cnt1 > self.cntp and (cnt1 - self.cntp) < (cnt2 - self.cnto):
			prob -= 20
		elif cnt1 < self.cntp and cnt2 > self.cnto:
			prob -= 50

		return prob

	def find_prob_cells(self, block_status, topx, topy):

		prob = 0
		for comb in self.winning_comb:
			pCount = 0
			oCount = 0
			comb_status = [block_status[topx + x][topy + y] for (x, y) in comb]

			pCount = comb_status.count(self.ply["max"])
			oCount = comb_status.count(self.ply["min"])

			if (pCount == 0 and oCount > 0):
				prob -= pow(10,oCount-1)
			elif (pCount == 1 and oCount == 3):
				prob += pow(10,2)
			elif (oCount == 0 and pCount):
				prob += pow(10,pCount-1)
		return prob/1000.0

	def find_prob_block(self, board_status, board_prob):

		prob = 0
		for comb in self.winning_comb:
			pCount = 0
			oCount = 0
			combProb = 0
			comb_status = [board_status[x][y] for (x, y) in comb]
			pCount = comb_status.count(self.ply["max"])
			oCount = comb_status.count(self.ply["min"])
			combProb = sum([board_prob[x][y] for (x, y) in comb])
			prob = self.normalize(combProb, prob)
			if (pCount == 0 and oCount > 0):
				prob -= pow(10,oCount)
			elif (pCount == 1 and oCount == 3):
				prob += pow(10,3)
			elif (oCount == 0 and pCount):
				prob += pow(10,pCount)

		return prob

	def normalize(self, p_gain, gain):
		sign = 1
		p_abs = abs(p_gain)
		idx = int(p_abs)
		if idx > 4:
			idx = 4
		if p_gain < 0:
			sign = -1
		frac_part = p_abs - idx
		weight = self.normal_weights[idx]
		gain += sign * (weight * frac_part + int(weight / 9))
		return gain