/*
* Author: T. HILAIRE
*
* Licence: GPL v3
*/

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include "light_ws2812.h"
#include "TMx8.h"
#include <string.h>


/* data for TM1637 and TM1638 */
#define NB_TMx8 3
#define NB_TMx7 3
uint8_t TMxDisplay[NB_TMx8+NB_TMx7] = {0};    /* display data of the TM1637 and TM1638*/


const uint8_t TMx8_STB_PINMASK[3] = { BIT(TMx8_STB_PIN0), BIT(TMx8_STB_PIN1), BIT(TMx8_STB_PIN2)};  /* STB0, STB1 and STB2 are on PD5, PD6 and PD7 respectively */



//#define NB_TMx7 3
//uint8_t TMx7data[NB_TMx7][8]={0};  /* each TM1638 has 16 bytes of addressable data */
//uint8_t TMx7toChange[NB_TMx7] = {0};    /* x-th bit set to 1 => the x-th byte has changed (should be sent to the TMx8) */


/* data for RGB LEDS */
#define NB_LEDS 21
struct sRGB_LED{
	uint16_t blinkPattern;  /* pattern: x-th bits indicates if the led is on at cycle x; 0xffff for always on, 0b0101010101010101 for fast blinking */
	struct cRGB color;
};
const struct cRGB LedOff = {0};         /* led off */
struct sRGB_LED RGBleds[NB_LEDS] = {0};        /* array of leds */
struct cRGB bufferLeds[NB_LEDS] = {0};  /* buffer of data to send (dedicated to light_ws2812 libray) */

uint8_t RGBledsHasChanged = 0; /* bool that indicates if the leds has changed during last cycle */
uint16_t blinkEvent = 0;  /* the x-th bit of blinkEvent indicates if a Led need to change its color (blink) at cycle #x WRT to the previous cycle */
uint16_t blinkEventTable[NB_LEDS] = {0};    /* intermediate table: the same as blinkEvent, but for each led. Use only to do not have to recompute it every time (we have here enough bytes in RAM for this) */

/*TODO: put it in a fancy struct */




void setDisplayTMx(uint8_t SPIcommand, uint8_t* SPIbuffer)
{
	uint8_t nTM = SPIcommand&7;     /* number of the TM board: 0-3 for the TMx8 and 4-7 for the TMx7 */
	uint8_t size = 8 ? (SPIcommand & (1<<4)) : 4; /* 4 or 8 bytes */
	uint8_t* TMbuffer = &(TMxDisplay[nTM]);
	for( uint8_t i = 4 ? SPIcommand & (1<<3) : 0; i<size; i++)  /* 1st or 2nd display */
	{
		/* if the byte has changed, then send it! */
		if (*TMbuffer != *SPIbuffer)
		{
			if (SPIcommand & (1<<2))
			{
				/* send to TM1638 */
				TMx8_sendData(i<<1, *SPIbuffer, TMx8_STB_PINMASK[SPIcommand&3]);
			}
			else
			{
				/* send to TM1637 */

			}
		}
		*TMbuffer++ = *SPIbuffer++;   /* copy the new data */
	}
	/* send command */

}



/* add a new command for a led
nLed: number of the led
buffer: the 5 bytes for the SPI buffer */
void setRGBLed(uint8_t nLed, uint8_t* buffer)
{
	RGBledsHasChanged = 1;

	/* copy the five bytes */
	RGBleds[ nLed ] = *(struct sRGB_LED*) buffer;

	/* update the blink Event Table for the concerned led */
	uint16_t blinkPatternOfThisLed = RGBleds[ nLed].blinkPattern;
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
void fillRGBBuffer( uint8_t bcycle)
{
	struct cRGB *pBuffer = bufferLeds;
	struct sRGB_LED *pLeds = RGBleds;
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
	static uint8_t SPIcycle = 0;     /* counts the cycles */
	static uint8_t SPIcommand;      /* 1st byte received (indicates which command, and how many other bytes will follow */
	static uint8_t SPIbuffer[8] = {0};    /* buffer (5 bytes for a LED, 8 for display, etc.) */
	static uint8_t SPInbBytes = 0;      /* how many bytes we will receive in the buffer for this command */
	/* copy the data (1st data in SPIcommand, the others in SPIbuffer) */
	if (SPIcycle)
		SPIbuffer[ SPIcycle-1 ] = SPDR;
	else
	{
		/* copy the header*/
		SPIcommand = SPDR;
		/* compute how many bytes we will next receive */
		if ((SPIcommand & 0xF0) == 0b11000000)
			SPInbBytes = 4;     /* set the 7-segment display, 4-byte mode */
		else if ((SPIcommand & 0xF0) == 0b11010000)
			SPInbBytes = 8;     /* set the 7-segment display, 8-byte mode */
		else if ( ((SPIcommand & 0xE0) == 0) && (SPIcommand!=0) )
			SPInbBytes = 5;     /* set RGB Led */
		else
			SPInbBytes = 0;     /* other command requires no extra bytes */
	}
	SPIcycle++;
	/* check if the end of the data transfer */
	if (SPIcycle > SPInbBytes)
	{
		SPIcycle = 0;
		switch (SPIcommand & 0b11000000)
		{
			case 0:
				/* set RGB color */
				if (SPIcommand)
					setRGBLed( SPIcommand-1, SPIbuffer);
				/*else NOP: do nothing */
				break;
			case 0b01000000:
				/* set a led */
				break;
			case 0b10000000:
				/* set the brightness */
				break;
			default:    /* 0b11xxxxxx */
				if ( !(SPIcommand & 0b00100000 ) )
				{
					/* set the display */
					setDisplayTMx(SPIcommand, SPIbuffer);
				}
				else if (SPIcommand & 0b00010000)
				{
					/* clear the display */
				}
				else
				{
					/* turn on/off the display */
				}
		}
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
		if (RGBledsHasChanged || ((blinkEvent >> (cycle>>4))&1) )      /* cycle>>4 -th bit of blinkEvent */
		{
			/* prepare the buffer */
			fillRGBBuffer(cycle>>4);
			ws2812_setleds(bufferLeds, NB_LEDS);
			RGBledsHasChanged = 0;
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

	/* turn off the RGB leds */
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


	TMx8_setup(1);
	//TMx8_sendData(0,0b01101101,TMx8_STB_PINMASK[0]);
	//TMx8_sendData(2,0b00000110,TMx8_STB_PINMASK[0]);
	//TMx8_sendData(1,255,TMx8_STB_PINMASK[0]);

	/* enable interrupts and wait */
	sei();
	while(1);   /*TODO: idle mode? */
}
