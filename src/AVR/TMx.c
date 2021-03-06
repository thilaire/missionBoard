/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: TMx8.c
       high-level driver for the TM1638 boards
       - manage messages from the SPI
       - get data from the TMx8 and put it in the right order
       - based on the low-level driver (see TM1638.c)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/


#include <avr/io.h>
#include <stdint.h>
#include <util/delay.h>

#include "TMx.h"
#include "TM1638.h"


/* debug */
const uint8_t NUMBER_FONT[] = {
  0b00111111, // 0
  0b00000110, // 1
  0b01011011, // 2
  0b01001111, // 3
  0b01100110, // 4
  0b01101101, // 5
  0b01111101, // 6
  0b00000111, // 7
  0b01111111, // 8
  0b01101111, // 9
  0b01110111, // A
  0b01111100, // B
  0b00111001, // C
  0b01011110, // D
  0b01111001, // E
  0b01110001  // F
};



/* data for TM1637 and TM1638 */

uint8_t TMxDisplay[4*NB_TMx7+8*NB_TMx8] = {0};    /* display data of the TM1637 and TM1638 */

const uint8_t TM1638_STB_PINMASK[NB_TMx8] = { BIT(TM1638_STB_PIN0), BIT(TM1638_STB_PIN1), BIT(TM1638_STB_PIN2), BIT(TM1638_STB_PIN3)};  /* STB0, STB1 and STB2 are on PD5, PD6 and PD7 respectively */

uint8_t TMx8Input[NB_TMx8] = {0};       /* data from the line input K3*/




/* get input data from the TM1638 boards, and returns 1 if something have changed */
uint8_t getDataTMx8(uint8_t nTM, uint8_t* data) {
	uint8_t d;   /* corresponds to K3 byte of the TM */
	uint8_t TMdata; /* bytes received from the TMx8 */

	/* set the TMx8 in read mode */
	clearTM1638_Stb(TM1638_STB_PINMASK[nTM]);
	TM1638_setDataMode(READ_MODE, INCR_ADDR);
	_delay_us(10);  /* wait at least 10µs ? */
	/* get the 4 bytes and put the useful bits (those from K3) in data */
	TMdata = TM1638_getByte();
	d = (TMdata & (BIT(1)|BIT(5))) >> 1;
	TMdata = TM1638_getByte();
	d |= (TMdata & (BIT(1)|BIT(5)));
	TMdata = TM1638_getByte();
	d |= (TMdata & (BIT(1)|BIT(5))) << 1;
	TMdata = TM1638_getByte();
	d |= (TMdata & (BIT(1)|BIT(5))) << 2;
	/* close the connection */
	setTM1638_Stb();

	/* check if K3 has changed	and update SPItoSend datas */
	if (d != TMx8Input[nTM]) {
		TMx8Input[nTM] = d;
		*data = d;
		return 1;
	}
	else {
		return 0;
	}
}


/* TODO: is it really useful to store the data, and check if we need to send each byte or not? */
/* according to the SPI data received, set the display of the TMx (send appropriate command) */
void setDisplayTMx(uint8_t SPIcommand, uint8_t* SPIbuffer)
{
	uint8_t size = (SPIcommand & (1<<4)) ? 8 : 4; /* 4 or 8 bytes */
	uint8_t pos = (SPIcommand & (1<<3))? 4 : 0;      /* 1st or 2nd 4-digit display */
	/* compute the adress of the TM buffer (in TMxDisplay) */
	uint8_t* TMbuffer;
	if (SPIcommand & (1<<2))
		TMbuffer = TMxDisplay + 4*NB_TMx7 + (SPIcommand&3)*8 + pos;
	else
		TMbuffer = TMxDisplay + (SPIcommand&3)*4;

	/* loop for every byte sent */
	for( uint8_t i = 0; i<size; i++,pos++)
	{
		/* if the byte has changed, then send it! */
		if ((*TMbuffer) != (*SPIbuffer) )
		{
			if (SPIcommand & (1<<2))
			{
				/* send to TM1638 */
				//TM1638_sendData(pos<<1, *SPIbuffer, 0b1111000);
				TM1638_sendData(pos<<1, *SPIbuffer, TM1638_STB_PINMASK[SPIcommand&3]);
			}
			else
			{
				/* send to TM1637 */
				//TMx7_sendData(pos, *SPIbuffer, SPIcommand&3);

			}
		}
		*TMbuffer++ = *SPIbuffer++;   /* copy the new data */
	}
}

/* according to the SPI data received, set the Leds of the TMx8 (send appropriate command) */
void setLedTMx8(uint8_t SPIcommand)
{
	uint8_t nLed = (SPIcommand & 28)>>2; /* bits 2, 3 and 4 */
	TM1638_sendData(
		(nLed<<1)+1,                              /* address in memory */
	    (SPIcommand & BIT(5)) >> 5,               /* data set to 0 or 1 according to bit 6 (set to 1 only, because bit 0 corresponds to SEG9 used on the board) */
	    TM1638_STB_PINMASK[SPIcommand&3]);
}

/* according to the SPI data received, set the brightness of the TMx (send appropriate command) */
void setBrightnessTMx(uint8_t SPIcommand)
{
	uint8_t brightness = (SPIcommand & 56)>>3;   /* bits 3, 4 and 5 */
	if (SPIcommand & (1<<2))
	{
		/* send to TM1638 */
		TM1638_turnOn(brightness, TM1638_STB_PINMASK[SPIcommand&3]);
	}
	else
	{
		/* send to TM1637 */
		//TMx7_turnOn(brightness, SPIcommand&3);
	}
}

/* according to the SPI data received, turn off the TMx (send appropriate command) */
void turnOffTMx(uint8_t SPIcommand)
{
	if (SPIcommand & (1<<2))
	{
		/* send to TM1638 */
		TM1638_turnOff(TM1638_STB_PINMASK[SPIcommand&3]);
	}
	else
	{
		/* send to TM1637 */
		//TMx7_turnOff(SPIcommand&3);
	}
}

/* according to the SPI data received, clear the TMx (send appropriate command) */
void clearTMx(uint8_t SPIcommand)
{
	if (SPIcommand & (1<<2))
	{
		/* send to TM1638 */
		TM1638_clearDisplay(TM1638_STB_PINMASK[SPIcommand&3]);
	}
	else
	{
		/* send to TM1637 */
		//TMx7_clearDisplay(SPIcommand&3);
	}
}

/* set up the TMx8 and TMx7 boards */
void setupTMx(uint8_t brightness)
{
	TM1638_setup(brightness);
}

/* when the RPi ask for all the data
we simply change the value stored in TMx8Input */
void switchDataTMx()
{
	for( uint8_t i=0; i<NB_TMx8; i++)
	{
		TMx8Input[i] = ~TMx8Input[i];   /* switch the bits */
	}
}