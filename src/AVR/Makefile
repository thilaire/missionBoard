# Compilation options
CC = avr-gcc
OBJCPY = avr-objcopy
CCFLAGS = -Wall
OPTIM = -Os

# about the AVR
DEVICE = attiny861
FREQ = 8000000UL

# and the Raspberry Pi that program the AVR
HOST = pi@raspberrypi.local

# files
OUT = MB-AVR
SRC = light_ws2812.c MB-AVR.c
OBJ = $(SRC:.c=.o)


# Compile the C files
light_ws2812.o: light_ws2812.h ws2812_config.h
%.o: %.c
    $(CC) $(CCFLAGS) $(OPTIM) -mmcu=$(DEVICE) -DF_CPU=$(FREQ) -o $@ -c $<

# Link them
$(OUT).elf: $(OBJ)
    $(CC) -mmcu=$(DEVICE) -o $@ $^

# Generate the hex
$(OUT).hex: $(OUT).elf
    $(OBJCPY) -j .text -j .data -O ihex $@ $<

# Flash the AVR (with avrdude)
program: $(OUT).hex
    scp $< $(HOST):.
    ssh -t $(HOST) sudo avrdude -c linuxgpio -p $(DEVICE) -U flash:w:$< -v


# Clen the mess
clean:
	rm -f $(OBJ) $(OUT).elf $(OUT).hex
	ssh $(HOST) rm -f $(OUT).hex
