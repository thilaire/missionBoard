/*
* Author: T. HILAIRE
*
* driver for the RGB leds and the SPI protocol used
*
* Licence: GPL v3
*/


#include "light_ws2812.h"
#include "RGB.h"


/* data for RGB LEDS */
 #define NB_LEDS 21
struct sRGB_LED{
	uint16_t blinkPattern;  /* pattern: x-th bits indicates if the led is on at cycle x; 0xffff for always on, 0b0101010101010101 for fast blinking */
	struct cRGB color;
};
const struct cRGB LedOff = {0};         /* led off */
struct sRGB_LED RGBleds[NB_LEDS] = {0};        /* array of leds */
 struct cRGB bufferLeds[NB_LEDS] = {0};  /* buffer of data to send (dedicated to light_ws2812 libray) */

 uint8_t RGBledsHasChanged = 0; /* bool that indicates if the leds has changed during last cycle */
 uint16_t blinkEvent = 0;  /* the x-th bit of blinkEvent indicates if a Led need to change its color (blink) at cycle #x WRT to the previous cycle */
uint16_t blinkEventTable[NB_LEDS] = {0};    /* intermediate table: the same as blinkEvent, but for each led. Use only to do not have to recompute it every time (we have here enough bytes in RAM for this) */

/*TODO: put it in a fancy struct ?*/





/* add a new command for a led
nLed: number of the led
buffer: the 5 bytes for the SPI buffer */
void setRGBLed(uint8_t nLed, uint8_t* buffer)
{
	RGBledsHasChanged = 1;

	/* copy the five bytes */
	RGBleds[ nLed ] = *(struct sRGB_LED*) buffer;

	/* update the blink Event Table for the concerned led */
	uint16_t blinkPatternOfThisLed = RGBleds[ nLed].blinkPattern;
	blinkEventTable[ nLed ] = blinkPatternOfThisLed ^ ( (blinkPatternOfThisLed>>15) | (blinkPatternOfThisLed<<1) ); /* (a>>15) | (a<<1) corresponds to a 1-bit left bitwise rotation; a XOR with itself gives the place where the bit changes from it predecessor */

	/* then re-compute blinkEvent, as the OR-sum of each blinkEventTable element */
	blinkEvent = 0;
	uint16_t* pbE = blinkEventTable;
	for(uint8_t i=0; i<NB_LEDS; i++)
	{
		blinkEvent |= *pbE++;
	}
}


/* fill the Led Buffer with the led colors
  (manage the blinking according to the cycle) */
void fillRGBBuffer( uint8_t bcycle)
{
	struct cRGB *pBuffer = bufferLeds;
	struct sRGB_LED *pLeds = RGBleds;
	uint16_t pattern = (1U<<bcycle);

	/* copy the leds to the buffer */
	/* and switch off the leds that blink (off) in that cycle */
	for( uint8_t i=0; i<NB_LEDS; i++)
	{
		if (pLeds->blinkPattern & pattern)
		{
			*pBuffer = pLeds->color;
		}
		else
		{
			/* this led is off */
			*pBuffer = LedOff;
		}
		pBuffer++;
		pLeds++;
	}
}

void updateRGB()
{
	ws2812_setleds(bufferLeds, NB_LEDS);
	RGBledsHasChanged = 0;
}


uint8_t RGBshouldBeUpdated(uint8_t blinkCycle)
{
	return (RGBledsHasChanged || ((blinkEvent >> blinkCycle)&1) );      /* blinkCycle -th bit of blinkEvent */
}