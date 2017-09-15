import logging
import sys

def readNordicFile(f):
	nordics = []
	emsg = "Nordic Read: The following line is too short: {0}\n{1}"
	i = 0
	nordics.append([])
	
	for line in f:
		if line.strip() == "":
			i += 1;
			nordics.append([])
		elif(len(line) < 81):
			logging.error(emsg.format(len(line), line))
			sys.exit()
		elif (line[79] == "7"):
			pass
		elif (line[79] == " "):
			nordics[i].append(line)
		else:
			nordics[i].append(line)

	return nordics
