import sys
import os

digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)

# HWM START: Create DEBUG-file
output_file = open(
    "underfundig_debug", "w", encoding="utf-8")


def print_debug(op, sp, stack):
    """ Prints debug-output with operand, stack-pointer and the stack

    op: the program's current 'operand'\n
    sp: the program's current 'stack-pointer'\n
    stack: the virtual program's 'stack'
    """
    output_string = op + ":\t"
    sp_value = "*"
    for i in range(len(stack)):
        if i == sp:
            output_string += "(" + str(stack[i]) + "),"
        else:
            output_string += str(stack[i]) + ","

    output_file.write(output_string + "\n")
    output_file.flush()

# HWM END: Create DEBUG-file


def parse_num(code):
    num = 0
    for i, c in enumerate(code):
        num += digits[c] * base**i
    return num


if len(sys.argv) < 2:
    print("Mangler programfil!")
    exit(1)

code = open(sys.argv[1], "rt", encoding="utf8").read()
pc = 0

stack = [0] * 256
sp = 0

# HWM DEBUG - output debug info
print_debug('*', sp, stack)

while pc < len(code):
    op = code[pc]
    pc += 1

    if op == "🐰":
        stack[sp] = parse_num(code[pc:pc+4])

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        sp += 1
        pc += 4

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)
    elif op == "🐥":
        stack[sp] = stack[sp-1]

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        sp += 1

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)
    elif op == "🌱":
        sp -= 1

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        stack[sp-1] += stack[sp]

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        stack[sp-1] %= base**4

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)
    elif op == "🌻":
        sp -= 1

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        stack[sp-1] -= stack[sp]

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        stack[sp-1] %= base**4

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)
    elif op == "🐇":
        sp -= 1

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        if stack[sp] != 0:
            pc += parse_num(code[pc:pc+4])
        else:
            pc += 4
    elif op == "🥚":
        sp -= 1

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        stack[sp-1] ^= stack[sp]

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)
    elif op == "🐤":
        sp -= 1
        os.write(1, bytes([stack[sp]]))
    elif op == "🐣":
        line = sys.stdin.buffer.readline().strip()
        for c in line:
            stack[sp] = c

            # HWM DEBUG - output debug info
            print_debug(op, sp, stack)

            sp += 1

            # HWM DEBUG - output debug info
            print_debug(op, sp, stack)

        stack[sp] = len(line)

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)

        sp += 1

        # HWM DEBUG - output debug info
        print_debug(op, sp, stack)
    elif op == "🌞":
        exit(0)

        # HWM DEBUG - close debug file
        output_file.close()
