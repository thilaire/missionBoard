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






/* data to send through the SPI */
#define SIZE_SPITOSEND NB_TMx8+3+1
 struct {
    uint8_t header;                     /* header of the SPI to send protocol */
	uint8_t OnlyOneByte;                /* data, when it can be in one byte (only one thing has changed) */
	uint8_t TMx8data[NB_TMx8];        /* TMx8 data on line K3 */
	uint8_t ADCdata[3];                 /* ADC value */
	uint8_t IOdata;
}  SPItoSend_data = {0};
uint8_t SPItoSend_nbBytes = 1;     /* nb byte to send: only the header */
uint8_t SPItoSend_cycle = 0;           /* cycle number */


void updateSPItoSendData( uint8_t data, uint8_t index)
{
	uint8_t* SPIbuffer = ((uint8_t*) &SPItoSend_data)+index+2;
	if (data != *SPIbuffer)
	{
		*SPIbuffer = data;
		if (SPItoSend_data.header&0b11110000)
		{
			/* something has already changed */
			SPItoSend_data.header = 0b01110000;
		}
		else
		{
			/* first change. We save it in SPItoSendByte */
			SPItoSend_data.header = 0b00010000 | index;
			SPItoSend_data.OnlyOneByte = data;
		}

		PORTB |= (1<<4);
		_delay_ms(1);
		PORTB &= ~(1<<4);

	}
	/* copy to SPDR if we are not already sending something */
	if (SPItoSend_cycle==0)
	{
		SPDR = SPItoSend_data.header;
		/* determine the nb of bytes to send (including header) from the header */
		SPItoSend_nbBytes = (SPItoSend_data.header>>4) + 1;
	}
}






/* SPI interrupt function */
ISR (SPI_STC_vect)
{
	/* SPI receive data */
	static uint8_t SPIcycle = 0;     /* counts the cycles */
	static uint8_t SPIcommand;      /* 1st byte received (indicates which command, and how many other bytes will follow */
	static uint8_t SPIbuffer[8] = {0};    /* buffer (5 bytes for a LED, 8 for display, etc.) */
	static uint8_t SPInbBytes = 0;      /* how many bytes we will receive in the buffer for this command */

	/* SPI send data */
	static uint8_t *toSendBuffer = ((uint8_t*) &SPItoSend_data)-1;   /* the byte before, so that we can start with the 1st byte for the 1st transaction */

	/* ===== Receive byte ==== */

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

	/* ===== Send (prepare to send next) byte ====== */

	/* increase cycle and data pointer */
	SPItoSend_cycle++;
	toSendBuffer++;
	/* check if it's the end of the buffer */
	if (SPItoSend_cycle==SPItoSend_nbBytes)
	{
		/* re-init the buffer to the beginning of SPItoSend_data */
		toSendBuffer = ((uint8_t*) &SPItoSend_data);
		SPItoSend_cycle=0;
		/* initialize header (nothing to send) */
		SPItoSend_data.header = 0;
		SPItoSend_nbBytes = 1;
	}
	/* skip the next byte if more than one byte (+header) is to sent */
	else if (SPItoSend_cycle==1 && (SPItoSend_nbBytes>2) )
	{
		toSendBuffer++; /* we skip the next byte that is not to send in that mode */
	}
	/* finaly, copy the next byte to SPDR */
	SPDR = *toSendBuffer;



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
	_delay_ms(100);
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


	SPDR = 0;

/*	SPItoSend_data.header = 0b00110000;
	SPItoSend_nbBytes = 4;
	SPItoSend_data.OnlyOneByte = 38;*/
	SPItoSend_data.TMx8data[0] = 100;
	SPItoSend_data.TMx8data[1] = 101;
	SPItoSend_data.TMx8data[2] = 102;
	SPItoSend_data.ADCdata[0] = 127;
	SPItoSend_data.ADCdata[1] = 132;
	SPItoSend_data.ADCdata[2] = 135;
	SPItoSend_data.IOdata = 42;

	/* enable interrupts and wait */
	sei();
	while(1);   /*TODO: idle mode? */
}
