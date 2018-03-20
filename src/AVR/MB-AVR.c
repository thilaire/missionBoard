/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: MB-AVR.c
       Main file of the AVR code
       - SPI interrupt
       - Timer interrupt (for the polling)

       configured for an ATtiny88 (see the doc for the IOs)
       running at 8Mhz
       Fuses: E=07, H=DF, L=EE

Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/


#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>

#include <string.h>
#include "RGB.h"
#include "TMx.h"
#include "ADC.h"



//debug
extern const uint8_t NUMBER_FONT[];


/* data to send through SPI */
uint8_t SPISend_header = 0;
uint8_t SPISend_cycle = 0;
uint8_t SPISend_data[2] = {0};
const uint8_t NB_BYTES[4] = { 0b00000000, 0b00010000, 0b00010000, 0b00100000};



/* SPI interrupt function */
ISR (SPI_STC_vect) {
	/* SPI receive data */
	static uint8_t SPIRec_cycle = 0;     /* counts the cycles */
	static uint8_t SPIRec_command;      /* 1st byte received (indicates which command, and how many other bytes will follow */
	static uint8_t SPIRec_buffer[8] = {0};    /* buffer (5 bytes for a LED, 8 for display, etc.) */
	static uint8_t SPIRec_nbBytes = 0;      /* how many bytes we will receive in the buffer for this command */

	/* ===== Receive byte ==== */

	/* copy the data (1st data in SPIRec_command, the others in SPIRec_buffer) */
	if (SPIRec_cycle)
		SPIRec_buffer[ SPIRec_cycle-1 ] = SPDR;
	else {
		/* copy the header*/
		SPIRec_command = SPDR;
		/* compute how many bytes we will next receive */
		if ((SPIRec_command & 0xF0) == 0b11000000)
			SPIRec_nbBytes = 4;     /* set the 7-segment display, 4-byte mode */
		else if ((SPIRec_command & 0xF0) == 0b11010000)
			SPIRec_nbBytes = 8;     /* set the 7-segment display, 8-byte mode */
		else if ( ((SPIRec_command & 0xE0) == 0) && (SPIRec_command!=0) && (SPIRec_command!=31) )
			SPIRec_nbBytes = 5;     /* set RGB Led */
		else
			SPIRec_nbBytes = 0;     /* other command requires no extra bytes */
	}
	SPIRec_cycle++;
	/* check if the end of the data transfer */
	if (SPIRec_cycle > SPIRec_nbBytes) {
		SPIRec_cycle = 0;
		switch (SPIRec_command & 0b11000000) {
			case 0:
				if (SPIRec_command) {
					if (SPIRec_command == 0b00011111) {
						turnOffRGB();
					}
					else {
						/* set RGB color */
						setRGBLed( SPIRec_command-1, SPIRec_buffer);
					}
				}
				/*else NOP: do nothing */
				break;
			case 0b01000000:
				/* set a led */
				setLedTMx8(SPIRec_command);
				break;
			case 0b10000000:
				/* set the brightness and turn on*/
				setBrightnessTMx(SPIRec_command);
				break;
			default:    /* 0b11xxxxxx */
				if ( !(SPIRec_command & 0b00100000 ) ) {
					/* set the display */
					setDisplayTMx(SPIRec_command, SPIRec_buffer);
				}
				else if (SPIRec_command == 0b11110000) {
					/* ask for the AVR datas (TMx8 and potentiometers) */
					/* we reset the data, so that they will be send again in the next polling cycles */
					switchDataTMx();
					switchDataADC();
				}
				else if ((SPIRec_command & 0b00011000) == 0) {
					/* turn off the display */
					turnOffTMx(SPIRec_command);
				}
				else if ((SPIRec_command & 0b00011000) == 8) {
					/* clear the display */
					clearTMx(SPIRec_command);
				}


		}
	}

	/* ===== Send (prepare to send next) byte ====== */
	if (SPISend_cycle >= (SPISend_header>>4)) {
		/* end of the cycle; start over */
		SPISend_cycle = 0;
		SPISend_header = 0;
		SPDR = 0;
	}
	else {
		/* otherwise continue to send data */
		SPDR = SPISend_data[SPISend_cycle];
		SPISend_cycle++;
	}

}


/* get the data from the TMx8 and update SPIsend data accordingly */
void updateDataTMx8(uint8_t nTM) {
	uint8_t data;
	if (getDataTMx8(nTM, &data)) {
		/* copy the data in the right place (header is 1 if Pot has changed, 0 otherwise) */
		SPISend_data[SPISend_header>>2] = data;
		/* TMx8 data has changed */
		SPISend_header |= 0b00001000;
	}
}


/* get the data from the ADC and update SPIsend data accordingly */
void updateADC(uint8_t cycle) {
	uint8_t data;

	if (cycle==3) {  /* switches on analog input*/
		if (getADCSwitches(&data)) {
			/* copy the data in the first byte */
			SPISend_data[0] = data;
			/* ADC data has changed */
			SPISend_header |= 0b00001000;
		}
	}
	else if (getADC(cycle, &data)) { /* regular potentiometer */
		/* copy the data in the first byte */
		SPISend_data[0] = data;
		/* ADC data has changed */
		SPISend_header |= 0b00000100;
	}
}





/* Timer 1 interrupt function (when TIMER1==OCR1A) */
ISR (TIMER1_COMPA_vect  ) {
	static uint8_t cycle=0;
	static uint8_t blinkCycle = 0;

	/* initialize SPI header */
	SPISend_header = cycle&3;

	/* acquire Potentiometer */
	updateADC(cycle&3);
	/* acquire data from TMx8 */
	updateDataTMx8(cycle&3);
	/* run ADC for the next cycle */
	runADC((cycle+1)&3);

	/* run blinking cycle */
	if ((cycle&63) == 63) {
		/* check if we need to send data to the led (something has changed since previous cycle ?) */
		if (RGBshouldBeUpdated(blinkCycle)) {
			/* prepare the buffer */
			fillRGBBuffer(blinkCycle);
			updateRGB();
		}
		blinkCycle = (blinkCycle+1) & 15;   /* only the 4 LSB */
	}

	/* update SPI header and SPDR (next byte to be sent)*/
	SPISend_header &= 0b11001111;
	SPISend_header |= NB_BYTES[SPISend_header>>2];
	SPDR = SPISend_header;

	/* pulse the Raspberry Pi if something has changed */
	if (SPISend_header&0b00001100) {
		PORTC |= 1;
		//_delay_us(1);
		PORTC &= ~1;
	}
	/* next cycle */
	cycle++;
}


int main(void) {
	/* configure inputs/outputs */
	DDRB = 0b11010011;       /* PB0, PB1, PB4, PB6 and PB7 are outputs */
	DDRC = 0b10000001;       /* PC0 and PC7 are outputs */
	DDRD = 0b11111111;      /* PD0 to PD7 are outputs */

	/* configure the USI */
	SPCR |= (1<<SPIE) | (1<<SPE);
	SPDR = 0;   /* next byte to send */

	/* turn off the RGB leds */
	_delay_ms(10);
	updateRGB();

	/* blink LED C7 (debug LED) to tell we are alive */
	PORTC |= (1U<<7);
	_delay_ms(500);
	PORTC &= ~(1U<<7);

	/* configure timer1, 16bits mode, Prescaler=1/8
	interrupt after 15625 ticks (compare for channel A) */
	TCCR1B = (1U<<CS11) | (1U<<WGM12);     /* prescaler = 1/8 and Clear Timer on Compare match (CTC) T*/
	TCCR1C = (1U<<FOC1A);    /* channel A */
	OCR1A = 15625;//31250;              /* 15625 ticks @ 1MHz -> 15.625ms */
	TIMSK1 = (1U<<OCIE1A);      /* set interrupt on Compare channel A */

	/* setup the TMx8 and TMx7 boards */
	setupTMx(1);
	initADC();
	runADC(0);


	SPDR = 0;
	//uint8_t clkMask = 0b00000111;
	//TM1637_setup(clkMask);
	//TM1637_write(255,255,255,255, clkMask);

    //TM1637_SERIAL_INIT;

	//led_print(0, "tE5t");


	/* enable interrupts and wait */
	sei();
	while(1);   /*TODO: idle mode? */
}
