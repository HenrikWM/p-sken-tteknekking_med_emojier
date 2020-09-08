import sys

operands = {"🐰", "🐥", "🌱", "🌻", "🐇", "🥚", "🐤", "🐣", "🌞"}

digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)


def parse_num(code):
    num = 0
    for i, c in enumerate(code):
        num += digits[c] * base**i
    return num


if len(sys.argv) < 2:
    print("Mangler programfil!")
    exit(1)


def group(lst, n):
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield tuple(val)


def write_decoded_commands(characters):
    with open("underfundig_kommandoer", "w", encoding="utf-8") as output_file:

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


def removeOperands(characters):
    code_without_operands = ""
    for code_character in code:
        if code_character not in operands:
            code_without_operands += code_character
    return code_without_operands


code = open(sys.argv[1], "rt", encoding="utf-8").read()

write_decoded_commands(code)


def decode_underfundig(characters):
    code_characters = list(group(removeOperands(characters), 4))
    code_characters_decoded = ""
    for code_character_group in code_characters:
        val = parse_num(code_character_group)
        if (val < 700):
            code_characters_decoded += chr(val)

    cipher_text = ""
    i = 0
    for _ in code_characters_decoded:
        if (i + 1 > len(code_characters_decoded)):
            break

        cipher_text += code_characters_decoded[i]
        if (code_characters_decoded[i] == "*") and (code_characters_decoded[i+2] != "*"):
            cipher_text += code_characters_decoded[i+1]
            i += 3
            continue

        i += 1
    return cipher_text


def decipher(characters):
    characters = characters.replace('**', '*')

    reading_cipher_characters = True
    deciphered_text = ""

    i = 0

    while reading_cipher_characters:
        if i == len(characters):
            reading_cipher_characters = False
            break

        if i + 1 < len(characters):
            if characters[i+1] != "*":
                i += 1
                continue
            else:
                character_numeric_value = ord(str(characters[i]))

                difference_between_numeric_values = ord(
                    str(characters[i+2])) - ord(str(characters[i+1]))

                xor_result = character_numeric_value ^ difference_between_numeric_values
                if (xor_result > -1):
                    deciphered_text += chr(xor_result)

        i += 1

    return deciphered_text


# Decode all characters in "underfundig"-file
# w XOR (4-*) = '}'
# 4 XOR (D-*) = '.'
# Output = 'Passord: "w*4*D*T*W*J*7*A*Y*f*`*j*n***}*4*\x9d*ç*¿*Ą*Ŏ*Ŋ*Ŧ*ı*Ɖ*Ǔ*Ǒ*Ǐ*ǐ*Ǉ*Ǧ*ǜ*ƹ*ț*ɵGratulerer! Flagget vet du allerede :)\nIkke riktig :(\n'
decoded_characters = decode_underfundig(code)

# Get deciphered text
# Output = '}.nywG neP .nywG re nvan ttiM{TSHP'
deciphered_cipher_raw = decipher(decoded_characters)

# Reverse deciphered text
# Output = 'PHST{Mitt navn er Gwyn. Pen Gwyn.}'
deciphered_cipher = deciphered_cipher_raw[::-1]

print(deciphered_cipher)
