"""Rotor definitions."""

from typing import Dict, List

import numpy as np


class Rotor:
    def __init__(self, wiring: str):
        # Mapping info.
        mapping: Dict[int, int] = {k - 65: v - 65 for k, v in eval(wiring).items()}
        if len(mapping) != 26:
            raise NotImplementedError("Currently only support A-Z.")

        # Which character is at which location.
        self.loc: Dict[int, int] = {}
        self.length: int = len(mapping)
        self.current: int = 0  # Controls whether to step the next rotor.

        # Index 0 to convert from right to left;
        # Index 1 to convert from left to right.
        self.arr: np.ndarray = np.zeros([2, len(mapping)], dtype=np.uint8)

        sorted_keys: List[int] = sorted(mapping.keys())
        assert sorted_keys[0] == 0

        for i, in_char in enumerate(sorted_keys):
            self.arr[0][i] = mapping[in_char]
            self.arr[1][mapping[in_char]] = i

            self.loc[in_char] = i

    def tune(self, tunning_char: int):
        self.current = self.loc[tunning_char]

    def rotate(self) -> bool:
        """
        Rotate this rotor. If the index reaches to the end, send signal that the next rotor should be
        rotated as well.
        """
        self.current += 1
        if self.current == self.length:
            self.current = 0
            return True
        return False

    def input(self, input_index: int, reverse: bool) -> int:
        """Core function. Get output index."""
        internal_index: int = self.arr[1 if reverse else 0][
            ((26 - self.current) % 26 + input_index) % 26
        ]
        adjusted_index: int = abs(internal_index + self.current) % 26
        return adjusted_index


class Reflector:
    def __init__(self, wiring: str):
        self.mapping: Dict[int, int] = {k - 65: v - 65 for k, v in eval(wiring).items()}

    def input(self, input_index: int) -> int:
        """Core function. Input index is the absolute position on the wheel-like structure."""
        return self.mapping[input_index]
