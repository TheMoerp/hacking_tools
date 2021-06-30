import argparse
import textwrap
import pyperclip

parser = argparse.ArgumentParser(description='Little tool to help building exploits')
parser.add_argument('bytestream', help='bytestream you want to adapt. acceptable formats: 0xnn...nn, nn..nn, \\xnn...\\xnn')
parser.add_argument('-s', '--swap', action="store_true", help='swap endianness')
parser.add_argument('-d', '--delimiter', action="store_true", help='add \\x delimiter')
parser.add_argument('-r', '--remove', action="store_true", help='remove \\x delimiter')
parser.add_argument('-c', '--copy', action="store_true", help='copy the adapted bytestream to the clipboard')
args = parser.parse_args()

byte_stream = args.bytestream

if args.delimiter and args.remove:
    print("\nYou cannot add and remove the delimiter at the same time\n")
    exit()


del_check = False
if "\\x" in byte_stream:
    del_check = True

if byte_stream[0:2] == "0x":
    byte_stream = byte_stream[2:]

byte_list = []
if not del_check:
    if (len(byte_stream) % 2) == 1:
        byte_stream = f"0{byte_stream}"
    byte_list = textwrap.wrap(byte_stream, 2)
else:
    byte_list = byte_list = byte_stream[2:].split('\\x')

if args.swap:
    byte_list.reverse()

if args.delimiter or (del_check and not args.remove):
    byte_stream = '\\x' + '\\x'.join(byte_list)
else:
    byte_stream = ''.join(byte_list)


print(f"\nAdapted bytestream: {byte_stream}\n")

if args.copy:
    pyperclip.copy(byte_stream)
    print("The adapted bytestream has been copied to the clipboard\n")