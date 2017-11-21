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

struct cRGB leds[12];
struct cRGB colors[8];
int main(void)
{
    char i, delta=0;
  //Rainbowcolors
    colors[0].r=150; colors[0].g=150; colors[0].b=150;
    colors[1].r=255; colors[1].g=000; colors[1].b=000;//red
    colors[2].r=255; colors[2].g=100; colors[2].b=000;//orange
    colors[3].r=100; colors[3].g=255; colors[3].b=000;//yellow
    colors[4].r=000; colors[4].g=255; colors[4].b=000;//green
    colors[5].r=000; colors[5].g=100; colors[5].b=255;//light blue (türkis)
    colors[6].r=000; colors[6].g=000; colors[6].b=255;//blue
    colors[7].r=100; colors[7].g=000; colors[7].b=255;//violet


  while(1)
  {

    for(i=0; i<12; i++)
    {
        /*leds[i].r = 0;
        leds[i].g = 0;
        leds[i].b = 255;*/
        leds[i] = colors[(i+delta)&7];
    }
    delta++;

    ws2812_setleds(leds,12);
    _delay_ms(500);                         // wait for 500ms.

  }
}
