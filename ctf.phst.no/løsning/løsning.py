import sys

operands = {"🐰", "🐥", "🌱", "🌻", "🐇", "🥚", "🐤", "🐣", "🌞"}

digits = {"🎲": 0, "🍫": 1,  "🎮": 2, "🎧": 3, "🎨": 4, "🍬": 5}
base = len(digits)

if len(sys.argv) < 2:
    print("Mangler programfil!")
    exit(1)


def parse_num(code):
    """ Copy of method defined in 'merkelig.py'

    Reads group of 4 emoji-characters and returns a numeric value

    Example:

    🎮🍫🎮🎲 = 80
    """
    num = 0
    for i, c in enumerate(code):
        num += digits[c] * base**i
    return num


def group(characters, size):
    """ Groups the characters into groups in specified size.
    """
    for i in range(0, len(characters), size):
        val = characters[i:i+size]
        if len(val) == size:
            yield tuple(val)


def removeOperands(characters):
    characters_without_operands = ""
    for character in characters:
        if character not in operands:
            characters_without_operands += character
    return characters_without_operands


def extract_text(characters):
    underfundig_characters_groups = list(group(removeOperands(characters), 4))
    underfundig_characters_decoded = ""
    for underfundig_character_group in underfundig_characters_groups:
        number_value = parse_num(underfundig_character_group)
        if (number_value < 700):  # only interested in numeric values within (extended) ASCII-table
            underfundig_characters_decoded += chr(number_value)

    cipher_text = ""
    i = 0
    for _ in underfundig_characters_decoded:
        if (i + 1 > len(underfundig_characters_decoded)):
            break

        cipher_text += underfundig_characters_decoded[i]

        # Pattern of the cipher to decode is: '<char>*<char>*<char>[...]', e.g. 'w*4*D*T*W'
        # If we see the current character group's character is not in this format, skip to the next character group's character
        if (underfundig_characters_decoded[i] == "*") and (underfundig_characters_decoded[i+2] != "*"):
            cipher_text += underfundig_characters_decoded[i+1]
            i += 3
            continue

        i += 1
    return cipher_text


def decipher(characters):
    characters = characters.replace('**', '*')  # Nice trap! ;)

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


underfundig_content = open(sys.argv[1], "rt", encoding="utf-8").read()

# Decode all characters in "underfundig"-file.
# Gets only data which is ASCII/Binary and skips any operands
# Output = 'Passord: "w*4*D*T*W*J*7*A*Y*f*`*j*n***}*4*\x9d*ç*¿*Ą*Ŏ*Ŋ*Ŧ*ı*Ɖ*Ǔ*Ǒ*Ǐ*ǐ*Ǉ*Ǧ*ǜ*ƹ*ț*ɵGratulerer! Flagget vet du allerede :)\nIkke riktig :(\n'
text = extract_text(underfundig_content)

print(text)

# Get deciphered text
# w XOR (4-*) = '}'
# 4 XOR (D-*) = '.'
# etc.
# Output = '}.nywG neP .nywG re nvan ttiM{TSHP'
deciphered_cipher_raw = decipher(text)

print(deciphered_cipher_raw)

# Reverse the deciphered text
# Output = 'PHST{Mitt navn er Gwyn. Pen Gwyn.}'
deciphered_cipher = deciphered_cipher_raw[::-1]

print(deciphered_cipher)
