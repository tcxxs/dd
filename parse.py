#coding: gbk

import os
import attr
import hero

FILE_EXT = '.hero'

def parse_path(path):
	heroes = {}
	for fname in os.listdir(path):
		if not fname.endswith(FILE_EXT):
			continue
		name = os.path.splitext(fname)[0]
		heroes[name] = hero.Hero(name, parse_file(os.path.join(path, fname)))
	return heroes

def parse_file(fname):
	f = open(fname, 'rb')
	content = f.read()
	f.close()

	hero = {}
	path = []
	for line in content.split('\n'):
		line = line.rstrip()
		if not line:
			continue
		parse_line(hero, path, line)

	return hero

def parse_line(hero, path, line):
	tabs = 0
	while line[tabs] == '\t':
		tabs += 1
	line = line[tabs:]
	
	path[tabs:] = []
	cur = hero
	for key in path:
		cur = cur[key]

	info = line.split('=')
	if len(info) == 1:
		key = info[0]
		cur[key] = {}
		path.append(key)
	else:
		key, value = info
		cur[key] = attr.value(path, key, value)