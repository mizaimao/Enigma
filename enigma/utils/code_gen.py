"""
Use a single seed to generate a code page.
A code page would contain:
    1. dates (ranges from 1 to 31, inclusively);
    2. rotors;
    3. ring settings;
    4. plugboard settings;
    5. indicators (no idea what this is and it not seems to be used).
"""
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from enigma.utils.constants import ROTOR_NAMES

DAYS: int = 31


class CodeGen:
    """Code generator."""

    def __init__(
        self,
        seed: int = None,
        n_rotors: int = 5,
        rotor_slots: int = 3,
        n_plugs: int = 6,
        i_groups: int = 4,
        extended: bool = False,
    ):
        """
        Args:
            seed: Seed for generation.
            n_rotors: Number of rotors (excluding reflector).
            rotor_slots: How many rotors are actually used.
            n_plugs: Number of used switches on the plugboard.
            extended: Whether to use the entire ASCII space. False means only capital A-Z.
        """
        assert rotor_slots <= n_rotors
        assert n_plugs <= 13  # 26 characters.

        self.rng: np.random._generator.Generator = np.random.default_rng(seed)
        self.n_dates: int = DAYS  # Normally 31 days.
        self.ranges: List[int] = list(range(128) if extended else range(65, 91))

        # Call each generation functions and get corresponding codes.
        self.rotors: List[List[int]] = self._gen_rotors(n_rotors, rotor_slots)
        self.alignments: List[List[int]] = self._gen_rotor_alignments(rotor_slots)
        self.plugs: Dict[int, int] = self._gen_plugs(n_plugs)
        self.indicators: List[List[int]] = self._gen_indicators(i_groups)

        # DataFrame to keep the record.
        self.df: pd.DataFrame = self.build_csv()

    def _gen_rotors(self, n_rotors: int, rotor_slots: int) -> List[List[int]]:
        """Generate a list for what rotors to use each day."""
        available_rotors: List[int] = list(range(n_rotors))
        rotors: List[List[int]] = []
        for _ in range(self.n_dates):
            self.rng.shuffle(available_rotors)
            rotors.append(available_rotors[:rotor_slots])
        return rotors

    def _gen_rotor_alignments(self, rotor_slots: int) -> List[List[int]]:
        """Rotor positions."""
        alignments: List[List[int]] = []
        available_keys: List[int] = self.ranges.copy()

        for _ in range(self.n_dates):
            alignments.append(self.rng.choice(available_keys, rotor_slots))
        return alignments

    def _gen_plugs(self, n_plugs: int) -> List[Dict[int, int]]:
        """Generate requested pair of switches."""
        plugs: List[Dict[int, int]] = []
        for _ in range(self.n_dates):
            available_keys: List[int] = self.ranges.copy()
            self.rng.shuffle(available_keys)
            plugs.append({})
            for _plug in range(n_plugs):
                key_0: int = available_keys.pop()
                key_1: int = available_keys.pop()

                plugs[-1][key_0] = key_1

            assert len(plugs[-1]) == n_plugs
        return plugs

    def _gen_indicators(self, i_groups: int) -> List[List[int]]:
        """
        Generate requested number of indicator groups. Each group comes with 3 characters.
        NOTE: If only capital letters are used, then the results will be lowercases;
        if uses the full ascii table, then the results will also be from any possible ascii characters.
        """
        indicators: List[List[int]] = []
        available_keys: List[int] = self.ranges.copy()
        offset: int = (
            32 if len(available_keys) == 26 else 0
        )  # "A" and "a" has a dist 32 in ascii table.

        for _ in range(self.n_dates):
            day_group: List[int] = []
            for _group in range(i_groups):
                self.rng.shuffle(available_keys)
                day_group.append([x + offset for x in available_keys[:3]])
            indicators.append(day_group.copy())

        return indicators

    def print_table_terminal(self):
        """Print the generated table to terminal."""

        def print_row(i: int):
            """Print info for each day."""
            breaker: str = " " * 4
            rotor_string_len: int = 9

            date: str = "{:02d}".format(self.n_dates - i)
            rotors: str = " ".join([ROTOR_NAMES[r] for r in self.rotors[i]])
            rotors += " " * (rotor_string_len - len(rotors))  # Add right padding.
            alignments: str = " ".join(
                ["{:02d}".format(r + 1) for r in self.alignments[i]]
            )
            plugs: str = " ".join(
                [f"{chr(key1)}{chr(key2)}" for key1, key2 in self.plugs[i].items()]
            )
            indicators: str = " ".join(
                [f"{chr(i1)}{chr(i2)}{chr(i3)}" for i1, i2, i3 in self.indicators[i]]
            )

            print(breaker.join([date, rotors, alignments, plugs, indicators]))

        # Print header line.
        header: str = (
            " " * 0
            + "DAY"
            + " " * 5
            + "ROTORS"
            + " " * 7
            + "RINGS"
            + " " * 11
            + "PLUGS"
            + " " * 13
            + "INDICATORS"
            + " " * 2
        )
        divider: str = "-" * len(header)
        print(divider)
        print(header)
        print(divider)

        for day in range(self.n_dates):
            print_row(day)
        print(divider)

    def build_csv(self):
        """Make a table version of generated info."""
        rows: List[Dict[str, Any]] = []
        for day in range(self.n_dates):
            row: Dict[str, Any] = {
                "day": self.n_dates - day,
                "rotors": self.rotors[day],
                "rings": list(self.alignments[day]),
                "plugs": self.plugs[day],
                "indicators": self.indicators[day],
            }
            rows.append(row.copy())
        self.df = pd.DataFrame(rows)

    def export_csv(self, dest: Path = None):
        """Save table to disk."""
        if self.df is None:
            self.build_csv()
        if dest is None:
            dest = Path(__file__).parent.parent.joinpath("tables", "default.csv")
        dest = Path(dest)
        print(f"Saving csv to {dest}...")
        self.df.to_csv(dest)


if __name__ == "__main__":
    gen = CodeGen(seed=42, n_rotors=5, rotor_slots=3, extended=False)
    gen.print_table_terminal()
    gen.export_csv()
