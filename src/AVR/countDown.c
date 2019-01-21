/*----------------------------------------------------------------------------

                          *========================*
                          |                        |
                          | Project MissionBoard   |
                          |                        |
                          *========================*


 Authors: T. HILAIRE
 Licence: GPL v3

 File: countDown.c
       utilities function for the countDown
       count down from 10 to 0
       (every 1/16 of second, the timer uses those functions)


Copyright 2017-2018 T. Hilaire

----------------------------------------------------------------------------*/

/* arrays to display the digits to the 7-segment display */
const uint8_t digit[10] = {191,134,219,207,230,237,253,167,255,239};
const uint8_t array10[16] = {63,63,6,6,91,79,79,102,109,109,125,125,39,127,127,111};
const uint8_t array100[8] = {63,125,91,127,109,6,39,79};


/* value of the count down (in fixed-point, scale=1/16s) */
uint8_t countdown = 160;
uint8_t isRunning = 0;

/* initialize the count down (to 10s) */
void initCountDown() {
	uint8_t disp[8] = {0,0,6,191,63,63,63,63};
	countdown = 160;    /* 10 seconds */
	isRunning = 0;
	/* display "  10.0000" */
	setDisplayTMx(0b11010100,val);

}

/* run the count down */
void runCountDown() {
	if (countdown!=0)
		isRunning = 1;
}

/* stop the count down */
void stopCountDown() {
	isRunning = 0;
}

/* update the count down
WARNING: the array TMxDisplay (from TMx.c) is not modified by this function */
void updateCountDown() {
	if (isRunning) {
		/* display the count down */
		if (countdown&15) {
			/* only need to display right part of the display */
			TM1638_sendData(8, array10[countdown&15], TM1638_STB_PINMASK[0]); /* 1/10 of seconds */
            TM1638_sendData(10, array100[countdown&7], TM1638_STB_PINMASK[0]); /* 1/100 of seconds */
            TM1638_sendData(12, array100[countdown&3], TM1638_STB_PINMASK[0]); /* fake 1/1000 of seconds */
            TM1638_sendData(14, array100[(countdown<<1)&3], TM1638_STB_PINMASK[0]);/* fake 1/10000 of seconds */
		}
		else {
			/* display the 8 char "   x.0000" where x is the number of seconds */
			TM1638_sendData(6, giti[countdown>>4], TM1638_STB_PINMASK[0]); /* seconds */
			TM1638_sendData(8, 63, TM1638_STB_PINMASK[0]);  /* display `0` */
			TM1638_sendData(10, 63, TM1638_STB_PINMASK[0]);
			TM1638_sendData(12, 63, TM1638_STB_PINMASK[0]);
			TM1638_sendData(14, 63, TM1638_STB_PINMASK[0]);
		}
		/* decrease it */
		countDown--;
		if (countDown==0)
			isRunning = 0;
	}
}
