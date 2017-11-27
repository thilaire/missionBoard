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

struct cRGB leds[NB_LEDS] = 0;

int main(void)
{

	#ifdef DEBUG
	leds[12].green = 255;
	#endif

	/* configure inputs/outputs */
	DDRA = 0b00000110       /* PA1 and PA2 are outputs */
	DDRB = 0b01000010       /* PB1 and PB6 are outputs */


	/* turn off the led */
	ws2812_setleds(leds, NB_LEDS);




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
