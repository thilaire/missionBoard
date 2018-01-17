/*
* Author: T. HILAIRE
*
* driver for TM1638 board and the SPI protocol used
*
* Licence: GPL v3
*/


#include <avr/io.h>
#include <util/delay.h>

#include "TMx8.h"
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

const uint8_t TM1638_STB_PINMASK[3] = { BIT(TM1638_STB_PIN0), BIT(TM1638_STB_PIN1), BIT(TM1638_STB_PIN2)};  /* STB0, STB1 and STB2 are on PD5, PD6 and PD7 respectively */








/* data to send through the SPI */
 struct {
	uint8_t TMx8K1[NB_TMx8];        /* TMx8 data on line K1 */
	uint8_t TMx8K2[NB_TMx8];        /* TMx8 data on line K2 */
	uint8_t dataADC[3];                 /* ADC value */
}  SPItoSend = {0};
uint8_t SPItoSendHeader = 0;
uint8_t SPItoSendcycle = 0;
uint8_t SPItoSendByte = 0;      /* byte to send, when we only send one byte */


/* get input data from the TM1638 boards */
void getDataTMx8(uint8_t nTM)
{
	uint8_t K1=0, K3=0;
	uint8_t data;


	/* set the TMx8 in read mode */
	clearTM1638_Stb(TM1638_STB_PINMASK[nTM]);
	TM1638_setDataMode(READ_MODE, INCR_ADDR);
	_delay_us(20);  /* wait at least 10µs ? */
	/* get the 1st byte and put it in K1 and K2 */
	data = TM1638_getByte();
uint8_t data1 = data;
	K3 = (data & BIT(3)) >> 3;
	K3 |= (data & BIT(7)) >> 6;
	K1 = (data & BIT(1)) >> 1;
	K1 |= (data & BIT(5)) >> 4;
	/* get the 2nd byte and put it in K1 and K2 */
	data = TM1638_getByte();
uint8_t data2 = data;
	K3 |= (data & BIT(3)) >> 1;
	K3 |= (data & BIT(7)) >> 4;
	K1 |= (data & BIT(1)) << 1;
	K1 |= (data & BIT(5)) >> 2;
	/* get the 3rd byte and put it in K1 and K2 */
	data = TM1638_getByte();
uint8_t data3 = data;
	K3 |= (data & BIT(3)) << 1;
	K3 |= (data & BIT(7)) >> 2;
	K1 |= (data & BIT(1)) << 3;
	K1 |= (data & BIT(5));
	/* get the last byte and put it in K1 and K2 */
	data = TM1638_getByte();
uint8_t data4 = data;
	K3 |= (data & BIT(3)) << 3;
	K3 |= (data & BIT(7));
	K1 |= (data & BIT(1)) << 5;
	K1 |= (data & BIT(5)) << 2;
	/* close the connection */
	setTM1638_Stb();

	/* check if K1 and K2 has changed
	and update SPItoSend datas */
	if (K1 != SPItoSend.TMx8K1[nTM])
	{
		SPItoSend.TMx8K1[nTM] = K1;
		if (SPItoSendHeader)
		{
			/* something has already changed */
			SPItoSendHeader = 0b10000000;
		}
		else
		{
			/* first change. We save it in SPItoSendByte */
			SPItoSendHeader = 0b01000000 | nTM;
			SPItoSendByte = K1;
		}
	}
	if (K3 != SPItoSend.TMx8K2[nTM])
	{
		SPItoSend.TMx8K2[nTM] = K3;
		if (SPItoSendHeader)
		{
			/* something has already changed */
			SPItoSendHeader = 0b10000000;
		}
		else
		{
			/* first change. We save it in SPItoSendByte */
			SPItoSendHeader = 0b01000100 | nTM;
			SPItoSendByte = K3;
		}
	}
	/* copy to SPDR if we are not already sending something */
	if (SPItoSendcycle==0)
		SPDR = SPItoSendHeader;


/* debug */
TM1638_sendData(0, K1, TM1638_STB_PINMASK[0]);
TM1638_sendData(2, K3, TM1638_STB_PINMASK[0]);
TM1638_sendData(8, data1, TM1638_STB_PINMASK[0]);
TM1638_sendData(10, data2, TM1638_STB_PINMASK[0]);
TM1638_sendData(12, data3, TM1638_STB_PINMASK[0]);
TM1638_sendData(14, data4, TM1638_STB_PINMASK[0]);

}



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