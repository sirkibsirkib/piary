import glob
import os
import math
import time
import sys
import errno
import datetime
from dicts import *
from config import *
from grid import Grid
from copy import deepcopy
import pyperclip
import git

PREV_N_DAYS = 36
NEXT_N_DAYS = 10
DRAW_H = 17
DRAW_W = (PREV_N_DAYS+NEXT_N_DAYS)*2 + 20


def del_line(filename):
	file = open(filename, "r+", encoding = "utf-8")
	#Move the pointer (similar to a cursor in a text editor) to the end of the file. 
	file.seek(0, os.SEEK_END)
	#This code means the following code skips the very last character in the file - 
	#i.e. in the case the last line is null we delete the last line 
	#and the penultimate one
	pos = file.tell()
	#Read each character in the file one at a time from the penultimate 
	#character going backwards, searching for a newline character
	#If we find a new line, exit the search
	deleted = ''
	
	if pos > 0:
		r = file.read(1)
		deleted = r + deleted
	while pos > 0 and r != "\n":
		pos -= 1
		
		file.seek(pos, os.SEEK_SET)
		r = file.read(1)
		deleted = r + deleted
	#So long as we're not at the start of the file, delete all the characters ahead of this position
	if pos > 0:
		file.seek(pos-1, os.SEEK_SET)
		file.truncate()
		file.close()
	else:
		file.close()
		os.remove(filename)
	return deleted
	

def print_vis(y, m, d, wd, now_tuple):
	g = Grid(DRAW_W, DRAW_H, default=' ')
	for _ in range(NEXT_N_DAYS):
		y,m,d,wd = next_date(y,m,d,wd)
	days_backward = -NEXT_N_DAYS
	g.stripe_up(PREV_N_DAYS*2, DRAW_H-1, DRAW_H, char=':')
	while days_backward < PREV_N_DAYS:
		x_write = (PREV_N_DAYS-days_backward) * 2
		g.set(x_write, DRAW_H-6, weekday_name[wd][0]) 
		g.set(x_write+1, DRAW_H-6, '_') 
		g.write_at(x_write, DRAW_H-(4 if days_backward%2==0 else 5), '{:02d}'.format(d))
		if d == 1:
			g.write_at(x_write, DRAW_H-3, month_name[m-1])
			g.stripe_up(x_write-1, DRAW_H-6, DRAW_H-4, char='|')
		fname = filename_for(y,m,d)
		if (y,m,d) == now_tuple:
			g.write_at(x_write, DRAW_H-2, '^TODAY')
			g.write_at(x_write+1, 0, '>>future>>')
		try:
			stat_info = os.stat(fname)
			draw_height = int(0.6*(stat_info.st_size**0.28))
			g.stripe_up(x_write, DRAW_H-7, draw_height, char='#')
		except: pass
		y,m,d,wd = prev_date(y,m,d,wd)
		days_backward += 1
	g.print_grid()

def prev_date(y,m,d,wd):
	d2 = d-1
	m2 = m
	y2 = y
	if d2 == 0:
		m2 = m-1
		if m2 == 0:
			m2 = 12
			y2 = y-1
		d2 = last_day(m2, y2)
	return y2, m2, d2, (wd-1 if wd > 0 else 6)
	
def next_date(y,m,d,wd):
	d2 = d+1
	m2 = m
	y2 = y
	if d2 > last_day(m2,y2):
		d2 = 1
		m2 += 1
		if m2 > 12:
			y2 += 1
			m2 = 1
	return y2, m2, d2, (wd+1 if wd < 6 else 0)

def leap(year):
	return year%4 == 0

def last_day(month, year):
	if month == 2:
		return 29 if leap(year) else 28
	else:
		return months_last_day[month]

def folder_for(y,m):
	l = [
		'{}'.format(y),
		'{}_{}'.format(y,m)
	]
	return os.path.join(ENTRIES_PATH, *l)
		
def filename_for(y,m,d):
	f = '{:04d}_{:02d}_{:02d}.txt'.format(y, m, d)
	return os.path.join(folder_for(y,m), f)

	
def assert_folder(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
	
	
def main():
	if ENTRIES_PATH == 'path_to_entries':
		print(('Please set the variable `ENTRIES_PATH` in `config.py`\n'
		'to your desired entries folder path!\n'
		'Press `ENTER` to exit.'))
		try: input()
		except: pass
		exit(1)
	now = datetime.datetime.now()
	now_tuple = (now.year, now.month, now.day, now.weekday())
	y,m,d,wd = deepcopy(now_tuple)
	while True:
		os.system('cls')
		selected_filename = filename_for(y,m,d)
		was_text = False
		print('Enter new text line(s) to append to today\'s entry. CTRL+C or `exit` to end')
		print('Enter commands as `/<command>` for any command in {prev, next, today, rmln, sync, exit}')
		print_vis(y, m, d, wd, now_tuple)
		try:
			with open(selected_filename, 'r') as f:
			
				print('Current entry for today ({}, {}-{}-{}) so far:'.format(weekday_name[wd], y, month_name[m-1], d))
				for ln in f:
					print('::  '+ln.strip())
			was_text = True
		except:
			print('No entry yet for today ({}, {}-{}-{}):'.format(weekday_name[wd], y, month_name[m-1], d))
		sys.stdout.write('::  ')
		try:
			text_in = input()
		except KeyboardInterrupt:
			print('\nSee you tomorrow!')
			exit(0)
			
		
		if text_in:
			# non-empty input
			if text_in.startswith('/'):
				# command input
				suppress_tip = False
				if text_in == '/exit':
					print('See you tomorrow!')
					exit(0)
				if text_in == '/today' or text_in == '/t':
					y,m,d,wd = now.year, now.month, now.day, now.weekday()
					print('going to today day!')
				elif text_in == '/prev' or text_in == '/p':
					y,m,d,wd = prev_date(y,m,d,wd)
					print('going to previous day!')
				elif text_in == '/next' or text_in == '/n':
					y,m,d,wd = next_date(y,m,d,wd)
					print('going to next day!')
				elif text_in[1:] == 'rmln' or text_in == '/r':
					deleted = del_line(selected_filename)
					pyperclip.copy(deleted)
					print('deleting last line! Its now in clipboard')
				elif text_in == '/sync':
					print('finding entries repo...')
					try:
						g
					except:
						try: g = git.cmd.Git(ENTRIES_PATH)
						except:
							print('failed to find git repo in `entries` folder!')
							continue
					print('pulling...')
					try:
						g.pull()
					except:
						print('pull failed')
					print('trying existing push')
					try:
						g.push()
					except:
						print('push failed')
					print('adding...')
					x = g.add('.')
					commit_msg = 'piary sync at ' + str(datetime.datetime.now())
					try:
						g.commit(m=commit_msg)
						print('committed')
						print('pushing...')
						g.push()
						print('success!')
					except:
						print('nothing to commit')
					print('press ENTER to continue...')
					input()
					suppress_tip = True
				else:
					suppress_tip = True
				if not suppress_tip and len(text_in) > 2 and text_in[0] == '/':
					print('Just `/{}` also works!\n'.format(text_in[1]))
					print('press ENTER to continue...')
					input()
					
				
			else:
				# diary entry input
				
				assert_folder(folder_for(y,m))
				with open(selected_filename, 'a') as f:
					f.write(('\n' if was_text else '')+text_in)
					
if __name__ == '__main__':
	main()
else:
	print('not main thread?')
	print('press ENTER to continue...')
	input()