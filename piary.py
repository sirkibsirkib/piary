import glob
import os
import math
import time
import sys
import datetime
from dicts import *
from grid import Grid
from copy import deepcopy


PREV_N_DAYS = 40
NEXT_N_DAYS = 10
DRAW_H = 14


def del_line(filename):
	file = open(filename, "r+", encoding = "utf-8")
	#Move the pointer (similar to a cursor in a text editor) to the end of the file. 
	file.seek(0, os.SEEK_END)
	#This code means the following code skips the very last character in the file - 
	#i.e. in the case the last line is null we delete the last line 
	#and the penultimate one
	pos = file.tell() - 1
	#Read each character in the file one at a time from the penultimate 
	#character going backwards, searching for a newline character
	#If we find a new line, exit the search
	while pos > 0 and file.read(1) != "\n":
		pos -= 1
		file.seek(pos, os.SEEK_SET)
	#So long as we're not at the start of the file, delete all the characters ahead of this position
	if pos > 0:
		file.seek(pos-1, os.SEEK_SET)
		file.truncate()
		file.close()
	else:
		file.close()
		os.remove(filename)
	

def print_vis(y, m, d, now_tuple):
	g = Grid(87, DRAW_H, default=' ')
	for _ in range(NEXT_N_DAYS):
		y,m,d = next_date(y,m,d)
	days_backward = 0
	while days_backward < PREV_N_DAYS:
		x_write = (PREV_N_DAYS-days_backward) * 2
		g.set(x_write, DRAW_H-6, '^') 
		g.set(x_write+1, DRAW_H-6, '-') 
		g.write_at(x_write, DRAW_H-(4 if days_backward%2==0 else 5), '{:02d}'.format(d))
		if d == 1:
			g.write_at(x_write, DRAW_H-3, month_name[m-1])
			g.stripe_up(x_write-1, DRAW_H-6, DRAW_H-4, char='|')
		fname = filename_for(y,m,d)
		if (y,m,d) == now_tuple:
			g.write_at(x_write, DRAW_H-2, '^TODAY')
		try:
			stat_info = os.stat(fname)
			draw_height = int(stat_info.st_size**0.2)
			g.stripe_up(x_write, DRAW_H-7, draw_height, char='#')
		except: pass
		y,m,d = prev_date(y,m,d)
		days_backward += 1
	g.set(60,DRAW_H-6, '@')
	g.set(60,0, '@')
	g.print_grid()




def prev_date(y,m,d):
	d2 = d-1
	m2 = m
	y2 = y
	if d2 == 0:
		m2 = m-1
		if m2 == 0:
			m2 = 12
			y2 = y-1
		d2 = last_day(m2, y2)
	return y2,m2,d2
	
def next_date(y,m,d):
	d2 = d+1
	m2 = m
	y2 = y
	if d2 > last_day(m2,y2):
		d2 = 1
		m2 += 1
		if m2 > 12:
			y2 += 1
			m2 = 1
	return y2, m2, d2

def leap(year): return year%4 == 0

def last_day(month, year):
	if month == 2:
		return 29 if leap(year) else 28
	else:
		return months_last_day[month]
		
def filename_for(y,m,d):
	if not os.path.exists('entries'):
		os.makedirs('entries')
	f = '{:04d}_{:02d}_{:02d}.txt'.format(y, m, d)
	return os.path.join('entries', f)
	
now = datetime.datetime.now()
now_tuple = (now.year, now.month, now.day)
y,m,d = deepcopy(now_tuple)
while True:
	os.system('cls')
	selected_filename = filename_for(y,m,d)
	was_text = False
	print('Enter new text line(s) to append to today\'s entry. CTRL+C to end')
	print('Enter commands as `/<command>` from {prev, next, today, rmln}')
	print_vis(y, m, d, now_tuple)
	try:
		with open(selected_filename, 'r') as f:
		
			print('Current entry for today ({}-{}-{}) so far:'.format(y, month_name[m-1], d))
			for ln in f:
				print('::  '+ln.strip())
		was_text = True
	except:
		print('No entry yet for today ({}-{}-{}):'.format(y, month_name[m-1], d))
	sys.stdout.write('::  ')
	try:
		text_in = input().strip()
	except KeyboardInterrupt:
		print('\nSee you tomorrow!')
		exit(0)
		
	
	if text_in:
		# non-empty input
		if text_in.startswith('/'):
			# command input
			success = True
			if text_in == 't':
				y,m,d = now.year, now.month, now.day
				print('going to today day!')
			elif text_in == 'prev' or text_in == '/p':
				y,m,d = prev_date(y,m,d)
				print('going to previous day!')
			elif text_in == 'next' or text_in == '/n':
				y,m,d = next_date(y,m,d)
				print('going to next day!')
			elif text_in[1:] == 'rmln' or text_in == 'r':
				del_line(selected_filename)
				print('deleting last line!')
				
			
		else:
			# diary entry input
			with open(selected_filename, 'a') as f:
				f.write(('\n' if was_text else '')+text_in)