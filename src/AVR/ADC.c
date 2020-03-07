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
#include "TMx.h"

const uint8_t NUMBER_FONT2[] = {
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




/* list of midpoint intervals and the associated index
used by ADC-to-switches convertion */
const uint8_t inter[] = {0, 4, 16, 27, 38, 49, 59, 69, 81, 93, 102, 110, 117, 125, 132, 139};
const uint8_t switches[] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15};

uint8_t Pot[3] = {0};       /* data from the ADC inputs */
uint8_t ADCswitches = 0;    /* data from the ADC swithces */

/* initialize the ADC */
void initADC()
{
	ADMUX = 0b01100000 | 5;     /* align left, so that we read 8 MSB bits in ADCH */
	ADCSRB = 0;
	DIDR0 = 0b11000000;     /* reduce power consumption, only ADC2, 3, 4 and 5 are used */
	//ADCSRA = 0b10000100;    /* prescaler=32, so it runs at 250kHz; a conversion takes 25 cycles, or 0.1ms */
	ADCSRA = 0b11000111;
}

/* get the previously run ADC, and return 1 if something has changed */
uint8_t getADC(uint8_t cycle, uint8_t* data)
{
	/* dedicated conversion for the ADC switches
	or direct conversion */
	if (cycle == 3) {
		return getADCSwitches(data);
	} else {

		/* the value is in ADCH */
		*data = ADCH;

		/* compute the difference */
		int8_t diff = Pot[cycle] - *data;
		if ((diff>8) || (diff<-8))
		{
			Pot[cycle] = *data;
			return 1;
		}
		else
			return 0;
		//return  !((diff==0 || diff==1 || diff==2));
	}
}


/* run the ADC (to be aquire in the next cycle */
void runADC(uint8_t cycle)
{
	/* select the ADC: (5-cycle) gives the PIN of the ADC */
	if (cycle==3)
		ADMUX = 0b01100000 | 2;     /* voltage reference = 1.1V */
	else
		ADMUX = 0b01100000 | (5-cycle); /* voltage ref = AVcc = 3.3V */
	/* run it! */
	ADCSRA = 0b11000111;
}


/* when the RPi ask for all the data
we simply change the value stored in Pot and ADCswitches */
void switchDataADC()
{
	for( uint8_t i=0; i<3; i++)
	{
		Pot[i] = ~Pot[i];   /* switch the bits */
	}
	ADCswitches = (~ADCswitches)&15;
}


/* similar to getADC, but for the analog input for the switches (ADC2) */
uint8_t getADCSwitches(uint8_t* data)
{
	/* get the ADC value in ADCH (and 2 LSB bits in ADCL) */
	/* fucking pb !! ADCL must be read before ADCH, otherwise the next conversion is lost!! (see page 179 of the datasheet) */
	//uint8_t adc = ADCL>>6 | ADCH<<2;
	uint8_t adc = ADCL>>7 | ADCH<<1;
	static uint8_t old_adc = 12;

	/* check if the adc differ from less than 2 to the old ADC value */
	int8_t diff = old_adc - adc;
	old_adc = adc;
	if ((diff>1) || (diff<-1))
	{
		*data = ADCswitches;
		return 0;
	}

	/* find the value  associated to the ADC with a dicothomic search
	in the table of midpoints (inter) and values (sw)*/
	uint8_t ind = 8;
	uint8_t lvl = 8;

	while (lvl > 1)
	{
		lvl >>= 1;
		if (adc < inter[ind])
			ind -= lvl;
		else
			ind += lvl;
	}
	/* last iteration */
	if (adc < inter[ind])
		*data = ind-1;
		//*data = switches[ind-1];
	else
		*data = ind;
		//*data = switches[ind];

	/* display value, for debug purpose only
	uint8_t val[4] = {0,0,0,0};
	val[1] = NUMBER_FONT2[(*data)/100];
	val[2] = NUMBER_FONT2[((*data)/10)%10];
	val[3] = NUMBER_FONT2[(*data)%10];
	setDisplayTMx(0b11000100,val);
	uint8_t val2[4] = {0,0,0,0};
	val2[1] = NUMBER_FONT2[(adc)/100];
	val2[2] = NUMBER_FONT2[((adc)/10)%10];
	val2[3] = NUMBER_FONT2[(adc)%10];
	setDisplayTMx(0b11001100,val2); */

	/* check if something has changed */
	if (ADCswitches != *data)
	{
		ADCswitches = *data;
		return 1;
	}
	else
		return 0;
}