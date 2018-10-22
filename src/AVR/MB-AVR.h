/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: MB-AVR.h
       Main header of the AVR code
       - definition of a SPI message

Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/


#ifndef __MB_AVR_H__
#define __MB_AVR_H__

#include <stdint.h>

/* message type
this is not memory efficient (we keep 8 bytes per message!)
but it simplifies a lot the code (we have to choose, we can't do both...)*/
typedef struct {
	uint8_t command;
	uint8_t data[8];        /* the elements must stay in that order ! */
} SPImessage;

#endif
