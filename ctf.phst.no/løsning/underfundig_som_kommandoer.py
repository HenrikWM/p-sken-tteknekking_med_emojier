import sys

operands = {"🐰", "🐥", "🌱", "🌻", "🐇", "🥚", "🐤", "🐣", "🌞"}

digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)


def parse_num(code):
    num = 0
    for i, c in enumerate(code):
        num += digits[c] * base**i
    return num


def write_decoded_commands(characters):
    with open("ctf.phst.no\\løsning\\underfundig_som_kommandoer_output", "w", encoding="utf-8") as output_file:

        group = []
        pc = 0
        for character in characters:
            if character in operands:
                description = ""
                if (character == "🐇"):
                    description = "jmp"
                elif (character == "🐣"):
                    description = "readline"
                elif (character == "🐤"):
                    description = "print"
                elif (character == "🐰"):
                    description = "get_next_num"
                elif (character == "🥚"):
                    description = "xor"
                elif (character == "🌞"):
                    description = "quit"
                elif (character == "🐥"):
                    description = "push"
                elif (character == "🌻"):
                    description = "pop_sub"
                elif (character == "🌱"):
                    description = "pop_add"
                output_file.writelines(
                    str(pc) + ": " + character + "(" + description + ")\n")
                pc += 1
                continue

            group.append(character)

            if (len(group) == 4):
                val = parse_num(group)
                output_file.writelines(''.join(str(x)
                                               for x in group) + ": " + str(val) + " (" + chr(val) + ")\n")
                group = []

            pc += 1
    output_file.close()


code = open(sys.argv[1], "rt", encoding="utf-8").read()

write_decoded_commands(code)
