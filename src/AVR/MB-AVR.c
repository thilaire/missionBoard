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
#include <util/atomic.h>

#include <string.h>



#include "RGB.h"
#include "TMx.h"
#include "ADC.h"


/* debug */
//TODO: to remove at the end
//const uint8_t NUMBER_FONT2[] = {
//  0b00111111, // 0
//  0b00000110, // 1
//  0b01011011, // 2
//  0b01001111, // 3
//  0b01100110, // 4
//  0b01101101, // 5
//  0b01111101, // 6
//  0b00000111, // 7
//  0b01111111, // 8
//  0b01101111, // 9
//  0b01110111, // A
//  0b01111100, // B
//  0b00111001, // C
//  0b01011110, // D
//  0b01111001, // E
//  0b01110001  // F
//};


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
#define SPI_RECV_SIZE 32
#define SPI_RECV_MASK 0b00011111
volatile struct {
	uint8_t buffer[SPI_RECV_SIZE];  /* buffer */
	uint8_t read;     /* index of the next byte to read */
	uint8_t write;    /* index of the next byte to be written */
	uint8_t end;    /* index of the end of the message, 0xFF means that it is not yet computed */
	uint8_t flag;       /* flag set to 1 when a byte is received */
} SPIRecv = {.buffer={0}, .read=0, .write=0, .end = 0xFF, .flag=0};

/* circular buffer for the data send through SPI */
#define SPI_SEND_SIZE 8
#define SPI_SEND_MASK 0b00000111
volatile struct {
	uint8_t buffer[SPI_SEND_SIZE];
	uint8_t read;
	uint8_t write;
} SPISend = {.buffer={1,2,3,4,5,6,7,8}, .read=0, .write=0};


/* timer for the polling */
volatile uint8_t timerFlag = 0;     /* flag set to 1 when a sampling occurs */
volatile uint8_t cycle = 0;  /* timer cycle: 4 MSB gives blinking cycle, the other the what-to-do cycle */



/* SPI interrupt function */
ISR (SPI_STC_vect) {
	/* copy the data  */
	SPIRecv.buffer[SPIRecv.write] = SPDR;

	/* increase the write index */
	SPIRecv.write = (SPIRecv.write+1) & SPI_RECV_MASK;

	/* check overflow */
	if (SPIRecv.write == SPIRecv.read) {
		/* TODO: should never happen. When sure, remove this test */
		uint8_t val[4] = {0xFF, 0xBB, 0xFF, 0xBB};
		setDisplayTMx(0b11000100,val);
		while(1); /* block everything */
	}

	/* prepare the next byte to send */
	if (SPISend.read == SPISend.write) {
		SPDR = 0;
	} else {
		SPDR = SPISend.buffer[SPISend.read];
		SPISend.read = (SPISend.read+1) & SPI_SEND_MASK;
	}


	/* set the flag (to tell that we have receive something) */
	SPIRecv.flag = 1;
}


/* called when we received a new byte from SPI */
void SPIRecv_TreatByte() {

	uint8_t data[8] = {0};
	uint8_t command = 0;
	static uint8_t nbBytes = 0;

	/* clear the SPI flag */
	SPIRecv.flag = 0;

	/* compute the index of the end of the message */
	if ( (SPIRecv.end == 0xFF) ) { //&& (SPIwrite == ((SPIread+1)&SPI_BUFFER_MASK)) ) {
		command = SPIRecv.buffer[SPIRecv.read];
		if ((command & 0xF0) == 0b11000000) {
			SPIRecv.end = (SPIRecv.write + 4) & SPI_RECV_MASK;     /* set the 7-segment display, 4-byte mode */
			nbBytes = 4;
		}
		else if ((command & 0xF0) == 0b11010000) {
			SPIRecv.end = (SPIRecv.write + 8) & SPI_RECV_MASK;     /* set the 7-segment display, 8-byte mode */
			nbBytes = 8;
		}
		else if ( ((command & 0xE0) == 0) && (command!=0) && (command!=31) ) {
			SPIRecv.end = (SPIRecv.write + 5) & SPI_RECV_MASK;     /* set RGB Led */
			nbBytes = 5;
		}
		else {
			SPIRecv.end = SPIRecv.write;     /* other commands do not require extra bytes */
			nbBytes = 0;
		}
	}
	/* treat the message when it is complete */
	if (SPIRecv.write == SPIRecv.end) {
	//if (((uint8_t) (SPIwrite-SPIread) & SPI_BUFFER_MASK) >= ((uint8_t) (SPIend-SPIread) & SPI_BUFFER_MASK)) {
		/* get the command and copy the data */
		command = SPIRecv.buffer[SPIRecv.read];
		for(uint8_t i=0; i<nbBytes; i++)
			data[i] = SPIRecv.buffer[(SPIRecv.read+1+i)&SPI_RECV_MASK];

		/* treat it, according to its 1st byte (command)*/
		switch (command & 0b11000000) {
			case 0:
				if (command) {
					if (command == 0b00011111) {
						turnOffRGB();
					}
					else {
						/* set RGB color */
						setRGBLed(command-1, data);
					}
				}
				/*else NOP: do nothing */
				break;
			case 0b01000000:
				/* set a led */
				setLedTMx8(command);
				break;
			case 0b10000000:
				/* set the brightness and turn on*/
				setBrightnessTMx(command);
				break;
			default:    /* 0b11xxxxxx */
				if ( !(command & 0b00100000 ) ) {
					/* set the display */
					setDisplayTMx(command, data);
				}
				else if (command == 0b11110000) {
					/* ask for the AVR datas (TMx8 and potentiometers) */
					/* we reset the data, so that they will be send again in the next polling cycles */
					for(int i=0; i<8; i++)
						clearTMx(i);
					switchDataTMx();
					switchDataADC();
				}
				else if ((command & 0b00011000) == 0) {
					/* turn off the display */
					turnOffTMx(command);
				}
				else if ((command & 0b00011000) == 8) {
					/* clear the display */
					clearTMx(command);
				}
		}
		/* increase the index of the current msg */
		SPIRecv.read = SPIRecv.end;
		SPIRecv.end = 0xFF;
	}
}


/* add a new data in the SPI Send buffer */
void SPISendData(uint8_t header, uint8_t data) {
	/* update the SPDR (if required) */
ATOMIC_BLOCK(ATOMIC_FORCEON)
{
	if (SPISend.read == SPISend.write) {
		SPDR = header;
		SPISend.read = (SPISend.read+1) & SPI_SEND_MASK;
	}
	/* copy the data in the right place */
	SPISend.buffer[SPISend.write] = header;
	SPISend.buffer[SPISend.write+1] = data;       /* SPI_SEND_SIZE is even, no need to mask the +1 */
	/* increase SPISENDwrite by 2 and check for overflow
	But we need to check overflow after each increase because SPISENDread can be odd or even
	(depending if a first byte has been sent or not) */
//	SPISend.write = (SPISend.write+1) & SPI_SEND_MASK;
//	if (SPISend.write == oldSPISENDread) {
//		/* TODO: should never happen. When sure, remove this test */
//		uint8_t val[4] = {0xBB, 0xFF, 0xBB, 0xFF};
//		setDisplayTMx(0b11000100,val);
//	}
//	SPISend.write = (SPISend.write+1) & SPI_SEND_MASK;
//	if (SPISend.write == oldSPISENDread) {
//		/* TODO: should never happen. When sure, remove this test */
//		uint8_t val[4] = {0xBB, 0xFF, 0xBB, 0xFF};
//		setDisplayTMx(0b11000100,val);
//	}
	SPISend.write = (SPISend.write+2) & SPI_SEND_MASK;
}
	/* pulse the Raspberry Pi to tell that something has changed */
	PORTC |= 1;
	_delay_us(1);
	PORTC &= ~1;

}



/* Timer 1 interrupt function (when TIMER1==OCR1A) */
ISR (TIMER1_COMPA_vect  ) {
	/* increase the cycle and set the flag. That's all */
	/* the treatment is done outside of the interrupt, in order to be able to be interrupted by SPI interrupt */
	cycle++;
	timerFlag = 1;
}


void doTimer()
{
	uint8_t data;
	uint8_t nTM = cycle&3;

	/* clear the timer flag */
	timerFlag = 0;

//	/* acquire Potentiometer */
//	if (getADC(nTM, &data)) {
//	    SPISendData( 0b01000000 | nTM, data);
//	}
//
//	/* acquire data from TMx8 */
//	if (getDataTMx8(nTM, &data)) {
//		SPISendData( 0b01000100 | nTM, data);
//	}


	/* run ADC for the next cycle */
//	runADC((cycle+1)&3);

	/* run blinking cycle */
	if ((cycle&15) == 3) {
		uint8_t blinkCycle = cycle>>4;
		/* check if we need to send data to the led (something has changed since previous cycle ?) */
		if (RGBshouldBeUpdated(blinkCycle)) {
			/* tell the RPi we will be busy for few micro-seconds (interruptions are disabled during
			the call to `ws2812_sendarray_mask`, so we won't be able to send any data back */
			PORTC |= (1U<<7);
			/* prepare the buffer */
			fillRGBBuffer(blinkCycle);
			updateRGB();
			/* tell the RPi we have finished */
			PORTC &= ~(1U<<7);
		}
//		/* check if the power LED need to blink */
//		if (RPiPower&1) {
//			//setLedTMx8(68 | (blinkCycle&1)<<5); /* turn on or off the led T1_LED, according to blinkCycle */
//			if (blinkCycle&1)
//				setBrightnessTMx(0b10001100);
//			else
//				turnOffTMx(0b11100100);
//
//		}

}

//	/* check if the RPi has shut down */
//	if (RPiPower == RPI_SHUTING && (PINC&1)==0) {
//		_delay_ms(5000);   /* TODO: need to know when the RPi is completly off to turn off the relay (instead of waiting 10s) */
//		//turnOff_RPi();
//	}

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
//	//SPISend_header = 0b10000000;
//			/* display "OFF" */
//			uint8_t off[4] = {92,113,113,0};
//			clearTMx(0b11101100);
//			setDisplayTMx(0b11000100,off);
//			setLedTMx8(100);
//		}
//	}


//	}
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
	TCCR1B = (1U<<CS10) | (1U<<WGM12);     /* prescaler = 1/1 and Clear Timer on Compare match (CTC) T*/
	TCCR1C = (1U<<FOC1A);    /* channel A */
	OCR1A = 62500;              /* 62500 ticks @ 8MHz -> 7.8125ms -> 1/128s */
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

	while(1) {
		/* TODO: manage to do the same with software interrupt, so don't have to poll the change of the Flag (it should be an interrupt flag, instead) */
		/* check if we have received something */
		if (SPIRecv.flag)
			/* if so, do something */
			SPIRecv_TreatByte();
		/* check if it's time to poll data from ADC and TMx8 (or to blink the leds) */
		else if (timerFlag)
			/* if so, do something */
			doTimer();
	}

}
