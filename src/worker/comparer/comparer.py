import sys

class compare:
	def __init__(self,user_file_loc,correct_file_loc):
		# Read user's output 
		self.user_output_file = user_file_loc
		self.user_output = open(self.user_output_file).read()
		# Read correct output
		self.correct_output_file = correct_file_loc
		self.correct_output = open(self.correct_output_file).read()
	#returns either 0 or 1 based on 
	#if outputs match with the ignore_
	#chars removed
	def compare_binary_ignore_chars(self,ignore_chars=""):	
		user_out = self.user_output
		corr_out = self.correct_output
		for i in ignore_chars:
			user_out.replace(i,'')
			corr_out.replace(i,'')
		if(user_out == corr_out):
			return 1.0
		return 0.0
	#Checks if ith line matches
	#returns a score from 0..1 based on % match
	def compare_partial_lines_match(self):
		user_out = self.user_output
		corr_out = self.correct_output
		user_out_lines = user_out.split("\n")
		corr_out_lines = corr_out.split("\n");
		totlines = len(corr_out_lines)
		corrlines = 0
		minlines = min(len(corr_out_lines),len(user_out_lines))
		for i in range(minlines):
			if(user_out_lines[i] == corr_out_lines[i]):
				corrlines += 1
		return float(corrlines)/totlines
	#Returns best possible line match score
	def compare_partial_lines_best_match(self):
		user_out = self.user_output
		corr_out = self.correct_output
		user_out_lines = user_out.split("\n")
		corr_out_lines = corr_out.split("\n");
		totlines = len(corr_out_lines)
		corrlines = 0
		LCS = {}
		LCS[(-1,-1)] = 0
		LCS[(-1,0)] = 1
		LCS[(0,-1)] = 1
		while i < len(corr_out_lines):
			while j < len(user_out_lines):
				if(corr_out_lines[i] == user_out_lines[i]):
					LCS[(i,j)] = LCS[(i-1,j-1)] + 1
				else:
				 	LCS[(i,j)] = 1 + min(LCS[(i-1,j)],LCS[(i,j-1)])
		return float(LCS[len(corr_out_lines)-1][len(user_out_lines)-1])/len(corr_out_lines)

