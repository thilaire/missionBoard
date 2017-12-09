

#include <util/delay.h>
#include <avr/io.h>


int main(void)
{

	/* configure inputs/outputs */
	DDRC = 0b10000000;       /* PC7 is output */


	/* blink LED B6 to tell we are alive */
	while(1)
	{
		PORTC |= (1<<7);
		_delay_ms(500);
		PORTC &= ~(1<<7);
		_delay_ms(500);
	}



}
