
import os
import random


class Crawler:

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


