#coding: gbk

class Hero(object):
	def __init__(self, name, hero):
		super(Hero, self).__init__()
		self.__dict__.update(hero['attr'])
		self.name = name
		self.skills = {}
		for sname, sattr in hero['skill'].iteritems():
			self.skills[sname] = Skill(self, sname, sattr)

	def calc_damage(self):
		dmg = 0
		for skill in self.skills.itervalues():
			dmg += skill.calc_damage()
		return dmg

class Skill(object):
	def __init__(self, hero, name, attr):
		super(Skill, self).__init__()
		self.__dict__.update(attr)
		self.hero = hero
		self.name = name

	def calc_damage(self):
		if not hasattr(self, 'enemy'):
			return 0
		if hasattr(self, 'crit'):
			crit = self.crit.value
		else:
			crit = 0
		crit = max(0, self.hero.crit.value + crit)
		dmg = self.hero.dmg.average() * (self.dmg.value / 100.0)
		return dmg * (1 + crit)