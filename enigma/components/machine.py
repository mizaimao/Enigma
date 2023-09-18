"""Machine main emulation module."""

from typing import Any, Dict, List, Tuple
from pathlib import Path

import pandas as pd
import numpy as np

from enigma.components.rotors import Rotor, Reflector
from enigma.utils.constants import ROTOR_NAMES


class Enigma:
    """Enigma M3 emulator."""

    def __init__(
        self,
        config_path: Path = None,
        table_path: Path = None,
        date: int = 1,
        print_cfg: bool = False,
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

        self.date: int = date

        self.rotors: List[Rotor]  # Rotors in use.
        self.all_rotors: List[Rotor]
        self.reflector: Reflector
        self.all_rotors, self.reflector = self.load_config(config_path)
        self.table: Dict[str, Any] = self.load_table(table_path)

        # Apply table settings to machine. Reduces number of rotors.
        self.adjust_machine()

        if print_cfg:
            self.print_cfg()

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

    def load_table(self, table_path: Path) -> Dict[str, Any]:
        table_path = Path(table_path)
        assert table_path.is_file(), f"Table at {table_path} not found."
        table: Dict[str, Any] = {}

        table_df: pd.DataFrame = pd.read_csv(table_path)
        date: int = table_df.shape[0] - self.date
        table["rotors"] = eval(table_df.iloc[date]["rotors"])
        table["rings"] = eval(table_df.iloc[date]["rings"])
        table["plugs"] = eval(table_df.iloc[date]["plugs"])
        table["indicators"] = eval(table_df.iloc[date]["indicators"])
        return table
    
    def print_cfg(self):
        """Print configs."""
        print_ext: int = 4  # Extend of config printing table width.

        date_desc: str = "CONFIGURED BY DATE"
        date_msg: str = "{:02d}".format(self.date)

        rotor_desc: str = "ROTORS IN USE"
        rotor_msg: str = " ".join([ROTOR_NAMES[r] for r in self.table["rotors"]])

        align_desc: str = "ROTOR INITIAL POSITIONS"
        align_msg: str = " ".join(
            ["{:02d}".format(r + 1 - 65) for r in self.table["rings"]]
        )

        plug_desc: str = "PLUGS"
        plug_msg: str = " ".join(
            [f"{chr(key1)}{chr(key2)}" for key1, key2 in self.table["plugs"].items()]
        )

        ind_desc: str = "INDICATORS"
        ind_msg: str = " ".join(
            [f"{chr(i1)}{chr(i2)}{chr(i3)}" for i1, i2, i3 in self.table["indicators"]]
        )
        descs: List[str] = [date_desc, rotor_desc, align_desc, plug_desc, ind_desc]
        msgs: List[str] = [date_msg, rotor_msg, align_msg, plug_msg, ind_msg]
        longest_desc: int = max([len(desc) for desc in descs])
        longest_msg: int = max([len(msg) for msg in msgs])

        title: str = "ENIGMA CONFIGURATION LOADED"
        longest_all: int = max(len(title), longest_desc + longest_msg + 1)  # +1 for the space between desc and msg.

        # Print table title.
        title_blanks: int = longest_all - len(title) + print_ext
        title_padding_left: int = title_blanks // 2
        assert title_padding_left >= 0
        title_padding_right: int = title_blanks - title_padding_left
        divider: str = "+" + "-" * (longest_all + print_ext) + "+"
        desc_ext: int = print_ext // 2
        msg_ext: int = print_ext - desc_ext

        print(divider)
        print("|" + " " * title_padding_left + title + " " * title_padding_right + "|") 
        print(divider)
        for desc, msg in zip(descs, msgs):
            desc_blanks: int = longest_desc - len(desc) + desc_ext 
            desc_left: int = desc_blanks // 2
            desc_right: int = desc_blanks - desc_left

            msg_blanks: int = longest_msg - len(msg) + msg_ext
            msg_left: int = msg_blanks // 2
            msg_right: int = msg_blanks - msg_left

            print("|" + " " * desc_left + desc + " "* desc_right + "|" +  " " * msg_left + msg +" " * msg_right + "|")
        print(divider)
        


    def rotate_rotors(self):
        # Rotate all rotors in use. From right to left.
        carry: bool = True
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
            reflected_index: int = self.reflector.input(input_index)

            # From left to right.
            output_index: int = reflected_index
            for rotor in self.rotors:
                output_index = rotor.input(output_index, reverse=True)

            # Convert to character.
            output_char = chr(output_index + 65)
            output_str += output_char

        return output_str


if __name__ == "__main__":
    input_message: str = "CHICKENMIZAIMAO"
    e = Enigma(print_cfg=True)
    encoded_message: str = e.input(input_message)
    e = Enigma()
    decoded_message: str = e.input(encoded_message)

    print(f"{input_message} -> {encoded_message} -> {decoded_message}")
