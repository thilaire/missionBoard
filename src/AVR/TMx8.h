/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: TMx8.c
       high-level driver for the TM1638 boards
       - manage messages from the SPI
       - get data from the TMx8 and put it in the right order
       - based on the low-level driver (see TM1638.c)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/


#ifndef _TMx8_H_
#define _TMx8_H_


#define NB_TMx8 3
#define NB_TMx7 3


uint8_t getDataTMx8(uint8_t nTM, uint8_t* data);
void setDisplayTMx(uint8_t SPIcommand, uint8_t* SPIbuffer);
void setLedTMx8(uint8_t SPIcommand);
void setBrightnessTMx(uint8_t SPIcommand);
void turnOffTMx(uint8_t SPIcommand);
void clearTMx(uint8_t SPIcommand);
void setupTMx(uint8_t brightness);
void switchDataTMx();

#endif