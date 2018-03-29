# how to put several digital input on a single analog input

Some doc to express how multiple switches are connected to a single analog input

(to be continued with scheme, some math, some experiment with Python Code, and the C code)



```C
uint8_t getADCSwitches(uint8_t* data)
{
	/* get the ADC value in ADCH */
	uint8_t adc = ADCH;
	/* convert it in 4-bit for the switches */
	if (adc<122)
		*data = (adc+5)>>4;
	else
	{
		uint8_t sh = adc-36;   /* shift*/
		uint8_t sh22 = sh + (sh>>2) + (sh>>3);  /* shift*22*/
		*data = sh22>>4;     /* shift*22/256 */
	}
	/* we want these 4 bits on the MSB */
	*data <<= 4;
	/* check if something has changed */
	if (ADCswitches != *data)
	{
		ADCswitches = *data;
		return 1;
	}
	else
		return 0;
}

```