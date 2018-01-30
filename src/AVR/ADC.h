/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: ADC.h
       utilities function for the ADC
       - run ADC, acquire data and check if it has changed


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/



#ifndef _ADC_H_
#define _ADC_H_


void initADC();
uint8_t getADCtoto(uint8_t cycle, uint8_t* data);
void runADC(uint8_t cycle);
void switchDataADC();

#endif