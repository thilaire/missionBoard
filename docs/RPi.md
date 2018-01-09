## install Raspbian

## change login/password

## enable SPI

## install a Python 3.x version (with x>=5)

See [this](https://raspberrypi.stackexchange.com/questions/54365/how-to-download-and-install-python-3-5-in-raspbian) or [this](https://stackoverflow.com/questions/41489439/pip3-installs-inside-virtual-environment-with-python3-6-failing-due-to-ssl-modul) posts:
```
sudo apt-get install python3-dev libffi-dev libssl-dev
wget https://www.python.org/ftp/python/3.6.4/Python-3.6.4.tgz  
tar xvf Python-3.6.4.tgz
cd Python-3.6.4
./configure --enable-optimizations
make -j4
sudo make altinstall
``` 

This version of Python is required, because my program relies on the `asyncio` library.

## Python Libraries

You will need the following libraries:
- spidev (for the SPI communication with the AVR micro-controller)
- RPi.GPIO

