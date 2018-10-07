# small script to help to compute the analog->digital decoder
# done with R1,R2,R3,R4 and R resistor (see schematic; this is NOT a R-2R ladder)

from matplotlib import pyplot as plt
from math import sqrt

data = [0, 24, 49, 75, 79, 103, 127, 150, 120, 142, 164, 186, 190, 210, 230, 249]



for i in range(16):
	# draw the line
	plt.plot([data[i], data[i]], [0, 15], '-r')

plt.plot(data, range(16), '*-')
plt.show()

rang = range(0,8)

# generate the lookup table
lut = [255]*256
for i, v in enumerate(data):

	for j in range(v-2,v+3):
		if j>=0:
			if lut[j] == 255:
				lut[j] = i
			else:
				print("Error for lut[%d]=%d"%(j, i))

print( "{" + ", ".join(str(v) for v in lut) + "}")




# try for optimizing coefficients (successful but not useful)
def diff(coefs, p=False):
	V = [d for d in data]
	for i in rang:
		# i in bin
		s1 = i&1
		s2 = (i&2)>>1
		s3 = (i&4)>>2
		s4 = (i&8)>>3

		V[i] = (coefs[0]*s1 + coefs[1]*s2 + coefs[2]*s3 + coefs[3]*s4)

	if p:
		plt.plot(range(16),[v-d for v,d in zip(V,data)])
		plt.show()

	return sqrt(sum(abs(v-d)**2 for v,d in zip(V,data)))


coefs = (slice(10, 30,0.5), slice(34, 54,.5), slice(70,85,.5), slice(110,120,.5))

# from scipy import optimize
# resbrute = optimize.brute(diff, coefs, full_output=True, finish=None)
# print(resbrute[0])  # global minimum
# print(resbrute[1])  # function value at global minimum
#
# diff(resbrute[0], True)
