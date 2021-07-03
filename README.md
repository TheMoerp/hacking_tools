# exploit tools
To install the needed python modules enter:

    pip install -r requirements.txt

## adapt_bytestream
#### Features:

 - swap endianness of a bytestream
 - add the delimiter \x to a bytestream
 - remove the delimiter \x from a bytestream
 - copy the adapted bytestream to the clipboard
 - save several bytestreams with name into a file

#### Usage

    python3 adapt_bytestream.py [-h] [-q] [-s] [-d] [-r] [-c] [-f FILE] [-n NAME] bytestream
Run it with the `-h` or `--help` flag to get a more detailed description of each option.