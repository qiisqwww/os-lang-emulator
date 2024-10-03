import tarfile
import platform
from pathlib import Path

from src.logger import Logger

__all__ = [
    "Emulator"
]


ROOT_PATH = str(Path(__file__).resolve().parents[1])


class Emulator:
    hostname: str
    current_directory: str
    _logger: Logger
    _fs_path: str
    _start_script_path: str
    _file_system: dict

    def __init__(self, config) -> None:
        self.hostname = config["hostname"]
        self.current_directory = '/'
        self.logger = Logger(self.hostname, config['log_file_path'])
        self._fs_path = config['fs_path']
        self._start_script_path = config['start_script_path']
        self._file_system = {self.current_directory: []}  # initialize root directory

        self.load_file_system()

    def load_file_system(self) -> None:
        with tarfile.open(self._fs_path, 'r') as tar:
            for member in tar.getmembers():
                member.name = "/" + member.name
                member_path = member.name.split("/")
                if len(member_path) == 2:
                    self._file_system["/"].append(member.name)
                    self._file_system[member.name] = []
                    continue

                parent = "/".join(member_path[:-1])
                self._file_system[parent].append(member.name)
                self._file_system[member.name] = []

    def execute_command(self, command):
        command = command.strip().split()
        if not command:
            return
        cmd = command[0]

        print(f"Executing command: {cmd}")

        if cmd == "ls":
            self.logger.write("ls command input")
            return self.ls(command[1] if len(command) > 1 else self.current_directory)
        elif cmd == "cd" and len(command) > 1:
            self.logger.write("cd command input")
            return self.cd(command[1])
        elif cmd == "cd":
            return f"Must input path for '{cmd}' command."
        elif cmd == "exit":
            self.logger.write("exit command input")
            print("Exiting emulator.")
            exit()
        elif cmd == "uname":
            self.logger.write("uname command input")
            return self.uname()
        elif cmd == "tail":
            self.logger.write("tail command input")
            return self.tail(command[1] if len(command) > 1 else '')
        else:
            return f"Command '{cmd}' not found."

    def _get_absolute_path(self, path):
        if path == "." or path == "./":
            return self.current_directory
        if path == ".." or path == "../":
            parent = "/".join(self.current_directory.split("/")[:-1])
            return parent if len(parent) > 0 else "/"

        if self.current_directory == "/" and path[0] != "/":
            return self.current_directory + path
        elif self.current_directory == "/" and path[0] == "/":
            return path
        elif path[0] != "/":
            return self.current_directory + "/" + path
        else:
            return self.current_directory + path

    def ls(self, path):
        if (path == "." or path == "./" or path == ".." or path == "../") and self.current_directory == "/":
            return f"No such file or directory: '{path}'"

        if path not in self._file_system:
            path = self._get_absolute_path(path)
            if path not in self._file_system:
                return f"No such file or directory: '{path}'"

        if not self._file_system[path]:
            return ""

        files = [filename.split("/")[-1] for filename in self._file_system[path]]
        return '\t'.join(files)

    def cd(self, path):
        if (path == "." or path == "./" or path == ".." or path == "../") and self.current_directory == "/":
            return f"No such file or directory: '{path}'"

        if path not in self._file_system:
            path = self._get_absolute_path(path)
            if path not in self._file_system:
                return f"No such file or directory: '{path}'"

        self.current_directory = path

    def uname(self):
        uname = platform.uname()
        return (f"System '{uname.system}'\nNode '{uname.node}'\nRelease '{uname.release}'\n"
                f"Version '{uname.version}'\nMachine '{uname.machine}'")

    def _get_absolute_filepath(self, filepath):
        if self.current_directory == "/" and filepath[0] != "/":
            return self.current_directory + filepath
        elif self.current_directory == "/" and filepath[0] == "/":
            return filepath
        elif filepath[0] != "/":
            return self.current_directory + "/" + filepath
        else:
            return self.current_directory + filepath

    def tail(self, filepath: str):
        print(ROOT_PATH)

        if filepath not in self._file_system:
            filepath = self._get_absolute_filepath(filepath)
            if filepath not in self._file_system:
                return f"No such file or directory: '{filepath}'"

        res = "Last 10 lines of file:\n"
        filepath = ROOT_PATH + "\\" + filepath[1:].replace("/", "\\")
        with open(filepath, 'r') as f:
            lines = f.readlines()[-10:]
            res += '\n'.join(lines)

        return res
