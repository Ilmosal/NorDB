#!/usr/bin/python
# -*- coding: ascii -*-

import math

def get93Value(char):
	i = ord(char)-33
	if i >= 0 and i <= 93:
		return i
	else:
		return -9

def getString93Value(string):
	value = 0
	for x in xrange(0,len(string)):
		value += get93Value(string[x]) * math.pow(93, len(string) - x - 1)
	return int(value)

def get93Char(value):
	return str(unichr(33+value))

def get93String(value):
	x = 1
	string = ""

	while value != 0:
		if math.pow(93,x) >= value:
			x -= 1
			i = int(math.floor(value/math.pow(93, x)))
			string += get93Char(i)
			value -= i * math.pow(93, x)
			x = 0
		else:
			x += 1
		
	return string

def getEventIndices(string):
	string = string.split("!")
	
	events = []
	for s in string:
		events.append(getString93Value(s))

	return events

def getEventString(events):
	string = ""
	for e in events:
		string += get93String(e) + "!"
	
	return string[:-1]

