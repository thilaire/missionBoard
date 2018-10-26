# Compilation options
CC = avr-gcc
OBJCPY = avr-objcopy
CCFLAGS = -Wall -O3
#OPTIM =
OPTIM = -Os

# about the AVR
DEVICE = attiny88
FREQ = 8000000UL

# and the Raspberry Pi that program the AVR
HOST = pi@raspberrypi.local

# files
OUT = MB-AVR
SRC = light_ws2812.c MB-AVR.c TM1638.c TM1637.c TMx.c RGB.c ADC.c
OBJ = $(SRC:.c=.o)

all: $(OUT).hex

# Compile the C files
MB-AVR.o: TMx.h ws2812_config.h RGB.h ADC.h
light_ws2812.o: light_ws2812.h ws2812_config.h
RGB.o: RGB.h
ADC.o: ADC.h
TM1638.o: TM1638.h
TM1637.o: TM1637.h
TMx.o: TMx.h TM1638.h TM1637.h
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
	@ssh -t $(HOST) 'echo 21 > /sys/class/gpio/export || :'
	@ssh -t $(HOST) 'echo "out" > /sys/class/gpio/gpio21/direction || :'
	@ssh -t $(HOST) 'echo 1 > /sys/class/gpio/gpio21/value'
	ssh -t $(HOST) sudo avrdude -c linuxgpio -p $(DEVICE) -U flash:w:$< -v
	@ssh -t $(HOST) sudo rmmod spi_bcm2835
	@ssh -t $(HOST) sudo modprobe spi_bcm2835
	@ssh -t $(HOST) 'echo 0 > /sys/class/gpio/gpio21/value'

# Clean the mess
clean:
	rm -f $(OBJ) $(OUT).elf $(OUT).hex $(SRC:.c=.s)
	ssh $(HOST) rm -f $(OUT).hex

# shutdown the raspberry
shutdown:
	ssh $(HOST) sudo shutdown now