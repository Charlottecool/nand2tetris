Class SymbolTable():
	def __init__(self):
		self.class_scope = {}
		self.subroutine_scope = {}
		self.index_counters = {'static':0,'field':0,'argument':0,'local':0}

	def startSubroutine(self):
		self.subroutine_scope = {}
		self.index_counters['argument'] = 0
		self.index_counters['local'] = 0

	def Define(self,name,type,kind):
		if kind in ['static','field']:
			self.class_scope[name] = (type,kind,self.index_counters[kind])
		else:
			self.subroutine_scope[name] = (type,kind,self.index_counters[kind])
		self.index_counters += 1

	def VarCount(self,kind):
		return self.index_counters[kind]

	def KindOf(self,name):
		if name in self.subroutine_scope:
			return self.subroutine_scope[name][1]
		elif name in self.class_scope:
			return self.class_scope[name][1]
		return None

	def TypeOf(self,name):
		if name in self.subroutine_scope:
			return self.subroutine_scope[name][0]
		elif name in self.class_scope:
			return self.class_scope[name][0]
		return None

	def IndexOf(self,name):
		if name in self.subroutine_scope:
			return self.subroutine_scope[name][2]
		elif name in self.class_scope:
			return self.class_scope[name][2]
		return None