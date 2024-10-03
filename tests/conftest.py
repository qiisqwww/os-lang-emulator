import pytest

from src.start_emulator import load_config, ROOT_PATH
from src.emulator import Emulator


@pytest.fixture()
def emulator() -> Emulator:
    config = load_config(f'{ROOT_PATH}/settings/config.xml')
    config['log_file_path'] = f'{ROOT_PATH}/settings/log.csv'
    config['fs_path'] = f'{ROOT_PATH}/settings/filesystem.tar'
    return Emulator(config)
