## install Python 3.5

See [this post on StackOverflow](https://raspberrypi.stackexchange.com/questions/54365/how-to-download-and-install-python-3-5-in-raspbian):
```
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tar.xz
tar -xvf Python-3.5.2.tar.xz
cd Python-3.5.2
./configure
make -j4
make altinstall
``` 

This version of Python is required, because my program relies on the `asyncio` library.

