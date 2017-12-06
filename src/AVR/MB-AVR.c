/*
* Light_WS2812 library example - RGB_blinky
*
* cycles one LED through red, green, blue
*
* This example is configured for a ATtiny85 with PLL clock fuse set and
* the WS2812 string connected to PB4.
*/

#include <util/delay.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include "light_ws2812.h"

/* RGB LEDS */
#define NB_LEDS 20
struct cRGB leds[NB_LEDS] = {0};

//ISR (USI_OVF_vect )                  // SPI interrupts
//{
//	USISR = 0b01000000;     /* reset Overflow Flag and reset USI counter */
//	PORTB |= (1<<6);
//	leds[USIDR].g = 255;
//	val = USIDR;
//	//ws2812_setleds(leds,NB_LEDS);
//	PORTB &= ~(1<<6);
//	USIBR = val+1;
//}

ISR (TIMER0_COMPA_vect )
{
	TCNT0H = 0;
	TCNT0L = 0; /* soft CTC mode */

	if (PORTB&(1<<6))
		PORTB &= ~(1<<6);
	else
		PORTB |= (1<<6);

}

int main(void)
{

	#ifdef DEBUG
	leds[12].g = 255;
	#endif

	/* configure inputs/outputs */
	DDRA = 0b00000110;       /* PA1 and PA2 are outputs */
	DDRB = 0b01000010;       /* PB1 and PB6 are outputs */

	/* configure the USI */
	//USICR |= 0b01011000;
	/*  USISIE (Start Condition Interrupt Enable): 0
		USIOIE (Counter Overflow): 1
		USIWM (Wire Mode): 01 three-wire mode (SPI compliant)
		USICS (Closk Source Dectect): 10 (SPI data mode=0)
		USICLK (Clock Strobe): 0
		USITC (Toggle Clock Port Pin): 0 */

	/* turn off the leds */
	ws2812_setleds(leds, NB_LEDS);

	/* blink LED B6 to tell we are alive */
/*	PORTB |= (1<<6);
	_delay_ms(500);
	PORTB &= ~(1<<6);
*/

	/* configure timer0, 16bits mode, Prescaler=1/64
	interrupt when match with OCR0A and OCR0B */
	TCCR0A = 0b10000000;
	TCCR0B = 0b00000011;
	TIMSK = 0b00010001;

	OCR0B = 42; //so match after 12500 ticks @8MHz, 1/64 as prescaler => interrupt every 100ms
	OCR0A = 212;    /* do not exchange these two lines (special 16bit register access) */

	sei();  /* enable interrupts */
	while(1);

//	while(1)
//	{
//
//		for(i=0; i<20; i++)
//		{
//			/*leds[i].r = 0;
//			leds[i].g = 0;
//			leds[i].b = 255;*/
//			leds[i] = colors[(i+delta)&7];
//		}
//		delta++;
//
//		ws2812_setleds(leds,20);
//		_delay_ms(500);                         // wait for 500ms.
//	}


}
