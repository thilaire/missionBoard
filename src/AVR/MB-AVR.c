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

#define NB_LEDS 20

struct cRGB leds[NB_LEDS] = {0};

void init_spi(void)
{
	/* configure the USI */
	USICR |= 0b10011000;
	/*  USISIF (Start Condition Interrupt Enable): 1
		USIOIE (Counter Overflow): 0
		USIWM (Wire Mode): 01 three-wire mode (SPI compliant)
		USICS (Closk Source Dectect): 10 (SPI data mode=0)
		USICLK (Clock Strobe): 0
		USITC (Toggle Clock Port Pin): 0 */

	/* enable SPI interrupt */
	/* clear SPI interrupt Flag by reading SPSR and SPDR */
	/* enable global interrupts */
}


ISR (USI_START_vect )                  // SPI interrupts
{
	leds[USIDR].g = 255;
	leds[0].g ^= 255;
	ws2812_setleds(leds,20);
	PORTB |= (1<<6);
	_delay_ms(500);
	PORTB &= 255-(1<<6);
}

int main(void)
{

	#ifdef DEBUG
	leds[12].g = 255;
	#endif

	/* configure inputs/outputs */
	DDRA = 0b00000110;       /* PA1 and PA2 are outputs */
	DDRB = 0b01000010;       /* PB1 and PB6 are outputs */

	init_spi();

	/* turn off the led */
	ws2812_setleds(leds, NB_LEDS);

	/* enable interrupt */
	sei();
	USIBR = 42;
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
