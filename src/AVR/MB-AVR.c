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
#include <avr/cpufunc.h>

#include <string.h>



#include "MB-AVR.h"
#include "RGB.h"
#include "TMx.h"
#include "ADC.h"


/* debug */
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




/* constants and functions for powering the Raspberry Pi */
#define RPI_OFF 0
#define RPI_BOOTING 1
#define RPI_ON 2
#define RPI_SHUTING 3
inline __attribute__((always_inline)) static void turnOn_RPi() { PORTD |= (1U<<4); }
inline __attribute__((always_inline)) static void turnOff_RPi() { PORTD &= ~(1U<<4); }
uint8_t RPiPower = RPI_OFF;     /* state of the Raspberry Pi power (see constants) */
uint8_t switchPower = 0;        /* current state of the switch (to catch its change) */



/* circular buffer for the data received from SPI */
#define SPI_BUFFER_LENGTH 8
#define SPI_BUFFER_MASK 0b00000111
SPImessage SPIbuffer[SPI_BUFFER_LENGTH];
uint8_t SPInextMsg = 0;     /* index of the next message */
uint8_t SPIpop = 0;         /* index of the current message, to be pop */


/* SPI interrupt function */
ISR (SPI_STC_vect) {
	/* some static data */
	static uint8_t cycle = 0;     /* counts the cycles */
	static uint8_t nbBytes = 0;      /* how many bytes we will receive in the buffer for this command */
	static uint8_t* nextData = &(SPIbuffer[0].command);     /* pointer to the byte to be filled */

	/* copy the data  */
	uint8_t byte = SPDR;
	*(nextData++) = byte;
	/* compute how many bytes we will next receive */
	if (cycle==0) {
		if ((byte & 0xF0) == 0b11000000)
			nbBytes = 4;     /* set the 7-segment display, 4-byte mode */
		else if ((byte & 0xF0) == 0b11010000)
			nbBytes = 8;     /* set the 7-segment display, 8-byte mode */
		else if ( ((byte & 0xE0) == 0) && (byte!=0) && (byte!=31) )
			nbBytes = 5;     /* set RGB Led */
		else
			nbBytes = 0;     /* other commands do not require extra bytes */
	}
	/* check if the end of the data transfer */
	cycle++;
	if (cycle > nbBytes) {
		cycle = 0;
		/* increase the index of the next message (circular buffer) */
		SPInextMsg = (SPInextMsg+1) & SPI_BUFFER_MASK;
		/* TODO: test overflow ! */
		if (SPInextMsg == SPIpop) {
			uint8_t val[4] = {0xFF, 0xBB, 0xFF, 0xBB};
			setDisplayTMx(0b11000100,val);
			while(1); /* block everything */
		}
		/* point to the next message */
		nextData = &(SPIbuffer[SPInextMsg].command);
	}

	/* send the next byte */
	SPDR = byte - 2;

}
//
//
///* get the data from the TMx8 and update SPIsend data accordingly */
//void updateDataTMx8(uint8_t nTM) {
//	uint8_t data;
//	if (getDataTMx8(nTM, &data)) {
//		/* copy the data in the right place (header is 1 if Pot has changed, 0 otherwise) */
//		SPISend_data[SPISend_header>>2] = data;
//		/* TMx8 data has changed */
//		SPISend_header |= 0b00001000;
//	}
//}
//
//
///* get the data from the ADC and update SPIsend data accordingly */
//void updateADC(uint8_t cycle) {
//	uint8_t data;
//
//	if (cycle==3) {  /* switches on analog input*/
//		if (getADCSwitches(&data)) {
//			/* copy the data in the first byte */
//			SPISend_data[0] = data;
//			/* ADC data has changed */
//			SPISend_header |= 0b00001000;
//		}
//	}
//	else if (getADC(cycle, &data)) { /* regular potentiometer */
//		/* copy the data in the first byte */
//		SPISend_data[0] = data;
//		/* ADC data has changed */
//		SPISend_header |= 0b00000100;
//	}
//}
//




/* Timer 1 interrupt function (when TIMER1==OCR1A) */
ISR (TIMER1_COMPA_vect  ) {
//	static uint8_t cycle=0;
//	static uint8_t blinkCycle = 0;
//
//	/* initialize SPI header */
//	SPISend_header = cycle&3;
//
//	/* acquire Potentiometer */
//	updateADC(cycle&3);
//	/* acquire data from TMx8 */
//	updateDataTMx8(cycle&3);
//	/* run ADC for the next cycle */
//	runADC((cycle+1)&3);
//
//	/* run blinking cycle */
//	if ((cycle&63) == 63) {
//		/* check if we need to send data to the led (something has changed since previous cycle ?) */
//		if (RGBshouldBeUpdated(blinkCycle)) {
//			/* prepare the buffer */
//			fillRGBBuffer(blinkCycle);
//			updateRGB();
//		}
//		/* check if the power LED need to blink */
//		if (RPiPower&1) {
//			//setLedTMx8(68 | (blinkCycle&1)<<5); /* turn on or off the led T1_LED, according to blinkCycle */
//			if (blinkCycle&1)
//				setBrightnessTMx(0b10001100);
//			else
//				turnOffTMx(0b11100100);
//
//		}
//		/* update the blink cycle */
//		blinkCycle = (blinkCycle+1) & 15;   /* only the 4 LSB */
//	}
//
//	/* update SPI header and SPDR (next byte to be sent)*/
//	SPISend_header &= 0b11001111;
//	SPISend_header |= NB_BYTES[(SPISend_header>>2)&3];
//
//	/* check if the RPi has shut down */
//	if (RPiPower == RPI_SHUTING && (PINC&1)==0) {
//		_delay_ms(5000);   /* TODO: need to know when the RPi is completly off to turn off the relay (instead of waiting 10s) */
//		//turnOff_RPi();
//	}
//
//	/* check if the power switch has changed (overset SPDR if necessary) */
//	if ((PINC&2) != switchPower) {
//		switchPower = PINC&2;
//		if (RPiPower == RPI_OFF) {
//			/* turn on the RPi */
//			turnOn_RPi();
//			RPiPower = RPI_BOOTING;
//			/* display "boot" */
//			uint8_t boot[4] = {124,92,92,120};
//			setDisplayTMx(0b11000100,boot);
//			setLedTMx8(100);
//		}
//		else if (RPiPower == RPI_ON) {
//			/* change PC0 to input with pull-up */
//			DDRC &= ~(0b00000001);
//			//PORTC |= 0b00000001;
//			/* now, we are shuting down the RPi */
//			RPiPower = RPI_SHUTING;
//			SPISend_header = 0b10000000;
//			/* display "OFF" */
//			uint8_t off[4] = {92,113,113,0};
//			clearTMx(0b11101100);
//			setDisplayTMx(0b11000100,off);
//			setLedTMx8(100);
//		}
//	}
//
//	/* pulse the Raspberry Pi if something has changed */
//	if (SPISend_header&0b10001100) {
//		PORTC |= 1;
//		//_delay_us(1);
//		PORTC &= ~1;
//	}
//
//	/* next cycle */
//	cycle++;
//	/* update SPDR with the datat to be sent */
//	SPDR = SPISend_header;
}


int main(void) {
	/* configure inputs/outputs */
	DDRB = 0b11010011;       /* PB0, PB1, PB4, PB6 and PB7 are outputs */
	DDRC = 0b10000001;       /* PC0 and PC7 are outputs */
	DDRD = 0b11111111;      /* PD0 to PD7 are outputs */

	/* configure the USI */
	SPCR |= (1<<SPIE) | (1<<SPE);
	SPDR = 0;   /* next byte to send */

	/* powering the Raspberry Pi */
	switchPower = PINC&2;
	if (!switchPower) {
		turnOn_RPi();
		RPiPower = RPI_ON;
	}

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
	/* TODO: clear the display */
	initADC();
	runADC(0);

	/* turn on the led T1_LED if the RPi is already running */
	if (RPiPower == RPI_ON) {
		setLedTMx8(100);
	}

	SPDR = 0;

	/* enable interrupts and wait */
	sei();

	/* loop to unstack commands from the SPI buffer */
	uint8_t val[4] = {0,0,0,0};
				uint8_t val2[4] = {0,0,0,0};
			val2[1] = NUMBER_FONT2[SPInextMsg];
			val2[2] = NUMBER_FONT2[SPIpop];
			//setDisplayTMx(0b11001100,val2);
	while(1)
	{
		/* test */
		_NOP();

		/* check if there are some message available */
		if (SPInextMsg != SPIpop)
		{
			/* treat it, according to its 1st byte (command)*/
			SPImessage* msg = &(SPIbuffer[SPIpop]);


			switch (msg->command & 0b11000000) {
				case 0:
					if (msg->command) {
						if (msg->command == 0b00011111) {
							turnOffRGB();
						}
						else {
							/* set RGB color */
							setRGBLed(msg->command-1, msg->data);
						}
					}
					/*else NOP: do nothing */
					break;
				case 0b01000000:
					/* set a led */
					setLedTMx8(msg->command);
					break;
				case 0b10000000:
					/* set the brightness and turn on*/
					setBrightnessTMx(msg->command);
					break;
				default:    /* 0b11xxxxxx */
					if ( !(msg->command & 0b00100000 ) ) {
						/* set the display */

						setDisplayTMx(msg->command, msg->data);
					}
					else if (msg->command == 0b11110000) {
						/* ask for the AVR datas (TMx8 and potentiometers) */
						/* we reset the data, so that they will be send again in the next polling cycles */
						for(int i=0; i<8; i++)
							clearTMx(i);
						switchDataTMx();
						switchDataADC();
					}
					else if ((msg->command & 0b00011000) == 0) {
						/* turn off the display */
						turnOffTMx(msg->command);
					}
					else if ((msg->command & 0b00011000) == 8) {
						/* clear the display */
						clearTMx(msg->command);
					}
			}
			/* increase the index of the current msg */
			SPIpop = (SPIpop+1) & SPI_BUFFER_MASK;
		}

	}

}
