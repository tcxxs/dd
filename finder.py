#coding: gbk

import parse

heroes = parse.parse_path('heroes/')


for hero in heroes.itervalues():
	'''
	print '--------attr--------'
	for k, v in hero['attr'].iteritems():
		print '\t', k, v
	print '--------skill--------'
	for name, skill in hero['skill'].iteritems():
		print '\t', name
		for k, v in skill.iteritems():
			print '\t\t', k, v
	'''

	print hero.name, hero.calc_damage()