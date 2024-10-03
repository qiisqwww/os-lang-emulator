import platform

import pytest

from src.emulator import Emulator


@pytest.mark.parametrize(
    "expected",
    [
        ((f"System '{platform.uname().system}'\nNode '{platform.uname().node}'\nRelease "
          f"'{platform.uname().release}'\nVersion '{platform.uname().version}'\nMachine "
          f"'{platform.uname().machine}'"))
    ]
)
def test_ls_command(expected: str, emulator: Emulator) -> None:
    assert emulator.uname() == expected
