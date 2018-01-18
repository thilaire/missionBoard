/*
* Author: T. HILAIRE
*
* Licence: GPL v3
*/

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include <string.h>
#include "RGB.h"
#include "TMx8.h"


extern uint8_t SPItoSendHeader;
extern uint8_t SPItoSendcycle;
extern uint8_t SPItoSendByte;







/* SPI interrupt function */
ISR (SPI_STC_vect)
{
	static uint8_t SPIcycle = 0;     /* counts the cycles */
	static uint8_t SPIcommand;      /* 1st byte received (indicates which command, and how many other bytes will follow */
	static uint8_t SPIbuffer[8] = {0};    /* buffer (5 bytes for a LED, 8 for display, etc.) */
	static uint8_t SPInbBytes = 0;      /* how many bytes we will receive in the buffer for this command */

	static uint8_t SPItoSendMode = 0;
	static uint8_t* SPItoSendBuffer;

//	/* prepare next byte to send */
//	if (SPItoSendcycle==0)
//	{
//		SPDR = SPItoSendHeader;
//		SPItoSendMode = SPItoSendHeader & 0b11000000;
//	}
//	else
//	{
//		if (SPItoSendMode == 0b01000000)
//		{
//			SPDR = SPItoSendByte;
//			SPItoSendcycle = 0;
//		}
//		else
//		{
//			SPDR = *SPItoSendBuffer++;
//			SPItoSendcycle++;
//			if (SPItoSendcycle==9)
//				SPItoSendcycle = 0; /* it was the last byte to send */
//		}
//	}

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
				setLedTMx8(SPIcommand);
				break;
			case 0b10000000:
				/* set the brightness and turn on*/
				setBrightnessTMx(SPIcommand);
				break;
			default:    /* 0b11xxxxxx */
				if ( !(SPIcommand & 0b00100000 ) )
				{
					/* set the display */
					setDisplayTMx(SPIcommand, SPIbuffer);
				}
				else if ((SPIcommand & 0b00011000) == 0)
				{
					/* turn off the display */
					turnOffTMx(SPIcommand);
				}
				else if ((SPIcommand & 0b00011000) == 8)
				{
					/* clear the display */
					clearTMx(SPIcommand);
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
		/* run capture ADC0 and TM1638[0] */
		getDataTMx8(0);
	}
	else if ((cycle&3) == 1)
	{
		/* run capture ADC1 and TM1638[1] */
		//getDataTMx8(1);
	}
	else if ((cycle&3) == 2)
	{
		/* run capture ADC2 and TM1638[2] */
		//getDataTMx8(2);
	}
	else
	{   /* end capture ADC2 */
		/* blinking cycle */
		if ((cycle&15) == 3)
		{
			/* check if we need to send data to the led (something has changed since previous cycle ?) */
			if (RGBshouldBeUpdated(cycle>>4))
			{
				/* prepare the buffer */
				fillRGBBuffer(cycle>>4);
				updateRGB();
			}
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
	SPDR = 0;   /* next byte to send */

	/* turn off the RGB leds */
	updateRGB();

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

	/* setup the TMx8 and TMx7 boards */
	setupTMx(1);



	/* enable interrupts and wait */
	sei();
	while(1);   /*TODO: idle mode? */
}
