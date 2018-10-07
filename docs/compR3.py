
from matplotlib import pyplot as plt
from math import sqrt
from operator import itemgetter

# data
data = [0, 24, 49, 75, 79, 103, 127, 150, 120, 142, 164, 186, 190, 210, 230, 249]

# sorted list of tuple (data, value to get)
i = sorted(zip(data, range(16)), key=itemgetter(0))
print(i)

# diff to get the intervals
intervals = [i.pop(0)]
prevd = intervals[0][0]
for d in i:
	intervals.append(((d[0]+prevd)//2, d[1]))
	prevd = d[0]

print(intervals)

inter, sw = list(zip(*intervals))

print("{" + ", ".join(str(v) for v in inter) + "}")
print("{" + ", ".join(str(v) for v in sw) + "}")

def test(x):
	ind = 8
	lvl = 8
	while lvl > 1:
		lvl = lvl // 2
		if x < inter[ind]:
			ind -= lvl
		else: #elif x > inter[ind]:
			ind += lvl

	return sw[ind-1] if x<inter[ind] else sw[ind]


# test if our test function is right
for v,d in enumerate(data):
	for i in range(-2,3):
		if test(d+i) == v:
			pass
			# print("test(%d+%d)=%d"%(d, i, v))
		else:
			print(u"\u26A0" + "!! test(%d) != %d" % (d+i, v))
