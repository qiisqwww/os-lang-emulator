from xml.etree import ElementTree as ET

from src.emulator import Emulator
from src.emulator_gui import EmulatorGUI


def load_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()

    config = {
        'hostname': root.find('hostname').text,
        'fs_path': root.find('fs_path').text,
        'log_file_path': root.find('log_file_path').text,
        'start_script_path': root.find('start_script_path').text
    }
    return config


def start_emulator():
    config = load_config('../settings/config.xml')

    emulator = Emulator(config)
    gui = EmulatorGUI(emulator)
    gui.start()


if __name__ == "__main__":
    start_emulator()
