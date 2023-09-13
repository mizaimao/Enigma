"""
Enigma configuration generator.
Will generate the following components:
    . specified number of rotors and their wiring;
    . reflector wiring;
"""

from typing import Any, Dict, List
from pathlib import Path

import pandas as pd
import numpy as np


class ConfigGen:
    """Generate random Enigma configurations."""

    def __init__(self, seed: int = None, n_rotors: int = 5, extended: bool = False):
        """
        Args:
            seed: RNG seed.
            n_rotors: How many rotors to generate.
            extended: Whether to use the entire ASCII space (128 chars vs 26 chars).
        """
        self.rng: np.random._generator.Generator = np.random.default_rng(seed)
        self.ranges: List[int] = list(range(128) if extended else range(65, 91))

        self.rotors: List[Dict[int, int]] = [
            self._gen_rotors() for _ in range(n_rotors)
        ]
        self.reflector: Dict[int, int] = self._gen_reflector()

        self.df: pd.DataFrame = self.build_csv()

    def _gen_rotors(self) -> Dict[int, int]:
        """Generate a rotor wiring mapping. A character may be mapped to itself."""
        input: List[int] = self.ranges.copy()
        output: List[int] = self.ranges.copy()
        self.rng.shuffle(input)
        self.rng.shuffle(output)
        return {
            input_char: output_char for input_char, output_char in zip(input, output)
        }

    def _gen_reflector(self) -> Dict[int, int]:
        """A bit different from rotor, because a character cannot map to itself."""
        chars: List[int] = self.ranges.copy()
        self.rng.shuffle(chars)
        reflector: Dict[int, int] = {}

        range_length: int = len(self.ranges)
        assert range_length % 2 == 0
        for _ in range(range_length // 2):
            input_char: int = chars.pop()
            output_char: int = chars.pop()

            reflector[input_char] = output_char
            reflector[output_char] = input_char

        return reflector

    def build_csv(self) -> pd.DataFrame:
        """Build a csv version of generated config."""
        rows: List[Dict[str, Dict[int, Any]]] = []
        for rotor in self.rotors:
            rows.append({"type": "rotor", "wiring": rotor})
        rows.append({"type": "reflector", "wiring": self.reflector})
        return pd.DataFrame(rows)

    def export_csv(self, dest: Path = None):
        """Save table to disk."""
        if self.df is None:
            self.build_csv()
        if dest is None:
            dest = Path(__file__).parent.parent.joinpath("configs", "default.csv")
        dest = Path(dest)
        print(f"Saving csv to {dest}...")
        self.df.to_csv(dest)


if __name__ == "__main__":
    c = ConfigGen(extended=False)
    c.export_csv()
