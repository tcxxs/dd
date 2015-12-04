#coding: gbk

import parse

heroes = parse.parse_heroes('heroes/')


for hero in heroes:
	print '--------attr--------'
	for k, v in hero['attr'].iteritems():
		print '\t', k, v
	print '--------skill--------'
	for name, skill in hero['skill'].iteritems():
		print '\t', name
		for k, v in skill.iteritems():
			print '\t\t', k, v