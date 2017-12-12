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

struct cRGB LedOff = {0};
struct cRGB leds[NB_LEDS] = {0};     /* leds */
struct cRGB bufferLeds[NB_LEDS] = {0};  /* buffer of data to send (dedicated to light_ws2812 libray) */
uint8_t blink[NB_LEDS]; /* blink scheme (mask+threshold) for each led */
uint8_t ledsHasChanged = 0;
uint16_t toBlinkTable = 0;  /* the x-th bit of toBlinkTable indicates if a Led need to change its color (blink) at cycle #x wrt to the previous cycle */


/* add a new command for a led
nLed: number of the led
led: the new color
blink: blink pattern
*/
void newCommandLed(uint8_t nLed, uint8_t* buffer)
{
	uint8_t *pBlink = blink;

	ledsHasChanged = 1;
	/* copy the first three octets */
	leds[ nLed ] = *(struct cRGB*) buffer;
	blink[ nLed ] = buffer[3];
	/* update the blink table
	ie iterate on each blink led
	and for each of them
	iterate on each cycle to detect when the state of the led changes
	and update toBlinkTable according to it */
	toBlinkTable = 0;
	for( uint8_t i=0; i<NB_LEDS; i++)
	{
		if (*pBlink)    // this led blinks
		{
			uint8_t precBlink = ((0 & *pBlink>>4)) >= (*pBlink&15);
			uint8_t currBlink;
			for( uint8_t cycle=15; cycle>0; cycle--)
			{
				currBlink = ((cycle & *pBlink>>4)) >= (*pBlink&15);
				toBlinkTable |= (currBlink!=precBlink);
				toBlinkTable <<= 1;
			}
		}
		pBlink++;
	}
}

/* fill the Led Buffer with the led colors
  (manage the blinking according to the cycle) */
void fillLedBuffer( uint8_t bcycle)
{
	struct cRGB *pBuffer = bufferLeds;
	uint8_t *pBlink = blink;

	/* copy the leds to the buffer */
	memcpy(bufferLeds, leds, 3*NB_LEDS);

	/* switch off the leds that blink in that cycle */
	for( uint8_t i=0; i<NB_LEDS; i++)
	{
		if ( ((bcycle & *pBlink>>4)) < (*pBlink&15) )
		{
			/* this led is off */
			*pBuffer = LedOff;
		}
		pBuffer++;
		pBlink++;
	}
}


/* SPI interrupt function */
ISR (SPI_STC_vect)
{
	static uint8_t SPIcycle = 0;
	static uint8_t SPIcommand;
	static uint8_t SPIbuffer[4];

	/* copy the data (1st data in SPIcommand, the others in SPIbuffer) */
	if (SPIcycle)
		SPIbuffer[ SPIcycle-1 ] = SPDR;
	else
		SPIcommand = SPDR;
	SPIcycle++;
	/* check if the end of the data transfer */
	if (SPIcycle == 5)
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
		if (ledsHasChanged || (toBlinkTable & (1U<<(cycle>>4))) )
		{
			/* prepare the buffer */
			fillLedBuffer(cycle>>4);
			ws2812_setleds( bufferLeds, NB_LEDS);
			ledsHasChanged = 0;
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



	/* test */
	leds[0].r = 255;
	blink[0] = 0x11;

	leds[2].r = 255;
	leds[2].g = 255;
	blink[2] = 0x41;

	leds[4].b = 255;
	leds[4].g = 255;
	blink[4] = 0x72;

	/* enable interrupts and wait */
	sei();
	while(1);   /*TODO: idle mode? */
}
