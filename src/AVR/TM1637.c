/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: TM1637.h
       low-level driver for the TM1637 chip
       - basic function to driver the TM1637 chip
       - used by the high-level driver (see TMx.c)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/


#include <util/delay.h>
#include "TM1637.h"


void TM1637_setup(uint8_t clkMask)
{
  TM1637_start(clkMask);
  TM1637_writeValue(0x8c,clkMask);
  TM1637_stop(clkMask);

  // clear display
  TM1637_write(0x00, 0x00, 0x00, 0x00,clkMask);
}

void TM1637_write(uint8_t first, uint8_t second, uint8_t third, uint8_t fourth, uint8_t clkMask)
{
  TM1637_start(clkMask);
  TM1637_writeValue(0x44, clkMask);
  TM1637_stop(clkMask);

  TM1637_start(clkMask);
  TM1637_writeValue(0xc0, clkMask);
  TM1637_writeValue(first, clkMask);
/*  TM1637_writeValue(second, clkMask);
  TM1637_writeValue(third, clkMask);
  TM1637_writeValue(fourth, clkMask);*/
  TM1637_stop(clkMask);

    TM1637_start(clkMask);
  TM1637_writeValue(0x89, clkMask);
  TM1637_stop(clkMask);


}

/* send the start signal */
void TM1637_start(uint8_t clkMask)
{
	setTM1637_Clk(clkMask);
	setTM1637_Dio();
	_delay_us(5);  /* wait at least 5µs ? */

	clearTM1637_Clk(clkMask);
	clearTM1637_Dio();
	_delay_us(5);
}


/* send the start signal */
void TM1637_stop(uint8_t clkMask)
{
	clearTM1637_Clk(clkMask);
	clearTM1637_Dio();
	_delay_us(5);

	setTM1637_Clk(clkMask);
	setTM1637_Dio();
	_delay_us(5);
}

uint8_t TM1637_writeValue(uint8_t value, uint8_t clkMask)
{
  for( uint8_t i = 0; i<8; i++)
  {
    clearTM1637_Clk(clkMask);
    _delay_us(5);
    writeTM1637_Dio((value & 1));
    _delay_us(5);
    value >>= 1;
	setTM1637_Clk(clkMask);
    _delay_us(5);
  }

    /* wait for ACK */
    clearTM1637_Clk(clkMask);
    _delay_us(5);

	/* configure DIO in input */
	TM1637_DIO_DDR &= ~(1U<<TM1637_DIO_PIN);
	TM1637_DIO_PORT |= (1U<<TM1637_DIO_PIN);

    setTM1637_Clk(clkMask);
    _delay_us(5);

      uint8_t ack = (TM1637_DIO_PIN == 0);

  	/* put back DIO in output mode */
	TM1637_DIO_DDR |= (1U<<TM1637_DIO_PIN);

    return ack;
}