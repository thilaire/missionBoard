/*
* Author: T. HILAIRE
*
* Licence: GPL v3
*/

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include "light_ws2812.h"


struct LED
{
	uint8_t red;
	uint8_t green;
	uint8_t blue;
	uint8_t blink;
};



/* RGB LEDS */
#define NB_LEDS 20

struct LED leds[NB_LEDS] = {0};     /* leds */
struct cRGB bufferLeds[NB_LEDS] = {0};  /* buffer of data to send (dedicated to light_ws2812 libray) */
uint8_t hasChanged = 1;

/* timer */
uint8_t cycle=0;


/* SPI */
uint8_t SPIbuffer[5];
uint8_t SPIcycle = 0;

ISR (SPI_STC_vect)                  // SPI interrupts
{
	PORTC |= (1U<<7);
	SPIbuffer[ SPIcycle++ ] = SPDR;

	if (SPIcycle == 5)
	{
		SPIcycle = 0;
		uint8_t* sr = (uint8_t*) &leds[ SPIbuffer[0] ];
		uint8_t* de = &SPIbuffer[1];
		*sr++ = *de++;
		*sr++ = *de++;
		*sr++ = *de++;
		*sr++ = *de++;
		/*leds[ SPIbuffer[0] ].red = SPIbuffer[1];
		leds[ SPIbuffer[0] ].green = SPIbuffer[2];
		leds[ SPIbuffer[0] ].blue = SPIbuffer[3];
		leds[ SPIbuffer[0] ].blink = SPIbuffer[4];*/
	}

	PORTC &= ~(1U<<7);
	SPDR = 42;
}

ISR (TIMER1_COMPA_vect  )
{
	cycle++;

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
		/* deal with the RGB leds */
		struct LED *pL = leds;
		struct cRGB *pB = bufferLeds;
		uint8_t bcycle = cycle>>4;
		for( uint8_t i=0; i<NB_LEDS; i++)
		{
			if ( (bcycle & (pL->blink>>4)) >= (pL->blink&15) )
			{
				/* this led is on */
				pB->r = pL->red;
				pB->g = pL->green;
				pB->b = pL->blue;
			}
			else
			{
				/* this led is off */
				pB->r = 0;
				pB->g = 0;
				pB->b = 0;
			}
			pL++;
			pB++;
		}
		ws2812_setleds(bufferLeds,NB_LEDS);
	}



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

	/* blink LED C7 to tell we are alive */
	PORTC |= (1U<<7);
	_delay_ms(500);
	PORTC &= ~(1U<<7);


	/* configure timer1, 16bits mode, Prescaler=1/8
	interrupt after 15625 ticks (compare for channel A) */
	TCCR1B = (1U<<CS11) | (1U<<WGM12);     /* prescaler = 1/8 and Clear Timer on Compare match (CTC) T*/
	TCCR1C = (1U<<FOC1A);    /* channel A */
	OCR1A = 15625;              /* 15625 ticks @ 1MHz -> 15.625ms */
	TIMSK1 = (1U<<OCIE1A);      /* set interrupt on Compare channel A */



	leds[0].red = 255;
	leds[0].blink = 0x11;

	leds[2].red = 255;
	leds[2].green = 255;
	leds[2].blink = 0x41;

	leds[4].blue = 255;
	leds[4].green = 255;
	leds[4].blink = 0x72;




	SPDR = 42;
	sei();  /* enable interrupts */
	while(1);   /*TODO: idle mode? */


/*	 unsigned char i, delta=0;
	 struct cRGB colors[8];
  //Rainbowcolors
    colors[0].r=150; colors[0].g=150; colors[0].b=150;
    colors[1].r=255; colors[1].g=000; colors[1].b=000;//red
    colors[2].r=255; colors[2].g=100; colors[2].b=000;//orange
    colors[3].r=100; colors[3].g=255; colors[3].b=000;//yellow
    colors[4].r=000; colors[4].g=255; colors[4].b=000;//green
    colors[5].r=000; colors[5].g=100; colors[5].b=255;//light blue (türkis)
    colors[6].r=000; colors[6].g=000; colors[6].b=255;//blue
    colors[7].r=100; colors[7].g=000; colors[7].b=255;//violet


  while(1)
  {

    for(i=0; i<NB_LEDS; i++)
    {
        bufferLeds[i] = colors[(i+delta)&7];
    }
    delta++;

    ws2812_setleds(bufferLeds,NB_LEDS);
    _delay_ms(500);                         // wait for 500ms.

  }*/



}
