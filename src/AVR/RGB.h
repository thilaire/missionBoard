/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: RGB.h
       utilities function for the RGB leds
       - use the light_ws2812 library
       - manage the blink of the LED (according to a 16-bit pattern)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/



#ifndef _RGB_H_
#define _RGB_H_


void setRGBLed(uint8_t nLed, uint8_t* buffer);
void fillRGBBuffer( uint8_t bcycle);
void updateRGB();
uint8_t RGBshouldBeUpdated( uint8_t blinkCycle);
void turnOffRGB();

#endif