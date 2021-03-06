import argparse
import textwrap
import pyperclip


# Argument parser
parser = argparse.ArgumentParser(description='Little tool to help building exploits')
parser.add_argument('string', help='bytestream you want to adapt. acceptable formats: 0xnn...nn, nn..nn, \\xnn...\\xnn')
parser.add_argument('-q', '--quiet', action="store_true", help='do not print the adapted bytestream to stdout')
parser.add_argument('-s', '--swap', action="store_true", help='swap endianness')
parser.add_argument('-d', '--delimiter', action="store_true", help='add the \\x delimiter')
parser.add_argument('-r', '--remove', action="store_true", help='remove the \\x delimiter')
parser.add_argument('-a', '--ascii', action="store_true", help='set this flag if you want to convert an ascii string to a bytestream')
parser.add_argument('-c', '--copy', action="store_true", help='copy the adapted bytestream to the clipboard (only for Windows)')
parser.add_argument('-f', '--file', help='write output into a file defaultname: bytestream_save.txt', default='bytestream_save.txt')
parser.add_argument('-n', '--name', help='name of the stream for saving into a file')
args = parser.parse_args()

input_string = args.string
file = args.file
stream_name = args.name


def wrong_args_check():
    # Checks if -q is set and not -f
    if not file and args.quiet:
        print("\nYou will not get any output if you set the quiet flag and not the file flag\n")
        exit()

    # Checks if -d and -r is set
    if args.delimiter and args.remove:
        print("\nYou cannot add and remove the delimiter at the same time\n")
        exit()


def convert(input_string):
    return "".join(hex(ord(c))[2:] for c in input_string)



def stream2list(byte_stream):
    del_check = False
    # Checks if the entered byte_stream is delimitered
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

    return byte_list, del_check



def bytelist2bytestream(byte_list, del_check):
    # bytelist to bytestring
    if args.delimiter or (del_check and not args.remove):
        byte_stream = '\\x' + '\\x'.join(byte_list)
    else:
        byte_stream = ''.join(byte_list)

    return byte_stream

def output(byte_stream, stream_name):
    # Prints adapted bytestream
    if stream_name:
        if not args.quiet:
            print(f"\n{stream_name}: {byte_stream}\n")
        if file:
            f = open(file, 'a')
            f.write(f"{stream_name}: {byte_stream}\n")
            f.close()
    else:
        if not args.quiet:
            print(f"\nAdapted string: {byte_stream}\n")
        if file:
            f = open(file, 'a')
            f.write(f"Adapted string: {byte_stream}\n")
            f.close()

    # Copys adapted bytestream to the clipboard (only works on Windows)
    if args.copy:
        pyperclip.copy(byte_stream)
        print("The adapted bytestream has been copied to the clipboard\n")


def main():
    wrong_args_check()
    byte_stream = input_string

    if args.ascii:
        byte_stream = convert(input_string)

    byte_list, del_check = stream2list(byte_stream)

    # Reverses the bytelist to swap endianness
    if args.swap:
        byte_list.reverse()
    
    byte_stream = bytelist2bytestream(byte_list, del_check)

    output(byte_stream, stream_name)


if __name__ == "__main__":
    main()