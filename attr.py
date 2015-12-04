#coding: gbk

class Attr(object):
	def __init__(self, val):
		super(Attr, self).__init__()
		self.value = val

	def __str__(self):
		return str(self.value)

class Int(Attr):
	def __init__(self, val):
		super(Int, self).__init__(int(val))

	def __str__(self):
		return str(self.value)

class Float(Attr):
	def __init__(self, val):
		super(Float, self).__init__(float(val))

	def __str__(self):
		return '%.1f' % self.value

class Range(Attr):
	def __init__(self, val):
		info = val.split('-')
		if len(info) == 1:
			rg = (int(info[0]), int(info[0]))
		else:
			rg = (int(info[0]), int(info[1]))
		super(Range, self).__init__(rg)

	def __str__(self):
		return '%d-%d' % self.value

	def average(self):
		return sum(self.value) / 2

class Pos(Attr):
	def total(self):
		if '*' in self.value:
			n = 0
			for c in self.value:
				if c == '*':
					n += 1
			return n
		else:
			return 1

class Set(Attr):
	def __init__(self, ab, val):
		super(Set, self).__init__(val)
		self.ab = ab

	def __str__(self):
		s = []
		for c in self.value:
			s.append(self.ab[c])
		return ','.join(s)

class SetType(Set):
	def __init__(self, val):
		ab = {
			'm': 'melee',
			'r': 'range',
			'b': 'buff',
			'h': 'heal',
			'c': 'cure',
		}
		super(SetType, self).__init__(ab, val)

class SetAttack(Set):
	def __init__(self, val):
		ab = {
			'*': 'random',
			'm': 'mark',
			's': 'stun',
			'h': 'human',
			'u': 'unholy',
			'b': 'beast',
		}
		super(SetAttack, self).__init__(ab, val)

class Buff(Attr):
	def __init__(self, val):
		buffs = {}
		while val:
			buff = val[:2]
			val = val[2:]
			buffs.setdefault(buff, 0)
			buffs[buff] += 1
		super(Buff, self).__init__(buffs)

	def __str__(self):
		s = []
		for k, c in self.value.iteritems():
			s.append('%s:%d' % (k, c))
		return ','.join(s)

class Move(Attr):
	def __init__(self, val):
		moves = set()
		while val:
			moves.add(val[:2])
			val = val[2:]
		super(Move, self).__init__(moves)

	def __str__(self):
		return ','.join(self.value)

class State(Attr):
	def __init__(self, val):
		if val == '-':
			state = None
		else:
			state = val
		super(State, self).__init__(state)

	def __str__(self):
		if self.value:
			return '+'
		else:
			return '-'

class StateDot(State):
	def __init__(self, val):
		if val == '-':
			dot = val
		else:
			info = val.split('/')
			dot = (int(info[0]), int(info[1]))
		super(StateDot, self).__init__(dot)

	def __str__(self):
		if self.value:
			return '%d/%d' % self.value
		else:
			return '-'

_ATTR = {
	'attr': {
		'hp': Int,#=33
		'dodge': Int,#=5
		'prot': Int,#=0
		'spd': Int,#=1
		'acc': Int,#=0
		'crit': Float,#=5
		'dmg': Range,#=6-12
	},
	'skill': {
		'*': {
			'pos': Pos,#=xxoo
			'ally': Pos,#=ooxx, xxxx(self)
			'enemy': Pos,#=ooxx
			'type': SetType,#=m(m melee, r range, b buff, h heal, c cure)
			'acc': Int,#=100
			'dmg': Int,#=100
			'crit': Float,#=10
			'attack': SetAttack,#=h(* random, m mark, s stun, h human, u unholy, b beast)
			'self': Buff,#=+a(attack, + buff, - debuff), d(defence), u(useful)
			'target': Buff,#=+a(attack, + buff, - debuff), d(defence), u(useful)
			'move': Move,#=+1(+/- self move, + to right), <1(<> target move, < to left), *(random)
			'stun': State,#=+(affect), -(cure)
			'mark': State,#=+(affect), -(cure)
			'blight': StateDot,#=2/3(dmg/round), -(cure)
			'bleed': StateDot,#=2/3(dmg/round), -(cure)
			'heal': Range,#=1-10
			'stress': Int,#=10
			'torch': Int,#=10
		},
	},
}

def value(path, key, value):
	attr = _ATTR
	for p in path:
		if p in attr:
			attr = attr[p]
		else:
			attr = attr['*']

	return attr[key](value)