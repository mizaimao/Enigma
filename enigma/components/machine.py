"""Machine main emulation module."""

from typing import Any, Dict, List, Tuple
from pathlib import Path

import pandas as pd
import numpy as np

from enigma.components.rotors import Rotor, Reflector


class Enigma:
    """Enigma M3 emulator."""

    def __init__(
        self, config_path: Path = None, table_path: Path = None, date: int = 1
    ):
        """
        Load configuration file and table.
        NOTE: argument date is 1-based.
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.joinpath(
                "configs", "default.csv"
            )
        if table_path is None:
            table_path = Path(__file__).parent.parent.joinpath("tables", "default.csv")

        self.rotors: List[Rotor]  # Rotors in use.
        self.all_rotors: List[Rotor]
        self.reflector: Reflector
        self.all_rotors, self.reflector = self.load_config(config_path)
        self.table: Dict[str, Any] = self.load_table(table_path, date)

        # Apply table settings to machine. Reduces number of rotors.
        self.adjust_machine()

    def adjust_machine(self):
        """Adjust machine according to the table entry."""
        # Add appropriate rotors.
        self.rotors = []
        for rotor_index in self.table["rotors"]:
            self.rotors.append(self.all_rotors[rotor_index])
        # Rotate rotors to requested positions.
        for rotor, position in zip(self.rotors, self.table["rings"]):
            rotor.tune(position - 65)
        # Add plugs.

    def load_config(self, config_path: Path) -> Tuple[List[Rotor], Reflector]:
        config_path = Path(config_path)
        assert config_path.is_file(), f"Config at {config_path} not found."
        config_df: pd.DataFrame = pd.read_csv(config_path)

        rotors: List[Rotor] = []
        reflector: Reflector = None

        for row_i in range(config_df.shape[0]):
            component: Dict[str, Any] = config_df.iloc[row_i]
            if component["type"] == "rotor":
                rotor: Rotor = Rotor(component["wiring"])
                rotors.append(rotor)
            elif component["type"] == "reflector":
                assert (
                    reflector is None
                ), "There should only be one reflector in config table."
                reflector: Reflector = Reflector(component["wiring"])
            else:
                raise ValueError(
                    f"Unrecognized component type in config: {component['type']}."
                )

        return rotors, reflector

    def load_table(self, table_path: Path, date: int) -> Dict[str, Any]:
        table_path = Path(table_path)
        assert table_path.is_file(), f"Table at {table_path} not found."
        table: Dict[str, Any] = {}

        table_df: pd.DataFrame = pd.read_csv(table_path)
        date = table_df.shape[0] - date
        table["rotors"] = eval(table_df.iloc[date]["rotors"])
        table["rings"] = eval(table_df.iloc[date]["rings"])
        table["plugs"] = eval(table_df.iloc[date]["plugs"])
        table["indicators"] = eval(table_df.iloc[date]["indicators"])
        return table

    def rotate_rotors(self):
        carry: int = 1
        for rotor in self.rotors[::-1]:
            if carry:
                carry = rotor.rotate()
            else:
                break

    def input(self, input_str: str) -> str:
        output_str: str = ""
        input_str = input_str.upper()
        assert input_str.isalpha(), f"Only alpha strings accepted. Got {input_str}."
        for input_char in input_str:
            # Rotate rotors for each character.
            self.rotate_rotors()
            # From right to left.
            input_index: int = ord(input_char) - 65
            for rotor in self.rotors[::-1]:
                input_index = rotor.input(input_index, reverse=False)

            # Reflector.
            input_index = self.reflector.input(input_index)

            # From left to right.
            for rotor in self.rotors:
                input_index = rotor.input(input_index, reverse=True)

            # Convert to character.
            output_char = chr(input_index + 65)
            output_str += output_char

        print(output_str)
        return output_str


if __name__ == "__main__":
    e = Enigma()
    e.input("AAAAAAAA")
    e = Enigma()
    e.input("BTBONYQF")
