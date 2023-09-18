from pathlib import Path

from enigma.components.machine import Enigma


if __name__ == "__main__":

    input_message: str = "CHICKENMIZAIMAO"
    e = Enigma(print_cfg=True)
    encoded_message: str = e.input(input_message)
    e = Enigma()
    decoded_message: str = e.input(encoded_message)

    print(f"{input_message} -> {encoded_message} -> {decoded_message}")