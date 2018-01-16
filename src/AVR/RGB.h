/*
* Author: T. HILAIRE
*
* driver for the RGB leds and the SPI protocol used
*
* Licence: GPL v3
*/


#ifndef _RGB_H_
#define _RGB_H_


void setRGBLed(uint8_t nLed, uint8_t* buffer);
void fillRGBBuffer( uint8_t bcycle);
void updateRGB();
uint8_t RGBshouldBeUpdated( uint8_t blinkCycle);

#endif