import argparse
import textwrap

parser = argparse.ArgumentParser(description='Little tool to help building exploits')
parser.add_argument('bytestream', help='Bytestream you want to adapt')
parser.add_argument('-s', '--swap', action="store_true", help='swap endianness')
parser.add_argument('-d', '--delimiter', action="store_true", help='add \\x delimiter')
parser.add_argument('-r', '--remove_delimiter', action="store_true", help='remove \\x delimiter')
args = parser.parse_args()

byte_stream = args.bytestream

if args.delimiter and args.remove_delimiter:
    print("\nYou cannot add and remove the delimiter at the same time\n")
    exit()


del_check = False
if "\\x" in byte_stream:
    del_check = True


byte_list = []
if not del_check:
    if (len(byte_stream) % 2) == 1:
        byte_stream.insert(0, '0')
    byte_list = textwrap.wrap(byte_stream, 2)
else:
    byte_list = byte_list = byte_stream[2:].split('\\x')

if args.swap:
    byte_list.reverse()

if args.delimiter or (del_check and not args.remove_delimiter):
    byte_stream = '\\x' + '\\x'.join(byte_list)
else:
    byte_stream = ''.join(byte_list)


print(f"\nAdapted bytestream: {byte_stream}\n")