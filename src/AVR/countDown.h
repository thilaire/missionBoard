/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: countDown.h
       utilities function for the countDown
       count down from 10 to 0
       (every 1/16 of second, the timer uses those functions)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/

#ifndef __COUNTDOWN_H__
#define __COUNTDOWN_H__

/* initialize the count down (to 10s) */
void initCountDown();

/* run the count down */
void runCountDown();

/* stop the count down */
void stopCountDown();

/* update the count down */
void updateCountDown();


#endif