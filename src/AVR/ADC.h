/*
* Author: T. HILAIRE
*
* driver for TM1638 board and the SPI protocol used
*
* Licence: GPL v3
*/


#ifndef _ADC_H_
#define _ADC_H_


void initADC();
uint8_t getADC(uint8_t cycle, uint8_t* data);
void runADC(uint8_t cycle);
void switchDataADC();

#endif