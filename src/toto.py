
class Bidule:

	def __init__(self,v):
		self._v = v

	def __set__(self, instance, value):
		self._v = self._v+value




class Toto:

	d = {}


	def __init__(self):
		pass

	def add(self,name,x):
		self.bidule = Bidule(x)
		pass

class Celsius:

	def __init__(self, val):
		self._val = val
	def __get__(self, instance, owner):
		print('__get__')
		print(owner)
		return 5 * (instance.fahrenheit - 32) / 9 + self._val

	def __set__(self, instance, value):
		print ('__set__')
		instance.fahrenheit = 32 + 9 * value / 5 + self._val


class Temperature:

	#celsius = Celsius()

	def __init__(self, initial_f, name, val):
		self.fahrenheit = initial_f
		setattr(self.__class__, name, Celsius(val))

t = Temperature(212, 'toto',1000)
print(t.toto)
t.toto = 0
print(t.fahrenheit)



A = Toto()
A.add('bidule',12)
A.bidule=12

print(A)