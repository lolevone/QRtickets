def encrypt_text(text: str, gamma: list) -> str:
    """Returns text encrypted using gamma encryption."""
    new_text = ""
    for symbol in text:
        key = format(gamma[0], 'b')
        if len(key) % 2 == 1:
            key = '0' + key
        symbol = format(ord(symbol), 'b')
        while len(symbol) < 15:
            symbol = '0' + symbol
        new_symbol = ""
        k = 0
        for bit in symbol:
            if bit != key[k]:
                new_symbol += '1'
            else:
                new_symbol += '0'
            k += 1
            if k == len(key):
                k = 0
        new_symbol = chr(int(new_symbol, 2))
        new_text += new_symbol
        gamma[0] = ((gamma[0] * gamma[1]) % gamma[2])
    return new_text  # .encode('utf-16', 'replace').decode('utf-16', 'replace')


def encrypt_number(number: str, gamma: list) -> str:
    """Returns a number encrypted using gamma encryption."""
    new_number = ""
    alphabet = "ABCDEF"
    for symbol in number:
        if symbol in alphabet:
            for i in range(10, 16):
                if symbol == alphabet[i - 10]:
                    symbol = i
                    break
        else:
            symbol = int(symbol)
        key = format(gamma[0], 'b')
        if len(key) % 2 == 1:
            key = '0' + key
        symbol = bin(symbol)[2:]
        while len(symbol) < 4:
            symbol = '0' + symbol
        new_symbol = ""
        k = 0
        for bit in symbol:
            if bit != key[k]:
                new_symbol += "1"
            else:
                new_symbol += '0'
            k += 1
            if k == len(key):
                k = 0
        new_symbol = int(new_symbol, 2)
        if new_symbol > 9:
            new_symbol = alphabet[new_symbol - 10]
        else:
            new_symbol = str(new_symbol)
        new_number += new_symbol
        gamma[0] = ((gamma[0] * gamma[1]) % gamma[2])
    return new_number


def get_gamma_filename(name: str) -> list:
    """Returns a list of values for gamma encryption calculated using the filename."""
    initial_key = 0
    factor = 1
    for symbol in name:
        initial_key += ord(symbol)
        factor *= ord(symbol)
    module = factor + initial_key
    return [initial_key, factor, module]
