# small script to help to compute the analog->digital decoder
# done with R1,R2,R3,R4 and R resistor (see schematic; this is NOT a R-2R ladder)

from matplotlib import pyplot as plt

# values of the resistors
R4 = 470
R3 = 1000
R2 = 2000
R1 = 4700
R = 100

# voltage references
Vcc = 3.3
Varef = 1.1

# compute the voltage wrt to the 4 switches (4-bits)
V = [0]*16
for i in range(16):
	# i in bin
	s1 = i&1
	s2 = (i&2)>>1
	s3 = (i&4)>>2
	s4 = (i&8)>>3

	# compute the voltage
	x = s1/R1 + s2/R2 + s3/R3 + s4/R4
	V[i] = Vcc*(x / (1/R + x))
	# draw the line
	plt.plot([0,15],[V[i],V[i]],'-r')

# then draw the voltage wrt to the 4 bits
plt.plot(range(16),V,'*-')
plt.show()

# draw the difference (in number) after 8-bit Analog-Digital Conversion
xdiff = [256/Varef*(V[n]-V[n-1]) for n in range(1,len(V))]
plt.plot(range(15),xdiff,'ko-')
plt.show()

# inverse plot: draw the switches position (4-bit number) wrt to the result of the DAC
Ind = [0]*256
for i in range(16):
	x = int(V[i]*256/Varef)
	x_m = int(V[i-1] * 256 / Varef) if i>0 else x
	x_p = int(V[i+1] * 256 / Varef) if i<15 else 1.5*x

	for j in range(x-int((x-x_m)/2),x+int((x_p-x)/2)+1):
		if (j)>0 and (j)<256:
			Ind[j] = i

plt.plot(range(256),Ind,'-')
plt.plot([(x*256/Varef) for x in V],range(16),'r*')  # exact value for each number

x7 = V[7]*256/Varef
x8 = V[8]*256/Varef
x15 = V[15]*256/Varef
# coefficient tuned by hand
plt.plot([3+i*x7/7 for i in range(0,8)], range(0,8),'-og')
plt.plot([41+i*(x15-x8+3)/7 for i in range(8,16)], range(8,16), '-og')

# from scipy import stats, polyfit
# #slope, intercept, r_value, p_value, std_err = stats.linregress([int(x*256/Varef) for x in V[0:8]],range(0,8))
# (ar,br)=polyfit(V[0:8],range(0,8),1)
# print(ar, br)
# plt.plot([(ar*i+br) for i in range(0,8)],range(0,8),'og-')

plt.show()

#
print(x7/7)
print((x15-x8+3)/7)
def f(x):
	a = x-36
	b = a + (a>>2) + (a>>3)
	return b>>4

plt.plot(range(256),Ind,'-')
plt.plot(range(122),[(x+5)>>4 for x in range(122)],'y.')  # integer computation
plt.plot(range(126,220),[f(x) for x in range(126,220)],'m.')   # approx of (x-41)/((x15-x8+3)/7) (or (x-41)/11.62)
plt.plot([(x*256/Varef) for x in V],range(16),'r*')  # exact value for each number
plt.show()