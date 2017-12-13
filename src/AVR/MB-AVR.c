/*
* Author: T. HILAIRE
*
* Licence: GPL v3
*/

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include "light_ws2812.h"
#include <string.h>

/* RGB LEDS */
#define NB_LEDS 20


struct sLED{
	uint16_t blinkPattern;  /* pattern: x-th bits indicates if the led is on at cycle x; 0xffff for always on, 0b0101010101010101 for fast blinking */
	struct cRGB color;
};

const struct cRGB LedOff = {0};
struct sLED leds[NB_LEDS] = {0};     /* leds */
struct cRGB bufferLeds[NB_LEDS] = {0};  /* buffer of data to send (dedicated to light_ws2812 libray) */

uint8_t ledsHasChanged = 0;
uint16_t blinkEvent = 0;  /* the x-th bit of blinkEvent indicates if a Led need to change its color (blink) at cycle #x WRT to the previous cycle */
uint16_t blinkEventTable[NB_LEDS] = {0};    /* intermediate table: the same as blinkEvent, but for each led. Use only to do not have to recompute it every time (we have here enough bytes in RAM for this) */

/* add a new command for a led
nLed: number of the led
buffer: the 5 bytes for the SPI buffer */
void newCommandLed(uint8_t nLed, uint8_t* buffer)
{
	ledsHasChanged = 1;

	/* copy the five bytes */
	leds[ nLed ] = *(struct sLED*) buffer;

	/* update the blink Event Table for the concerned led */
	uint16_t blinkPatternOfThisLed = leds[ nLed].blinkPattern;
	blinkEventTable[ nLed ] = blinkPatternOfThisLed ^ ( (blinkPatternOfThisLed>>15) | (blinkPatternOfThisLed<<1) ); /* (a>>15) | (a<<1) corresponds to a 1-bit left bitwise rotation; a XOR with itself gives the place where the bit changes from it predecessor */

	/* then re-compute blinkEvent, as the OR-sum of each blinkEventTable element */
	blinkEvent = 0;
	uint16_t* pbE = blinkEventTable;
	for(uint8_t i=0; i<NB_LEDS; i++)
	{
		blinkEvent |= *pbE++;
	}
}


/* fill the Led Buffer with the led colors
  (manage the blinking according to the cycle) */
void fillLedBuffer( uint8_t bcycle)
{
	struct cRGB *pBuffer = bufferLeds;
	struct sLED *pLeds = leds;
	uint16_t pattern = (1U<<bcycle);

	/* copy the leds to the buffer */
	/* and switch off the leds that blink (off) in that cycle */
	for( uint8_t i=0; i<NB_LEDS; i++)
	{
		if (pLeds->blinkPattern & pattern)
		{
			*pBuffer = pLeds->color;
		}
		else
		{
			/* this led is off */
			*pBuffer = LedOff;
		}
		pBuffer++;
		pLeds++;
	}
}


/* SPI interrupt function */
ISR (SPI_STC_vect)
{
	static uint8_t SPIcycle = 0;
	static uint8_t SPIcommand;
	static uint8_t SPIbuffer[5];    /* 5 bytes for a LED ( RGB+ blink pattern) */

	/* copy the data (1st data in SPIcommand, the others in SPIbuffer) */
	if (SPIcycle)
		SPIbuffer[ SPIcycle-1 ] = SPDR;
	else
		SPIcommand = SPDR;
	SPIcycle++;
	/* check if the end of the data transfer */
	if (SPIcycle == 6)
	{
		SPIcycle = 0;
		newCommandLed( SPIcommand, SPIbuffer);
	}
}


/* Timer 1 interrupt function (when TIMER1==OCR1A) */
ISR (TIMER1_COMPA_vect  )
{
	static uint8_t cycle=0;
	if ((cycle&3) == 0)
	{
		/* capture ADC0, TM1637[0] and TM1638[0] */
	}
	else if ((cycle&3) == 1)
	{
		/* capture ADC1, TM1637[1] and TM1638[1] */
	}
	else if ((cycle&3) == 2)
	{
		/* capture ADC2, TM1637[2] and TM1638[2] */
	}
	if ((cycle&15) == 3)
	{
		/* check if we need to send data to the led (something has changed since previous cycle ?) */
		if (ledsHasChanged || ((blinkEvent >> (cycle>>4))&1) )      /* cycle>>4 -th bit of blinkEvent */
		{
			/* prepare the buffer */
PORTC |= (1U<<7);
			fillLedBuffer(cycle>>4);
			ws2812_setleds( bufferLeds, NB_LEDS);
			ledsHasChanged = 0;
PORTC &= ~(1U<<7);
		}
	}

	/* next cycle */
	cycle++;
}


int main(void)
{
	/* configure inputs/outputs */
	DDRB = 0b11010011;       /* PB0, PB1, PB4, PB6 and PB7 are outputs */
	DDRC = 0b10111000;       /* PC3, PC4, PC5 and PC7 are outputs */
	DDRD = 0b11110000;      /* PD4, PD5, PD6 and PD7 are outputs */

	/* configure the USI */
	SPCR |= (1<<SPIE) | (1<<SPE);

	/* turn off the leds */
	ws2812_setleds(bufferLeds, NB_LEDS);

	/* blink LED C7 (debug LED) to tell we are alive */
	PORTC |= (1U<<7);
	_delay_ms(500);
	PORTC &= ~(1U<<7);


	/* configure timer1, 16bits mode, Prescaler=1/8
	interrupt after 15625 ticks (compare for channel A) */
	TCCR1B = (1U<<CS11) | (1U<<WGM12);     /* prescaler = 1/8 and Clear Timer on Compare match (CTC) T*/
	TCCR1C = (1U<<FOC1A);    /* channel A */
	OCR1A = 15625;              /* 15625 ticks @ 1MHz -> 15.625ms */
	TIMSK1 = (1U<<OCIE1A);      /* set interrupt on Compare channel A */


	/* enable interrupts and wait */
	sei();
	while(1);   /*TODO: idle mode? */
}
