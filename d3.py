import random
import copy
import math

INF=float("inf")

class Player24():
	def __init__(self):
		pass

	def evaluate(self,board,block,flag):
		first=[[0 for p in range(4)] for q in range(4)]
		second=[[0 for p in range(4)] for q in range(4)]
		came=0
		for i in range(0,4):
			for j in range(0,4):
				came=0
				if block[i][j]=='-':
					came=1
					smallblock=[['-' for p in range(4)] for q in range(4)]
					for l in range(4*i,4*i+4):
						for m in range(4*j,4*j+4):
							smallblock[l-4*i][m-4*j]=board[l][m]
				if flag=='x':
					if came==1:
						first[i][j]=self.findprobabilities(smallblock,'x')
						second[i][j]=self.findprobabilities(smallblock,'o')
				else:
					if came==1:
						first[i][j]=self.findprobabilities(smallblock,'o')
						second[i][j]=self.findprobabilities(smallblock,'x')
				if came==0:
					if block[i][j]==flag:
						first[i][j]=1
						second[i][j]=0
					elif block[i][j]!='-':
						second[i][j]=1
						first[i][j]=0

				if first[i][j]==1:
					second[i][j]=0
				if second[i][j]==1:
					first[i][j]=0
		# print('#############################')
		# print('Print Board Max')
		# for i in range(4):
		# 	for j in range(4):
		# 		print first[i][j],
		# 	print
		# print('#############################')
		# print('#############################')
		# for i in range(0,4):
		# 	for j in range(0,4):
		# 		prob=0.5
		# 		if block[i][j]==flag:
		# 			first[i][j]=first[i][j]*1
		# 		elif block[i][j]!='-':
		# 			first[i][j]=first[i][j]*prob
		# 		else:
		# 			first[i][j]=0

		# for i in range(0,4):
		# 	for j in range(0,4):
		# 		prob=0.5
		# 		if block[i][j]!=flag:
		# 			second[i][j]=second[i][j]*1
		# 		elif block[i][j]!='-':
		# 			second[i][j]=second[i][j]*prob
		# 		else:
		# 			second[i][j]=0

		# first=self.calculate_wrt_block_status(first,second,block,flag,f1)
		# second=self.calculate_wrt_block_status(first,second,block,flag)
		present=self.findheuristic(first)
		opponent=self.findheuristic(second)
		return present-opponent

	def findprobabilities(self,smallblock,flag):
		value=[[0 for p in range(4)] for q in range(4)]
		for i in range(0,4):
			for j in range(0,4):
				if smallblock[i][j]==flag:
					value[i][j]=1
				elif smallblock[i][j]=='-':
					value[i][j]=0.5
				else:
					value[i][j]=0
		heuristic_value=self.findheuristic(value)
		return heuristic_value

	def findheuristic(self,value):
		# heuristic=[0,0,0,0,0,0,0,0,0,0]
		heuristic=[0,0,0,0,0,0,0,0,0,0,0,0]
		count=0
		for i in range(0,4):
			p=1
			for j in range(0,4):
				p=p*value[i][j]
			heuristic[count]=p
			count+=1

		for j in range(0,4):
			p=1
			for i in range(0,4):
				p=p*value[i][j]
			heuristic[count]=p
			count+=1

		# heuristic[8]=value[0][0]*value[1][1]*value[2][2]*value[3][3]
		# heuristic[9]=value[0][3]*value[1][2]*value[2][1]*value[3][0]
		heuristic[8]=value[1][2]*value[2][1]*value[2][3]*value[3][2]
		heuristic[9]=value[1][1]*value[2][0]*value[2][2]*value[3][1]
		heuristic[10]=value[0][2]*value[1][1]*value[1][3]*value[2][2]
		heuristic[11]=value[0][1]*value[1][0]*value[1][2]*value[2][1]

		flag1=0
		heuristic_value_avg=0
		for i in range(0,12):
			if heuristic[i]==1:
				flag1=1
			heuristic_value_avg+=heuristic[i]

		if flag1==1:
			return 1
		else:
			heuristic_value_avg=heuristic_value_avg/12
			return heuristic_value_avg

	def move(self, board, old_move, flag):
		#You have to implement the move function with the same signature as this
		#Find the list of valid cells allowed
		#cells = board.find_valid_move_cells(old_move)
		# print " move"
		[a,b,val]=self.dfs(board,0,old_move,flag,flag,-INF,INF,-1,-1)
		return a,b
		#return cells[random.randrange(len(cells))]

	def dfs(self,board,depth,old_move,flag,original_flag,alpha,beta,best_row,best_col):
		# print old_move

		if depth==3:
			# print board.block_status
			# print('#############################')
			# print('Print complete board')
			# board.print_board()
			# print('#############################')
			# print('#############################')
			val=self.evaluate(board.board_status,board.block_status,original_flag)
		#	val=self.evaluate(board.board_status,original_flag)
			return best_row,best_col,val
		#val=[]
		count=0
		# children=self.find_valid_cells(board.block_status,board.board_status,old_move)
		children = board.find_valid_move_cells(old_move)
		# print('#############')
		# print('Printing children')
		# print(children)
		# print('#############')
		# print('#############')
		if len(children)==0:
			val=self.evaluate(board.board_status,board.block_status,original_flag)
		#	val=self.evaluate(board.board_status,original_flag)
			return old_move[0],old_move[1],val
		#print old_move
		#best_move=children[0]
		# if flag=='o':
		# 	flag='x'
		# else:
		# 	flag='o'
		for x in children:
		# 	board.block_status[x[0]][x[1]]=flag
			copy_block_status = [['-' for i in range(4)] for j in range(4)]
			for i in range(0,4):
				for j in range(0,4):
					copy_block_status[i][j]=board.block_status[i][j]

			board.board_status[x[0]][x[1]]=flag

		 	board.block_status=self.updateboardstatus(board.block_status,board.board_status,x,flag)
			if flag=='o':
				util=self.dfs(board,depth+1,x,'x',original_flag,alpha,beta,best_row,best_col)
			else:
				util=self.dfs(board,depth+1,x,'o',original_flag,alpha,beta,best_row,best_col)
			utility=util[2]
			#print move,utility
			if depth%2==1 and utility<beta:
				beta=utility
				best_row=x[0]
				best_col=x[1]
			elif depth%2==0 and utility>alpha:
				alpha=utility
				best_row=x[0]
				best_col=x[1]

			board.board_status[x[0]][x[1]]='-'

			for i in range(0,4):
				for j in range(0,4):
					board.block_status[i][j]=copy_block_status[i][j]
			if alpha>=beta:
				break
		#print best_move
		if depth==0:
			if best_row==-1 or best_col==-1:
				best_row=children[0][0]
				best_col=children[0][1]
		if depth%2==0:
			return best_row,best_col,alpha
		else:
			return best_row,best_col,beta

	def updateboardstatus(self,block_status,board_status,move,flag):
		#board_status[move[0]][move[1]]=flag
		row=move[0]/4
		col=move[1]/4
		ans=0
		for i in range(0,4):
			c=0
			for j in range(0,4):
				if board_status[4*row+i][4*col+j]==flag:
					c+=1
			if c==4:
				ans=1
		for j in range(0,4):
			c=0
			for i in range(0,4):
				if board_status[4*row+i][4*col+j]==flag:
					c+=1
			if c==4:
				ans=1
		c=0
		for i in range(0,4):
			if board_status[4*row+i][4*col+i]==flag:
				c+=1
		if c==4:
			ans=1
		c=0
		for i in range(0,4):
			if board_status[4*row+i][4*col+3-i]==flag:
				c+=1
		if c==4:
			ans=1
		if ans==1:
			block_status[row][col]=flag
		return block_status

	def find_valid_cells(self,block_status,board_status,old_move):
		#returns the valid cells allowed given the last move and the current board state
		allowed_cells = []
		allowed_block = [old_move[0]%4, old_move[1]%4]
		#checks if the move is a free move or not based on the rules
		if old_move != (-1,-1) and block_status[allowed_block[0]][allowed_block[1]] == '-':
			for i in range(4*allowed_block[0], 4*allowed_block[0]+4):
				for j in range(4*allowed_block[1], 4*allowed_block[1]+4):
					if board_status[i][j] == '-':
						allowed_cells.append((i,j))
		else:
			for i in range(16):
				for j in range(16):
					if board_status[i][j] == '-' and block_status[i/4][j/4] == '-':
						allowed_cells.append((i,j))
		return allowed_cells
