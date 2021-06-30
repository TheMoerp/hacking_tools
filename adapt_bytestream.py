import argparse
import textwrap
import pyperclip

# Argument parser
parser = argparse.ArgumentParser(description='Little tool to help building exploits')
parser.add_argument('bytestream', help='bytestream you want to adapt. acceptable formats: 0xnn...nn, nn..nn, \\xnn...\\xnn')
parser.add_argument('-s', '--swap', action="store_true", help='swap endianness')
parser.add_argument('-d', '--delimiter', action="store_true", help='add \\x delimiter')
parser.add_argument('-r', '--remove', action="store_true", help='remove \\x delimiter')
parser.add_argument('-c', '--copy', action="store_true", help='copy the adapted bytestream to the clipboard')
args = parser.parse_args()

byte_stream = args.bytestream

# Checks if -d and -r is set
if args.delimiter and args.remove:
    print("\nYou cannot add and remove the delimiter at the same time\n")
    exit()

# Checks if the entered byte_stream is delimitered
del_check = False
if "\\x" in byte_stream:
    del_check = True

# Removes the 0x prefix if existing
if byte_stream[0:2] == "0x":
    byte_stream = byte_stream[2:]

# bytestream as list
byte_list = []

# Splits bytestream into a list
if not del_check:
    # Inserts "0" at the front if the number of chars is odd
    if (len(byte_stream) % 2) == 1:
        byte_stream = f"0{byte_stream}"

    byte_list = textwrap.wrap(byte_stream, 2)
else:
    byte_list= byte_stream[2:].split('\\x')

# Reverses the bytelist to swap endianness
if args.swap:
    byte_list.reverse()

# bytelist to bytestring
if args.delimiter or (del_check and not args.remove):
    byte_stream = '\\x' + '\\x'.join(byte_list)
else:
    byte_stream = ''.join(byte_list)


# Prints adapted bytestream
print(f"\nAdapted bytestream: {byte_stream}\n")

# Copys adapted bytestream to the clipboard
if args.copy:
    pyperclip.copy(byte_stream)
    print("The adapted bytestream has been copied to the clipboard\n")