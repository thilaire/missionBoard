/*
* Author: T. HILAIRE
*
* driver for TM1638 board and the SPI protocol used
*
* Licence: GPL v3
*/

#include <avr/io.h>
#include "ADC.h"

uint8_t Pot[4] = {0};       /* data from the ADC inputs */


/* initialize the ADC */
void initADC()
{
	ADMUX = 0b01100000; /* align left, so that we read 8 MSB bits in ADCH */
	ADCSRB = 0;
	DIDR0 = 0b11000011;     /* reduce power consumption, only ADC2, 3, 4 and 5 are used */
	ADCSRA = 0b10000100;    /* prescaler=32, so it runs at 250kHz; a conversion takes 25 cycles, or 0.1ms */
}

/* get the previously run ADC, and update the SPI */
uint8_t getADC(uint8_t cycle, uint8_t* data)
{
	*data = ADCH;   /* the value is in ADCH */
	/* compute the difference */
	int8_t diff = Pot[cycle] - *data;
	Pot[cycle] = *data;

	if ((diff>3) || (diff<-3))
	{
		return 1;
	}
	else return 0;   /* differ from 0 or 1 */
}

/* run the ADC (to be aquire in the next cycle */
void runADC(uint8_t cycle)
{
	/* select the ADC: 5-cycle gives the PIN of the ADC */
	ADMUX = 0b01100000 | ((5-cycle)&3);
	/* run it! */
	ADCSRA = 0b11000100;
}

/* when the RPi ask for all the data
we simply change the value stored in TMx8Input */
void switchDataADC()
{
	for( uint8_t i=0; i<4; i++)
	{
		Pot[i] = ~Pot[i];   /* switch the bits */
	}
}