/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: ADC.c
       utilities function for the ADC
       - run ADC, acquire data and check if it has changed


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/


#include <avr/io.h>
#include <util/delay.h>
#include "ADC.h"


uint8_t Pot[3] = {0};       /* data from the ADC inputs */
uint8_t ADCswitches = 0;

/* initialize the ADC */
void initADC()
{
	ADMUX = 0b01100000;     /* align left, so that we read 8 MSB bits in ADCH */
	ADCSRB = 0;
	DIDR0 = 0b11000011;     /* reduce power consumption, only ADC2, 3, 4 and 5 are used */
	ADCSRA = 0b10000100;    /* prescaler=32, so it runs at 250kHz; a conversion takes 25 cycles, or 0.1ms */
}

/* get the previously run ADC, and update the SPI */
uint8_t getADC(uint8_t cycle, uint8_t* data)
{
	/* the value is in ADCH */
	*data = ADCH;

	/* compute the difference */
	int8_t diff = Pot[cycle] - *data;
	if (diff>5 || diff<-5)
	{
		Pot[cycle] = *data;
		return 1;
	}
	else
		return 0;
	//return  !((diff==0 || diff==1 || diff==2));
}

/* run the ADC (to be aquire in the next cycle */
void runADC(uint8_t cycle)
{
	/* select the ADC: 5-cycle gives the PIN of the ADC */
	if (cycle==3)
		ADMUX = 0b00100000 | 2;     /* voltage reference = 1.1V */
	else
			ADMUX = 0b01100000 | (5-cycle); /* voltage ref = AVcc = 3.3V */
	_delay_us(10);  //ADC circuitery needs time to adapt the voltage reference */
	/* run it! */
	ADCSRA = 0b11000100;
}

/* when the RPi ask for all the data
we simply change the value stored in Pot and ADCswitches */
void switchDataADC()
{
	for( uint8_t i=0; i<3; i++)
	{
		Pot[i] = ~Pot[i];   /* switch the bits */
	}
	ADCswitches = ~ADCswitches;
}


/* similar to getADC, but for the analog input for the switches (ADC2) */
uint8_t getADCSwitches(uint8_t* data)
{
	/* get the ADC value in ADCH */
	uint8_t adc = ADCH;
	/* convert it in 4-bit for the switches */
	if (adc<122)
		*data = (adc+5)>>4;
	else
	{
		uint8_t sh = adc-36;   /* shift*/
		uint8_t sh22 = sh + (sh>>2) + (sh>>3);  /* shift*22*/
		*data = sh22>>4;     /* shift*22/256 */
	}
	/* check if something has changed */
	if (ADCswitches != *data)
	{
		ADCswitches = *data;
		return 1;
	}
	else
		return 0;
}