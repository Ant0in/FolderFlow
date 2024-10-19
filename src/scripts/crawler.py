
import os
import random


class Crawler:
    
    """
    Crawler is a class designed to manage and filter files in a directory based on allowed file extensions.
    It provides functionality to crawl through directories and retrieve files that match the specified extensions.

    Attributes:
    - _allowed_ext (list[str]): A list of allowed file extensions.

    Methods:
    - get_allowed() -> list[str]: Returns the list of allowed file extensions.
    - is_allowed(extension: str) -> bool: Checks if a given file extension is allowed.
    - add_allowed(*extensions: str) -> None: Adds new file extensions to the list of allowed extensions.
    - remove_allowed(*extensions: str) -> None: Removes specified file extensions from the list of allowed extensions.
    - clear_allowed() -> None: Clears all file extensions from the list of allowed extensions.
    - crawl_folder(root: str, local_only: bool = False, shuffle: bool = False, bypass_extension_limitation: bool = False) -> list[str]: Crawls the specified directory (root) and returns a list of valid files based on the allowed extensions.
        
    Parameters:
    - root (str): The root directory to crawl.
    - local_only (bool): If True, only crawls the specified root directory; if False, crawls subdirectories as well.
    - shuffle (bool): If True, shuffles the order of the returned files.
    - bypass_extension_limitation (bool): If True, ignores the allowed extensions limitation.

    Raises:
    - AssertionError: If the specified root path is not a directory or does not exist.
    """

    def __init__(self, *allowed_extensions: str) -> None:
        
        self._allowed_ext: list[str] = allowed_extensions

    def get_allowed(self) -> list[str]:
        return self._allowed_ext
    
    def is_allowed(self, extension: str) -> bool:
        return extension in self.get_allowed()
    
    def add_allowed(self, *extensions: str) -> None:
        for ext in extensions:
            if not self.is_allowed(ext):
                self.get_allowed().append(ext)

    def remove_allowed(self, *extensions: str) -> None:
        for ext in extensions:
            if self.is_allowed(ext):
                self.get_allowed().remove(ext)

    def clear_allowed(self) -> None:
        self.get_allowed().clear()
    
    def crawl_folder(self, root: str, local_only: bool = False, shuffle: bool = False, bypass_extension_limitation: bool = False) -> list[str]:

        assert (os.path.isdir(root) and os.path.exists(root))

        valid_files: list[str] = []

        if local_only:

            for file in os.listdir(root):
                fp: str = os.path.join(root, file)
                if bypass_extension_limitation or self.is_allowed(os.path.splitext(fp)[-1]): 
                    valid_files.append(fp)

        else:

            for subroot, _, files in os.walk(root):
                for file in files:
                    fp: str = os.path.join(subroot, file)
                    if bypass_extension_limitation or self.is_allowed(os.path.splitext(fp)[-1]):
                        valid_files.append(fp)

        if shuffle: random.shuffle(valid_files)

        return valid_files


