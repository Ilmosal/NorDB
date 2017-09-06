#!/usr/bin/python
# coding=utf-8 

import sys
import string

def read_fix_nordicp_file(f, old_nordic):
	nordics = []
	whitespace = "                                                                                \n"
	if not old_nordic:
		i = 0
		data_reached = False
		nordics.append([])
		for line in f:	
			for char in range(0, len(line)):
				if line[char] == '\xc4':
					ls = list(line)
					ls[char] = 'A'
					line = "".join(ls)
			if (line[0] == '\n'):
				i += 1
				nordics.append([])
				data_reached = False
				for line in nordics[i-1]:
					if (len(line) < 80):
						print(nordics[i-1])
				continue
			if (len(line) < 81):
				line = line[:-1]
				for a in range(0, 80-len(line)):
					line += ' '
					line += '\n'
			if (line == "                                                                                \n"):
				i+=1
				nordics.append([])
				data_reached = False
				for line in nordics[i-1]:
						if (len(line) < 80):
							print(nordics[i-1])
				continue
			if (line[79] == '7'):
				continue
			if (line[79] == ' '):
				data_reached = True
			if (data_reached and line[79] != ' '):
				return nordics
			
			nordics[i].append(line)
	else:
		i = 0
		data_reached = False
		nordics.append([])
		comment = False
		for line in f:
			
			if data_reached and not comment :
				if is_comment(line):
					comment = True
					continue
			if not data_reached:
				if line.strip() == "":
					continue
				if comment:
					line = line[:-1]+ whitespace[(len(line)-1):-2] + "3\n"
					comment = False
				else: 
					line = line[:-2] + whitespace[(len(line)-2):-2] + "1\n"
				nordics[i].append(line)
				data_reached = True
			else:
				comment = True
				if line.strip() == "":
					data_reached = False
					comment = False
					nordics.append([])
					i += 1
					continue
				if len(line) > 71:
					line = line[:68] + line[69:71] + " " + line[71:]
				nordics[i].append(line[:-1]+ whitespace[(len(line)-1):])

	return nordics	

def is_comment(line):
	counter = 0
	for i in range(0, len(line)):
		if line[i].isalpha():
			counter += 1
		elif line[i] == ' ':
			counter = 0
		if counter > 4:
			return True

	return False
