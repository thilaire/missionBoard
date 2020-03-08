# coding=utf-8

# dictionary value -> 7-segment data
Font = {
	0: 0b00111111,  # (48) 0
	1: 0b00000110,  # (49) 1
	2: 0b01011011,  # (50) 2
	3: 0b01001111,  # (51) 3
	4: 0b01100110,  # (52) 4
	5: 0b01101101,  # (53) 5
	6: 0b01111101,  # (54) 6
	7: 0b00100111,  # (55) 7
	8: 0b01111111,  # (56) 8
	9: 0b01101111,  # (57) 9
}

# build array10 and array10 of numbers such that
# i/16 = array10[i]/10 + array100[i&7]/100 (approximatively)
array10 = []
array100 = []
for i in range(16):
	f = i/16.0
	if i < 8:
		array100.append(int(f * 100) % 10)

	array10.append(int(f * 10))


print(array10)
print(array100)

# check
for i in range(16):
	print("%d -> %s%s" % (i, array10[i], array100[i & 7]))

# print the C arrays
print("const uint8_t digit[16] = {" + ",".join(str(Font[i % 10]+128) for i in range(16)) + "};")
print("const uint8_t array10[16] = {" + ",".join(str(Font[array10[i]]) for i in range(16)) + "};")
print("const uint8_t array100[8] = {" + ",".join(str(Font[array100[i]]) for i in range(8)) + "};")


# check
for i in range(256):
	# if i&15:
	print("%s%d.%d%d%d%d" % ("1" if ((i >> 4) > 9) else " ", (i >> 4) % 10, array10[i & 15], array100[i & 7],
	      array100[i & 3], array100[(i << 1) & 3]))
	# else:
	#   print("%d.%d%d%d%d" % (i >> 4, 0, 0, 0, 0))
