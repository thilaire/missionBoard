/*
* Author: T. HILAIRE
*
* driver for TM1638 board and the SPI protocol used
*
* Licence: GPL v3
*/


#ifndef _TMx8_H_
#define _TMx8_H_


#define NB_TMx8 3
#define NB_TMx7 3


void getDataTMx8(uint8_t nTM);
void setDisplayTMx(uint8_t SPIcommand, uint8_t* SPIbuffer);
void setLedTMx8(uint8_t SPIcommand);
void setBrightnessTMx(uint8_t SPIcommand);
void turnOffTMx(uint8_t SPIcommand);
void clearTMx(uint8_t SPIcommand);
void setupTMx(uint8_t brightness);

#endif