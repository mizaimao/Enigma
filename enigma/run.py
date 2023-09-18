from pathlib import Path

from enigma.components.machine import Enigma


if __name__ == "__main__":
    input_message: str = "CHICKENMIZAIMAO"
    config_path: Path = None
    table_path: Path = None
    date: int = 1

    enigma_machine = Enigma(
        config_path=config_path, table_path=table_path, date=date, print_cfg=True
    )
    encoded_message: str = enigma_machine.input(input_message)
    enigma_machine = Enigma(
        config_path=config_path,
        table_path=table_path,
        date=date,
    )
    decoded_message: str = enigma_machine.input(encoded_message)

    print("INPUT -> ENCODED -> DECODED:")
    print(f"{input_message} -> {encoded_message} -> {decoded_message}")
