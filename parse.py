#coding: gbk

import os
import attr

HERO_FILE_EXT = '.hero'

def parse_heroes(path):
	heroes = []
	for fname in os.listdir(path):
		if not fname.endswith(HERO_FILE_EXT):
			continue
		heroes.append(parse_hero(os.path.join(path, fname)))
	return heroes

def parse_hero(fname):
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