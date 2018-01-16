# Compilation options
CC = avr-gcc
OBJCPY = avr-objcopy
CCFLAGS = -Wall -O3
OPTIM = -Os

# about the AVR
DEVICE = attiny88
FREQ = 8000000UL

# and the Raspberry Pi that program the AVR
HOST = pi@raspberrypi.local

# files
OUT = MB-AVR
SRC = light_ws2812.c MB-AVR.c TM1638.c TMx8.c RGB.c
OBJ = $(SRC:.c=.o)

all: $(OUT).hex

# Compile the C files
MB-AVR.o: TMx8.h ws2812_config.h RGB.h
light_ws2812.o: light_ws2812.h ws2812_config.h
RGB.o: RGB.h
TM1638.o: TM1638.h
TMx8.o: TMx8.h TM1638.h
%.o: %.c
	$(CC) $(CCFLAGS) $(OPTIM) -mmcu=$(DEVICE) -DF_CPU=$(FREQ) -o $@ -c $<

# Link them
$(OUT).elf: $(OBJ)
	$(CC) -mmcu=$(DEVICE) -o $@ $^

# Generate the hex
$(OUT).hex: $(OUT).elf
	$(OBJCPY) -j .text -j .data -O ihex $< $@

assembly: $(SRC:.c=.s)
%.s : %.c %.o
	$(CC) $(CCFLAGS) $(OPTIM) -mmcu=$(DEVICE) -DF_CPU=$(FREQ) -S -fverbose-asm $< -o $@

# Flash the AVR (with avrdude)
# (use ssh with public/private key, so as to do not have to type the password each time...)
program: $(OUT).hex
	scp $< $(HOST):.
	ssh -t $(HOST) sudo avrdude -c linuxgpio -p $(DEVICE) -U flash:w:$< -v
	ssh -t $(HOST) sudo rmmod spi_bcm2835
	ssh -t $(HOST) sudo modprobe spi_bcm2835

# Clen the mess
clean:
	rm -f $(OBJ) $(OUT).elf $(OUT).hex $(SRC:.c=.s)
	ssh $(HOST) rm -f $(OUT).hex
